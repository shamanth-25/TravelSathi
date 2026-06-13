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
            
    def validate_parsed_data(data):
        if not data or not isinstance(data, dict):
            return None
            
        answer_str = str(data.get("answer", ""))
        if "Your highly detailed" in answer_str or "engaging multi-paragraph" in answer_str or "<detailed, comprehensive" in answer_str:
            logger.warning("Auto-detected literal template placeholder in AI response answer.")
            return None
            
        phrases_list = data.get("phrases", [])
        if phrases_list and isinstance(phrases_list, list):
            for p in phrases_list:
                if isinstance(p, dict):
                    phrase_val = str(p.get("phrase", ""))
                    trans_val = str(p.get("translation", ""))
                    pron_val = str(p.get("pronunciation", ""))
                    if (
                        "Meaning in" in phrase_val or
                        "Phrase in the local language" in trans_val or
                        "Romanized pronunciation guide" in pron_val or
                        "<original phrase>" in phrase_val or
                        "<English phrase>" in phrase_val or
                        "<translation" in trans_val or
                        "<romanized" in pron_val
                    ):
                        logger.warning("Auto-detected literal template placeholders in AI response phrases.")
                        return None
        return data

    try:
        # Use strict=False to allow unescaped control characters like literal newlines or tabs
        data = json.loads(cleaned, strict=False)
        return validate_parsed_data(data)
    except json.JSONDecodeError:
        pass

    # Heuristic repair for premature closing braces before top-level keys
    repaired = re.sub(r'\}\s*,\s*"(phrases|budget)"', r', "\1"', cleaned)
    
    try:
        data = json.loads(repaired, strict=False)
        return validate_parsed_data(data)
    except json.JSONDecodeError:
        # Try finding the first '{' and last '}' as a fallback on the repaired text
        try:
            start_idx = repaired.find("{")
            end_idx = repaired.rfind("}")
            if start_idx != -1 and end_idx != -1:
                json_str = repaired[start_idx:end_idx + 1]
                data = json.loads(json_str, strict=False)
                return validate_parsed_data(data)
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
        provider (str): The LLM provider ('ollama', 'groq', 'openrouter').
        api_key (str, optional): API key for Groq or OpenRouter.
    
    Returns:
        dict: A dictionary containing:
            - 'answer': Multi-paragraph itinerary or insight.
            - 'phrases': Local language phrases.
            - 'budget': Estimated daily costs.
    """
    provider_lower = str(provider).lower()
    is_phrase_query = query.startswith("TRANSLATE_PHRASE:") or "useful phrases" in query.lower() or "get phrases" in query.lower()
    if provider_lower == "ollama" and is_phrase_query:
        raise ValueError("Ollama phrase translation is bypassed in favor of accurate local offline translation.")

    # Map code to full language name (e.g. 'te' -> 'Telugu', 'hi' -> 'Hindi', 'en' -> 'English')
    lang_map = {
        "en": "English",
        "te": "Telugu",
        "hi": "Hindi",
        "english": "English",
        "telugu": "Telugu",
        "hindi": "Hindi"
    }
    lang_full = lang_map.get(str(language).lower(), str(language))

    # Map city to its primary local language name and script
    city_to_local_lang = {
        "hyderabad": ("Telugu", "తెలుగు"),
        "varanasi": ("Hindi", "हिन्दी"),
        "jaipur": ("Rajasthani/Hindi", "राजस्थानी/हिन्दी"),
        "mumbai": ("Marathi", "मराठी"),
        "kolkata": ("Bengali", "বাংলা"),
        "delhi": ("Hindi", "हिन्दी"),
        "chennai": ("Tamil", "தமிழ்"),
        "ahmedabad": ("Gujarati", "ગુજરાતી"),
        "general": ("Hindi", "हिन्दी")
    }
    
    # Map city keywords in different languages to their standard key
    city_matches = {
        "hyderabad": ["hyderabad", "హైదరాబాద్", "हैदराबाद"],
        "varanasi": ["varanasi", "వారణాసి", "वाराणसी"],
        "jaipur": ["jaipur", "జైపూర్", "जयपुर"],
        "mumbai": ["mumbai", "ముంబై", "मुंबई"],
        "kolkata": ["kolkata", "కోల్‌కతా", "कोलकाता"],
        "delhi": ["delhi", "ఢిల్లీ", "दिल्ली"],
        "chennai": ["chennai", "చెన్నై", "चेन्नई"],
        "ahmedabad": ["ahmedabad", "అహ్మదాబాద్", "अहमदाबाद"]
    }
    
    city_lower = str(city).lower()
    matched_city_key = "general"
    for key, aliases in city_matches.items():
        if any(alias in city_lower for alias in aliases):
            matched_city_key = key
            break
            
    local_lang_name, local_lang_script = city_to_local_lang.get(matched_city_key, ("Hindi", "हिन्दी"))

    # Standardize city to standard capitalized English for RAG and LLM prompts
    city = matched_city_key.capitalize()

    # 1. Retrieve relevant context from RAG
    rag = get_rag_engine()
    context_chunks = rag.retrieve(query, city, top_k=2)
    context = "\n\n".join(context_chunks)
    
    # Detect num_days if present in query
    days_match = re.search(r"Generate (\d+)-day itinerary", query, re.IGNORECASE)
    num_days = 3
    if days_match:
        num_days = int(days_match.group(1))
    
    # 2. Build the System and User Prompts
    if query.startswith("TRANSLATE_PHRASE:"):
        phrase_to_translate = query.replace("TRANSLATE_PHRASE:", "").strip()
        system_prompt = f"""You are TravelSathi, an AI-powered translation assistant.
