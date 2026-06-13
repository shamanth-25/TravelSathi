# TravelSathi User Manual

## Introduction

TravelSathi is an AI-powered travel companion designed to help users plan trips with personalized itineraries, budget estimates, local phrases, and destination insights. It supports both online and offline modes using Ollama.

---

## System Requirements

* Python 3.11 or above
* Streamlit
* Internet connection (for online models)
* Ollama installed (for offline mode)

---

## Starting the Application

### Local Execution

Run the following command:

```bash
streamlit run app.py
```

Open the application in your browser:

```text
http://localhost:8501
```

---

## Using TravelSathi

### Step 1: Select Destination

Choose one of the supported destinations:

* Hyderabad
* Jaipur
* Varanasi

---

### Step 2: Enter Your Query

Examples:

* Plan a 2-day itinerary for Hyderabad.
* Tell me about Bonalu festival.
* Suggest budget-friendly places to visit in Jaipur.
* Give me useful Telugu phrases for tourists.

---

### Step 3: Choose AI Provider

Available providers:

#### Ollama (Offline)

Requirements:

```bash
ollama serve
```

Supported local models include:

* qwen2.5:1.5b
* llama3.2:1b

#### Gemini

Provide a valid Gemini API key.

#### OpenAI

Provide a valid OpenAI API key.

---

### Step 4: Select Language

Choose the preferred response language.

TravelSathi will generate:

* Answers in the selected language
* Useful local phrases
* Budget estimates

---

## Understanding the Output

TravelSathi provides:

### Answer

Destination-specific travel recommendations.

### Local Phrases

Examples of useful phrases in the local language.

### Budget Breakdown

Estimated costs for:

* Food
* Travel
* Tickets

All values are displayed in INR.

---

## Troubleshooting

### Ollama Not Running

Error:

```text
Failed to communicate with Ollama
```

Solution:

```bash
ollama serve
```

---

### Streamlit Not Opening

Restart the application:

```bash
streamlit run app.py
```

---

### API Key Errors

Ensure valid API keys are entered for Gemini or OpenAI providers.

---

## Support

For issues and suggestions, contact the TravelSathi development team.

Thank you for using TravelSathi!
