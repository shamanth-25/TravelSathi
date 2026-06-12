import os
import re
import json
import logging
import requests
from rag.rag_engine import get_rag_engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai_engine")

def clean_and_parse_json(text):
    """Clean markdown code block wrappers and parse JSON safely."""
    if not text:
        return None
    
    cleaned = text.strip()
    
    # Remove markdown code block markers if present
    if cleaned.startswith("```"):
        # Match ```json ... ``` or ``` ... ```
        match = re.match(r"^```(?:json)?\s*(.*?)\s*```$", cleaned, re.DOTALL)
        if match:
            cleaned = match.group(1).strip()
            
    try:
        data = json.loads(cleaned)
        return data
    except json.JSONDecodeError:
        # Try finding the first '{' and last '}' as a fallback
        try:
            start_idx = cleaned.find("{")
            end_idx = cleaned.rfind("}")
            if start_idx != -1 and end_idx != -1:
                json_str = cleaned[start_idx:end_idx + 1]
                return json.loads(json_str)
        except Exception as e:
            logger.error(f"Failed to parse JSON using braces fallback: {str(e)}")
            
    return None

def get_response(
    query,
    city,
    language,
    provider,
    api_key=None
):
    """
    Get response from the TravelSathi AI engine.
    
    Args:
        query (str): The user's travel or cultural query.
        city (str): The destination city (Hyderabad, Varanasi, Jaipur).
        language (str): The language in which the response should be returned.
        provider (str): The LLM provider ('ollama', 'gemini', 'openai').
        api_key (str, optional): API key for Gemini or OpenAI.
        
    Returns:
        dict: A dictionary containing:
            "answer" (str): The main response.
            "phrases" (list): A list of local phrases.
            "budget" (dict): Estimated budget breakdown.
    """
    # 1. Retrieve relevant context from RAG
    rag = get_rag_engine()
    context_chunks = rag.retrieve(query, city, top_k=2)
    context = "\n\n".join(context_chunks)
    
    # 2. Build the System and User Prompts
    system_prompt = f"""You are TravelSathi, an AI-powered multilingual cultural companion.
Your goal is to assist travelers with cultural insights, local spots, and tourist details.

You must answer the query for the given city: '{city}' using the retrieved context.
If the context does not contain the answer, use your pre-trained knowledge, but prioritize the retrieved context.

You must respond in the user's requested language: '{language}'.
The 'answer' field in your JSON response must be in '{language}'.

You must always output a single, valid JSON object in the following format:
{{
    "answer": "Your detailed response in the requested language...",
    "phrases": ["useful local language phrases in their script, with English transliteration/meaning if helpful"],
    "budget": {{
        "food": 1000,
        "travel": 500,
        "tickets": 300
    }}
}}

The "phrases" field must be a list of strings representing useful phrases in the local language of the city (e.g. Telugu for Hyderabad, Hindi/Rajasthani for Varanasi/Jaipur).
The "budget" field must be a dictionary with specific cost estimations in INR (Indian Rupees) related to the query or general daily costs (e.g., food, tickets, guide, transport). The values must be integers.

Do not output any text before or after the JSON object. Do not include markdown code block styling like ```json.
Ensure the JSON keys are exactly as specified: 'answer', 'phrases', 'budget'.
"""

    user_prompt = f"""City: {city}
Requested Language: {language}
Retrieved Context:
{context}

Query: {query}
"""

    provider_lower = provider.lower()
    raw_response_text = ""
    
    # 3. Call the selected provider
    if provider_lower == "openai":
        from openai import OpenAI
        
        # Use provided key or fall back to environment variable
        active_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not active_key:
            raise ValueError("OpenAI API key is required but not provided or found in environment variables.")
            
        client = OpenAI(api_key=active_key)
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            raw_response_text = response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise e

    elif provider_lower == "gemini":
        import google.generativeai as genai
        
        # Use provided key or fall back to environment variable
        active_key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if not active_key:
            raise ValueError("Gemini API key is required but not provided or found in environment variables.")
            
        genai.configure(api_key=active_key)
        
        try:
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config={
                    "response_mime_type": "application/json",
                    "temperature": 0.2
                }
            )
            # Combine system instruction and prompt for Gemini
            combined_prompt = f"{system_prompt}\n\nUser Query:\n{user_prompt}"
            response = model.generate_content(combined_prompt)
            raw_response_text = response.text
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise e

    elif provider_lower == "ollama":
        # Local Ollama endpoint
        ollama_url = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        
        # Auto-detect pulled models to select the best one
        model_name = "llama3.2:1b"  # Default fallback
        try:
            tags_resp = requests.get(f"{ollama_url}/api/tags", timeout=2)
            if tags_resp.status_code == 200:
                models = [m["name"] for m in tags_resp.json().get("models", [])]
                # Candidates in priority order
                candidates = ["gemma2:2b", "gemma:2b", "phi3", "phi3:mini", "llama3", "mistral"]
                found = False
                for candidate in candidates:
                    for m in models:
                        if m.startswith(candidate):
                            model_name = m
                            found = True
                            break
                    if found:
                        break
                if not found and models:
                    model_name = models[0]  # default to first available
                logger.info(f"Ollama auto-detected model: {model_name}")
        except Exception as e:
            logger.warning(f"Could not connect to Ollama to list models: {str(e)}. Using default model: {model_name}")

        try:
            payload = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "format": "json",
                "stream": False,
                "options": {
                    "temperature": 0.2
                }
            }
            ollama_resp = requests.post(f"{ollama_url}/api/chat", json=payload, timeout=30)
            if ollama_resp.status_code != 200:
                raise RuntimeError(f"Ollama returned error status {ollama_resp.status_code}: {ollama_resp.text}")
                
            raw_response_text = ollama_resp.json().get("message", {}).get("content", "")
        except Exception as e:
            logger.error(f"Ollama connection error: {str(e)}")
            raise RuntimeError(f"Failed to communicate with Ollama: {str(e)}")
            
    else:
        raise ValueError(f"Unsupported provider: '{provider}'. Supported: 'openai', 'gemini', 'ollama'")

    # 4. Parse and validate the response
    data = clean_and_parse_json(raw_response_text)
    
    if data is None:
        logger.warning(f"Could not parse valid JSON from raw response: {raw_response_text}")
        # Build fallback structure
        return {
            "answer": raw_response_text or "No response received.",
            "phrases": [],
            "budget": {}
        }
        
    # Standardize and validate required keys
    standardized_response = {
        "answer": str(data.get("answer", "No response received.")),
        "phrases": list(data.get("phrases", [])),
        "budget": dict(data.get("budget", {}))
    }
    
    return standardized_response