Your task is to translate the phrase(s) provided into the primary local language spoken in the city of '{city}', which is '{local_lang_name}' (using the '{local_lang_script}' script).

If the input contains multiple phrases (e.g., separated by commas, semicolons, or newlines), you MUST translate each phrase separately and output a dictionary for each in the 'phrases' list.

You must output a valid JSON object exactly in this format:
{{
    "answer": "Here is the translation:",
    "phrases": [
        {{
            "phrase": "Hello",
            "translation": "নমস্কার",
            "pronunciation": "Nomoshkar"
        }}
    ],
    "budget": {{}}
}}

Do not output any text before or after the JSON.
"""
        user_prompt = f"Please translate this phrase: {phrase_to_translate}"
    elif "useful phrases" in query.lower() or "get phrases" in query.lower():
        system_prompt = f"""You are TravelSathi, an AI-powered multilingual cultural companion.
Your task is to provide a list of 5-8 useful everyday travel phrases (like greetings, asking for directions, ordering food, emergency) for a tourist visiting the city of '{city}'.

The phrases MUST be in the primary local language of '{city}', which is '{local_lang_name}' (using the '{local_lang_script}' script).

For each phrase, provide:
1. The English phrase (e.g. "Hello", "How much does this cost?", "Where is the toilet?")
2. The translation in '{local_lang_name}' script (e.g. for Hindi, 'नमस्ते'; for Telugu, 'నమస్కారం')
3. The romanized English pronunciation guide (e.g. 'Namaste' or 'Namaskaram')

You must respond in the user's requested language: '{lang_full}'.
The 'answer' field in your JSON response must contain a brief greeting and overview of '{local_lang_name}' language in '{lang_full}'.

You must always output a single, valid JSON object in this format:
{{
    "answer": "Welcome to the language guide!",
    "phrases": [
        {{
            "phrase": "Hello",
            "translation": "নమস্কার",
            "pronunciation": "Nomoshkar"
        }}
    ],
    "budget": {{}}
}}

Do not output any text before or after the JSON.
"""
        user_prompt = f"Please generate a list of useful phrases for the city of '{city}' in its local language '{local_lang_name}'."
    elif query.startswith("festival:"):
        festival_name = query.replace("festival:", "").strip()
        system_prompt = f"""You are TravelSathi, an AI-powered multilingual cultural companion.
Your goal is to provide a detailed, comprehensive, and engaging overview of the festival '{festival_name}' in the city of '{city}'.

Using the retrieved context, explain the significance, history, customs, and key rituals of the festival.
If the context does not contain the answer, use your pre-trained knowledge, but prioritize the retrieved context.

CRITICAL INSTRUCTION: You must write the festival explanation (the 'answer' field of the JSON response) in the requested language: '{lang_full}'.
- If the requested language is 'Telugu', you MUST output in Telugu script (తెలుగు).
- If the requested language is 'Hindi', you MUST output in Hindi/Devanagari script (हिन्दी).
- Do NOT output in English or Romanized script. You must perform translation of the English source context into the target language.

You must always output a single, valid JSON object in this format:
{{
    "answer": "<detailed, comprehensive, and engaging explanation of the festival in '{lang_full}'>",
    "phrases": [],
    "budget": {{}}
}}

Do not output any text before or after the JSON.
"""
        user_prompt = f"""City: {city}
Requested Language: {lang_full}
Retrieved Context:
{context}

Query: Explain the festival {festival_name} in {city}.
"""
    else:
        system_prompt = f"""You are TravelSathi, an AI-powered multilingual cultural companion.
Your goal is to assist travelers with cultural insights, local spots, and tourist details.

You must answer the query for the given city: '{city}' using the retrieved context.
If the context does not contain the answer, use your pre-trained knowledge, but prioritize the retrieved context.

CRITICAL INSTRUCTION 1: Your response must be HIGHLY DETAILED and COMPREHENSIVE. Do not give a minimal or brief summary. Write a rich, multi-paragraph itinerary describing the atmosphere, specific activities, history, and reasons to visit each place. Provide a clear day-by-day breakdown (from Day 1 up to Day {num_days}) detailing specific places and activities.

CRITICAL INSTRUCTION 2 (INTERESTS): If the user specifies "Interests" in their query, you MUST tailor the ENTIRE itinerary heavily around those specific interests! For example, if the interests mention "streetfood" or "food", you MUST dedicate the itinerary to local dishes, famous food markets, street food tours, and what specific foods to try each day rather than just historical sightseeing.

