# AGENTS.md

# TravelSathi Agent Documentation

## Overview

TravelSathi is an AI-powered travel planning assistant that combines Retrieval-Augmented Generation (RAG), offline large language models, and multilingual support to generate personalized travel guidance.

This document describes the intelligent components ("agents") used within the system.

---

# 1. Travel Planning Agent

## Purpose

Generates destination-specific travel responses based on user queries.

## Responsibilities

* Understand user travel questions.
* Generate travel recommendations.
* Create itinerary suggestions.
* Explain cultural information.
* Provide destination insights.

## Inputs

* User query
* Destination city
* Selected language
* AI provider

## Outputs

* Travel recommendations
* Detailed explanations
* Budget suggestions

---

# 2. RAG Retrieval Agent

## Purpose

Retrieves relevant knowledge from TravelSathi's local knowledge base.

## Responsibilities

* Search destination documents.
* Retrieve context chunks.
* Rank relevant information.
* Supply retrieved context to the LLM.

## Technologies

* FAISS
* Sentence Transformers
* TF-IDF fallback retrieval

## Supported Destinations

* Hyderabad
* Jaipur
* Varanasi

---

# 3. Ollama Agent

## Purpose

Provides fully offline AI functionality.

## Responsibilities

* Execute local language models.
* Process prompts without internet.
* Return JSON-formatted responses.

## Supported Models

* qwen2.5:1.5b
* llama3.2:1b

---

# 4. Cloud Provider Agent

## Purpose

Enables responses using cloud-based AI providers.

## Supported Providers

### OpenAI

* Model: GPT-4o-mini

### Gemini

* Model: Gemini 1.5 Flash

## Responsibilities

* Validate API keys.
* Route prompts to providers.
* Return structured responses.

---

# 5. Budget Estimation Agent

## Purpose

Provides approximate travel costs.

## Categories

* Food
* Transportation
* Entry Tickets

## Output

Estimated costs in Indian Rupees (INR).

---

# 6. Language Support Agent

## Purpose

Provides multilingual assistance.

## Responsibilities

* Translate responses.
* Generate local phrases.
* Improve tourist communication.

---

# Agent Collaboration Flow

User Query
↓
RAG Retrieval Agent
↓
Provider Selection
↓
(Ollama / OpenAI / Gemini)
↓
Travel Planning Agent
↓
Budget Estimation Agent
↓
Language Support Agent
↓
Final Structured Response

---

# Future Agents

Potential future enhancements include:

* Hotel Recommendation Agent
* Real-Time Weather Agent
* Safety Advisory Agent
* Transportation Booking Agent
* Emergency Assistance Agent

---

TravelSathi was developed as part of the Swecha Hackathon.
