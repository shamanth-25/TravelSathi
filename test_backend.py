from backend.ai_engine import get_response

response = get_response(
    query="Tell me about Bonalu",
    city="Hyderabad",
    language="Telugu",
    provider="Ollama"
)

print(response)