CRITICAL INSTRUCTION: You must write the response (the 'answer' field of the JSON response) in the requested language: '{lang_full}'.
- If the requested language is 'Telugu', you MUST output in Telugu script (తెలుగు).
- If the requested language is 'Hindi', you MUST output in Hindi/Devanagari script (हिन्दी).
- Do NOT output in English or Romanized script. You must perform translation of the English source context into the target language.

CRITICAL INSTRUCTION 3 (JSON FORMAT & LOCAL PHRASES): 
- You must always output a single, valid JSON object in the exact format below. 
- Do NOT translate the JSON keys (e.g., keep them as 'answer', 'phrases', 'budget', 'phrase', 'translation', 'pronunciation'). 
- The "phrases" field MUST be a list of dictionaries, NOT a list of strings.
- IMPORTANT: The phrases themselves MUST be in the PRIMARY LOCAL LANGUAGE of the destination city '{city}' (e.g., Telugu for Hyderabad, Rajasthani/Hindi for Jaipur), REGARDLESS of the user's requested language '{lang_full}'!

{{
    "answer": "Your highly detailed, comprehensive, and engaging response...",
    "phrases": [
        {{
            "phrase": "Hello",
            "translation": "নమস্কার",
            "pronunciation": "Nomoshkar"
        }}
    ],
    "budget": {{
        "food": 1000,
        "travel": 500,
        "tickets": 300
    }}
}}

The "phrases" field must be a list of dictionaries representing useful phrases in the local language of the city.
The "budget" field must be a dictionary with specific cost estimations in INR (Indian Rupees) related to the query or general daily costs (e.g., food, tickets, guide, transport). The values must be integers.

Do not output any text before or after the JSON object. Do not include markdown code block styling like ```json.
Ensure the JSON keys are exactly as specified: 'answer', 'phrases', 'budget'.
"""

        user_prompt = f"""City: {city}
Requested Language: {lang_full}
Retrieved Context:
{context}

Query: {query}
"""

    provider_lower = provider.lower()
    raw_response_text = ""
    
    # 3. Call the selected provider
    if provider_lower == "openrouter":
        from openai import OpenAI
        
        # Use provided key
        active_key = api_key
        if not active_key:
            raise ValueError("OpenRouter API key is required but not provided.")
            
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=active_key,
        )
        
        try:
            response = client.chat.completions.create(
                model="google/gemini-2.5-flash", # A fast and high-quality OpenRouter model
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.2,
                max_tokens=4000
            )
            raw_response_text = response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenRouter API error: {str(e)}")
            raise e

    elif provider_lower == "groq":
        from openai import OpenAI
        
        # Use provided key
        active_key = api_key
        if not active_key:
            raise ValueError("Groq API key is required but not provided.")
            
        client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=active_key,
        )
        
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant", # Groq's fast and highly-available model with much higher rate limits
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            raw_response_text = response.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq API error: {str(e)}")
            raise e


    elif provider_lower == "ollama":
        # Check Streamlit session state for endpoint first, with env/localhost fallback
        try:
            import streamlit as st
            ollama_url = st.session_state.get("ollama_url") or os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        except Exception:
            ollama_url = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
            
        # Auto-detect pulled models to select the best one
        model_name = "llama3.2:1b"  # Default fallback
        try:
            tags_resp = requests.get(f"{ollama_url}/api/tags", timeout=2)
            if tags_resp.status_code == 200:
                models = [m["name"] for m in tags_resp.json().get("models", [])]
                # Candidates in priority order
                candidates = ["qwen2.5:1.5b", "llama3.2:1b", "phi3","gemma2:2b", "gemma:2b", "mistral"]
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
            ollama_resp = requests.post(f"{ollama_url}/api/chat", json=payload, timeout=90)
            if ollama_resp.status_code != 200:
                raise RuntimeError(f"Ollama returned error status {ollama_resp.status_code}: {ollama_resp.text}")
                
            raw_response_text = ollama_resp.json().get("message", {}).get("content", "")
        except Exception as e:
            logger.error(f"Ollama connection error: {str(e)}")
            raise RuntimeError(f"Failed to communicate with Ollama: {str(e)}")
            
    elif provider_lower == "gemini":
        import google.generativeai as genai
        
        active_key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if not active_key:
            raise ValueError("Gemini API key is required but not provided.")
            
        genai.configure(api_key=active_key)
        
        try:
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=system_prompt
            )
            response = model.generate_content(
                user_prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    temperature=0.2
                )
            )
            raw_response_text = response.text
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise e
    else:
        raise ValueError(f"Unsupported provider: '{provider}'. Supported: 'gemini', 'openrouter', 'groq', 'ollama'")

    data = clean_and_parse_json(raw_response_text)
    if data is None:
        raise ValueError(f"Failed to parse valid JSON response from provider. Raw response: {raw_response_text}")
        
    # Standardize and validate required keys
    standardized_response = {
        "answer": str(data.get("answer", "No response received.")),
        "phrases": list(data.get("phrases", [])),
        "budget": dict(data.get("budget", {}))
    }
    
    return standardized_response
