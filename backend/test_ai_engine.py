import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Ensure project root is in the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.rag_engine import get_rag_engine
from backend.ai_engine import get_response, clean_and_parse_json


class TestRAGEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rag = get_rag_engine()

    def test_hyderabad_retrieval(self):
        results = self.rag.retrieve("Tell me about Charminar mosque", "hyderabad", top_k=1)
        self.assertGreater(len(results), 0)
        self.assertIn("charminar", results[0].lower())

    def test_varanasi_retrieval(self):
        results = self.rag.retrieve("What is the evening Ganga Aarti ritual?", "varanasi", top_k=1)
        self.assertGreater(len(results), 0)
        self.assertIn("aarti", results[0].lower())

    def test_jaipur_retrieval(self):
        results = self.rag.retrieve("Tell me about Amer Fort architecture", "jaipur", top_k=1)
        self.assertGreater(len(results), 0)
        self.assertIn("amer", results[0].lower())

    def test_unsupported_city(self):
        results = self.rag.retrieve("historical details", "bengaluru", top_k=1)
        self.assertEqual(len(results), 0)


class TestJSONParser(unittest.TestCase):
    def test_clean_json_standard(self):
        raw = '{"answer": "Hello", "phrases": ["Hi"], "budget": {"food": 100}}'
        parsed = clean_and_parse_json(raw)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["answer"], "Hello")
        self.assertEqual(parsed["phrases"], ["Hi"])
        self.assertEqual(parsed["budget"]["food"], 100)

    def test_clean_json_markdown(self):
        raw = '```json\n{"answer": "Hello Markdown", "phrases": [], "budget": {}}\n```'
        parsed = clean_and_parse_json(raw)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["answer"], "Hello Markdown")

    def test_clean_json_with_text(self):
        raw = 'Sure, here is the response:\n{\n  "answer": "Hello Text Wrapper",\n  "phrases": [],\n  "budget": {}\n}\nHope this helps!'
        parsed = clean_and_parse_json(raw)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["answer"], "Hello Text Wrapper")

    def test_invalid_json(self):
        raw = 'this is not json at all'
        parsed = clean_and_parse_json(raw)
        self.assertIsNone(parsed)

    def test_clean_json_premature_braces(self):
        raw = '{"answer": "Welcome to Kolkata, the \'City of Joy\'! Your 3-day itinerary, with a focus on temples..." }, "phrases": [ { "phrase": "Hello" } ], "budget": { "food": 4500 } }'
        parsed = clean_and_parse_json(raw)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["answer"], "Welcome to Kolkata, the 'City of Joy'! Your 3-day itinerary, with a focus on temples...")
        self.assertEqual(parsed["phrases"][0]["phrase"], "Hello")
        self.assertEqual(parsed["budget"]["food"], 4500)

    def test_clean_json_with_literal_newlines(self):
        raw = '{\n  "answer": "Day 1:\n- Temple visit\nDay 2:\n- Food",\n  "phrases": [],\n  "budget": {}\n}'
        parsed = clean_and_parse_json(raw)
        self.assertIsNotNone(parsed)
        self.assertIn("Day 1:", parsed["answer"])


class TestAIEngineRouting(unittest.TestCase):
    @patch("openai.resources.chat.Completions.create")
    @patch("openai.OpenAI")
    def test_openrouter_provider(self, mock_openai_class, mock_create):
        # Setup mock client
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_choice = MagicMock()
        mock_choice.message.content = '{"answer": "OpenRouter Success", "phrases": ["Hello"], "budget": {"food": 50}}'
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response
        
        res = get_response(
            query="test",
            city="hyderabad",
            language="english",
            provider="openrouter",
            api_key="fake_key"
        )
        
        self.assertEqual(res["answer"], "OpenRouter Success")
        self.assertIn("Hello", res["phrases"])
        self.assertEqual(res["budget"]["food"], 50)
        
        # Verify call
        mock_client.chat.completions.create.assert_called_once()

    @patch("openai.resources.chat.Completions.create")
    @patch("openai.OpenAI")
    def test_groq_provider(self, mock_openai_class, mock_create):
        # Setup mock client
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_choice = MagicMock()
        mock_choice.message.content = '{"answer": "Groq Success", "phrases": ["Namaste"], "budget": {"travel": 150}}'
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response
        
        res = get_response(
            query="test",
            city="varanasi",
            language="english",
            provider="groq",
            api_key="fake_key"
        )
        
        self.assertEqual(res["answer"], "Groq Success")
        self.assertIn("Namaste", res["phrases"])
        self.assertEqual(res["budget"]["travel"], 150)
        
        # Verify call
        mock_client.chat.completions.create.assert_called_once()

    @patch("requests.post")
    @patch("requests.get")
    def test_ollama_provider(self, mock_get, mock_post):
        # Mock tags response
        mock_tags = MagicMock()
        mock_tags.status_code = 200
        mock_tags.json.return_value = {"models": [{"name": "llama3.2:1b"}]}
        mock_get.return_value = mock_tags

        # Mock chat response
        mock_chat = MagicMock()
        mock_chat.status_code = 200
        mock_chat.json.return_value = {
            "message": {
                "content": '{"answer": "Ollama Success", "phrases": [], "budget": {}}'
            }
        }
        mock_post.return_value = mock_chat

        res = get_response(
            query="test",
            city="jaipur",
            language="english",
            provider="ollama"
        )
        
        self.assertEqual(res["answer"], "Ollama Success")
        mock_post.assert_called_once()

    def test_missing_api_keys(self):
        # Temporarily remove env vars to test error paths
        openrouter_key = os.environ.pop("OPENROUTER_API_KEY", None)
        groq_key = os.environ.pop("GROQ_API_KEY", None)
        
        try:
            with self.assertRaises(ValueError):
                get_response("test", "hyderabad", "english", "openrouter", api_key=None)
                
            with self.assertRaises(ValueError):
                get_response("test", "varanasi", "english", "groq", api_key=None)
        finally:
            if openrouter_key: os.environ["OPENROUTER_API_KEY"] = openrouter_key
            if groq_key: os.environ["GROQ_API_KEY"] = groq_key

    def test_unsupported_provider_raises_error(self):
        with self.assertRaises(ValueError):
            get_response("test", "hyderabad", "english", "unsupported-llm")


if __name__ == "__main__":
    unittest.main()
