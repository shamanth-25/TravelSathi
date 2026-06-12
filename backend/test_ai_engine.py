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
        results = self.rag.retrieve("historical details", "delhi", top_k=1)
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


class TestAIEngineRouting(unittest.TestCase):
    @patch("openai.resources.chat.Completions.create")
    @patch("openai.OpenAI")
    def test_openai_provider(self, mock_openai_class, mock_create):
        # Set up mocks
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_choice = MagicMock()
        mock_choice.message.content = '{"answer": "OpenAI Success", "phrases": ["Hello"], "budget": {"food": 50}}'
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response

        # Call get_response
        res = get_response(
            query="tell me about Charminar",
            city="hyderabad",
            language="english",
            provider="openai",
            api_key="mock-key-123"
        )

        # Assertions
        self.assertEqual(res["answer"], "OpenAI Success")
        self.assertEqual(res["phrases"], ["Hello"])
        self.assertEqual(res["budget"], {"food": 50})

    @patch("google.generativeai.GenerativeModel")
    @patch("google.generativeai.configure")
    def test_gemini_provider(self, mock_configure, mock_model_class):
        # Set up mocks
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model
        
        mock_response = MagicMock()
        mock_response.text = '{"answer": "Gemini Success", "phrases": ["Namaste"], "budget": {"travel": 150}}'
        mock_model.generate_content.return_value = mock_response

        # Call get_response
        res = get_response(
            query="tell me about Ganga Aarti",
            city="varanasi",
            language="english",
            provider="gemini",
            api_key="mock-key-123"
        )

        # Assertions
        self.assertEqual(res["answer"], "Gemini Success")
        self.assertEqual(res["phrases"], ["Namaste"])
        self.assertEqual(res["budget"], {"travel": 150})

    @patch("requests.post")
    @patch("requests.get")
    def test_ollama_provider(self, mock_get, mock_post):
        # Set up mocks for tags (models listing)
        mock_get_response = MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = {"models": [{"name": "gemma2:2b"}]}
        mock_get.return_value = mock_get_response

        # Set up mocks for chat completion
        mock_post_response = MagicMock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = {
            "message": {
                "content": '{"answer": "Ollama Success", "phrases": ["Ram Ram"], "budget": {"tickets": 100}}'
            }
        }
        mock_post.return_value = mock_post_response

        # Call get_response
        res = get_response(
            query="tell me about Amer Fort",
            city="jaipur",
            language="english",
            provider="ollama"
        )

        # Assertions
        self.assertEqual(res["answer"], "Ollama Success")
        self.assertEqual(res["phrases"], ["Ram Ram"])
        self.assertEqual(res["budget"], {"tickets": 100})

    def test_missing_api_key_raises_error(self):
        # Clean environment variables temporarily
        openai_key = os.environ.pop("OPENAI_API_KEY", None)
        gemini_key = os.environ.pop("GEMINI_API_KEY", None)
        google_key = os.environ.pop("GOOGLE_API_KEY", None)

        try:
            with self.assertRaises(ValueError):
                get_response("test", "hyderabad", "english", "openai", api_key=None)

            with self.assertRaises(ValueError):
                get_response("test", "varanasi", "english", "gemini", api_key=None)
        finally:
            # Restore environment variables
            if openai_key: os.environ["OPENAI_API_KEY"] = openai_key
            if gemini_key: os.environ["GEMINI_API_KEY"] = gemini_key
            if google_key: os.environ["GOOGLE_API_KEY"] = google_key

    def test_unsupported_provider_raises_error(self):
        with self.assertRaises(ValueError):
            get_response("test", "hyderabad", "english", "unsupported-llm")


if __name__ == "__main__":
    unittest.main()
