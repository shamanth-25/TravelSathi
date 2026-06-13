import unittest
import sys
import os

# Ensure project root is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.api import get_response

class TestAPIUtils(unittest.TestCase):
    def setUp(self):
        # Force backend check to fail or not use active API keys so we always test the mock fallback
        # by temporarily clearing environment variables.
        self.old_openrouter_key = os.environ.pop("OPENROUTER_API_KEY", None)
        self.old_groq_key = os.environ.pop("GROQ_API_KEY", None)

    def tearDown(self):
        # Restore environment variables
        if self.old_openrouter_key:
            os.environ["OPENROUTER_API_KEY"] = self.old_openrouter_key
        if self.old_groq_key:
            os.environ["GROQ_API_KEY"] = self.old_groq_key

    def test_default_itinerary(self):
        res = get_response(
            query="Generate a plan for Jaipur",
            city="Jaipur",
            language="en",
            provider="Gemini"
        )
        self.assertIn("Amer Fort", res["answer"])
        self.assertIn("Hawa Mahal", res["answer"])
        self.assertEqual(res["budget"]["Accommodation 🏨"], 40)
        self.assertEqual(res["budget"]["Food & Dining 🍽️"], 25)

    def test_temples_itinerary_english(self):
        res = get_response(
            query="We want to visit temples and spiritual places in Varanasi",
            city="Varanasi",
            language="en",
            provider="Gemini"
        )
        self.assertIn("Kashi Vishwanath", res["answer"])
        self.assertIn("Ganga Aarti", res["answer"])
        self.assertIn("Sankat Mochan", res["answer"])
        self.assertEqual(res["budget"]["Sightseeing 🎟️"], 25) # should increase

    def test_food_itinerary_hindi(self):
        res = get_response(
            query="बिरयानी और खाना खाने का मन है",
            city="Hyderabad",
            language="hi",
            provider="Gemini"
        )
        self.assertIn("ईरानी चाय और उस्मानिया बिस्कुट", res["answer"])
        self.assertIn("निजामी दावत", res["answer"])
        self.assertEqual(res["budget"]["भोजन (Food & Dining) 🍽️"], 40) # should increase to 40%

    def test_multiple_interests_blend(self):
        # Temples + Food
        res = get_response(
            query="temples and street food",
            city="Hyderabad",
            language="en",
            provider="Gemini"
        )
        # Day 1: temples (Birla Mandir)
        self.assertIn("Birla Mandir", res["answer"])
        # Day 2: food (Local Dining / Nimrah Cafe)
        self.assertIn("shawarma", res["answer"])
        # Day 3: temples (Jagannath Temple)
        self.assertIn("Jagannath Temple", res["answer"])

    def test_long_duration_unique_itinerary(self):
        # Generate a 10-day temples itinerary for Hyderabad and make sure no two days have identical descriptions
        res = get_response(
            query="Generate 10-day itinerary for Hyderabad. Interests: temples",
            city="Hyderabad",
            language="en",
            provider="Gemini"
        )
        
        answer = res["answer"]
        lines = [line.strip() for line in answer.split("\n") if line.strip().startswith("- ")]
        
        # We expect 10 day entries in the itinerary
        self.assertEqual(len(lines), 10)
        
        # We expect all descriptions to be unique
        self.assertEqual(len(set(lines)), 10)

        # Ensure that consecutive days do not repeat the same suffix/mod text
        import re
        bold_texts = []
        for line in lines:
            m = re.search(r"\*\*(.*?)\*\*", line)
            if m:
                bold_texts.append(m.group(1))
                
        suffixes = []
        for bt in bold_texts:
            if " - " in bt:
                suffixes.append(bt.split(" - ")[-1])
            else:
                suffixes.append("original")
                
        for i in range(len(suffixes) - 1):
            if suffixes[i] != "original" or suffixes[i+1] != "original":
                self.assertNotEqual(suffixes[i], suffixes[i+1], f"Consecutive days {i+1} and {i+2} repeated suffix: {suffixes[i]}")

    def test_all_cities_unique_experiences(self):
        # Verify that for all 8 cities, a 7-day itinerary for temples, food, and nature returns 7 unique base items.
        cities = ["Hyderabad", "Varanasi", "Jaipur", "Mumbai", "Kolkata", "Delhi", "Chennai", "Ahmedabad"]
        interests_list = ["temples", "street food", "nature"]
        
        for city in cities:
            for interest in interests_list:
                res = get_response(
                    query=f"Generate 7-day itinerary for {city}. Interests: {interest}",
                    city=city,
                    language="en",
                    provider="Gemini"
                )
                
                answer = res["answer"]
                lines = [line.strip() for line in answer.split("\n") if line.strip().startswith("- ")]
                
                # Check we generated 7 items
                self.assertEqual(len(lines), 7, f"Expected 7 days for {city} with {interest}, got {len(lines)}")
                
                # Extract the base attraction name (everything before the colon or suffix modifier)
                base_spots = []
                import re
                for line in lines:
                    m = re.search(r"\*\*(.*?)\*\*", line)
                    if m:
                        title = m.group(1)
                        # Strip off any modifier suffix like " - Evening Aarti & Meditation"
                        if " - " in title:
                            title = title.split(" - ")[0]
                        base_spots.append(title.strip())
                
                # Verify that all 7 base spots are unique
                self.assertEqual(len(set(base_spots)), 7, f"Repetitive base attractions found for {city} ({interest}): {base_spots}")

if __name__ == "__main__":
    unittest.main()
