# TravelSathi

TravelSathi is an AI-powered travel planning assistant designed to help users generate personalized itineraries for destinations across India. The application supports offline AI using Ollama, multilingual assistance, Retrieval-Augmented Generation (RAG), and budget-aware recommendations.

---

## Features

* 🗺️ AI-generated travel itineraries
* 💰 Budget-aware trip planning
* 🌐 Multilingual travel phrases
* 🤖 Offline AI support using Ollama
* 📚 Retrieval-Augmented Generation (RAG)
* 🏛️ Destination-specific knowledge base
* 🧳 Custom travel styles and interests
* 🖥️ Interactive Streamlit interface
* 🐳 Docker support for containerized deployment

---

## Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### AI & NLP

* Ollama
* Qwen / Llama models
* Sentence Transformers
* FAISS

### Data Processing

* Pandas
* NumPy
* Scikit-learn

### Containerization

* Docker
* Docker Compose

---

## Project Structure

```
TravelSathi/
├── backend/
├── frontend/
├── rag/
├── data/
├── translations/
├── utils/
├── app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── tests/
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd TravelSathi
```

### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running Locally

Start Ollama:

```bash
ollama serve
```

Run Streamlit:

```bash
streamlit run app.py
```

Open:

```
http://localhost:8501
```

---

## Running with Docker

```bash
docker-compose up --build
```

---

## Supported Destinations

* Hyderabad
* Jaipur
* Varanasi

Additional destinations can be added by extending the RAG knowledge base.

---

## Team

Developed as part of the Swecha Hackathon.

Project: TravelSathi

---

## License

This project is licensed under the GNU Affero General Public License v3.0 (AGPLv3).
