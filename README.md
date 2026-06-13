# 🗺️ TravelSathi (ప్రయాణ తోడు / यात्रासाथీ)

**TravelSathi** is an AI-powered, highly localized, and multilingual cultural companion web application designed to help travelers experience and navigate the rich heritage of India. Built with **Streamlit** and Python, it integrates semantic search context via **Retrieval-Augmented Generation (RAG)** and supports both local offline AI execution and cloud-based API inference.

---

## 🏆 Hackathon 2 Checklist Compliance

Our project fulfills **all** criteria specified for the hackathon:

1. **Multilingual (i18n & l10n)**:
   - Full application localization in **English**, **Telugu (తెలుగు)**, and **Hindi (हिन्दी)**.
   - Built using a structured key-based i18n framework ([utils/i18n.py](file:///Users/tippusalma/TravelSathi/utils/i18n.py)) and JSON translation maps ([hi.json](file:///Users/tippusalma/TravelSathi/translations/hi.json), [te.json](file:///Users/tippusalma/TravelSathi/translations/te.json), [en.json](file:///Users/tippusalma/TravelSathi/translations/en.json)).
   
2. **AI-Powered Features**:
   - **AI Trip Planner**: Tailor-made day-by-day itineraries based on user interests (e.g., temples, food, history, nature).
   - **Festival Explorer**: Deep historical and cultural insights of local festivals (e.g. Bonalu, Durga Puja, Ganesh Chaturthi) in the region.
   - **Phrase Assistant**: Custom translations and romanized pronunciation guides in the target city's primary local language (e.g. Tamil for Chennai, Marathi for Mumbai, Telugu for Hyderabad).
   - **Semantic RAG Grounding**: Augments queries using localized context from our text knowledge base files.

3. **Local AI Inference (Ollama)**:
   - Built-in support to run local models (e.g., `llama3.2:1b`, `qwen2.5:1.5b`) completely offline via standard Ollama local endpoints (`http://localhost:11434`).

4. **BYOK (Bring Your Own Keys / Tokens)**:
   - Streamlined Settings panel allowing users to provide their own API tokens for cloud inference via **Gemini**, **Groq**, or **OpenRouter**.

---

## Installation

TravelSathi can be set up either using Docker (recommended) or running directly on your local system.

### Prerequisites
- Python 3.9+ (if running locally)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (if using Docker)

### 🐳 Option A: Using Docker (Recommended)
Run the application inside a Docker container without needing to configure a local Python environment.

1. **Docker Compose (Simplest)**
   Build and start the container:
   ```bash
   docker-compose up --build
   ```
   This will start the application and bind it to port `8501`.

2. **Standard Docker CLI**
   ```bash
   # Build the Docker image
   docker build -t travelsathi .

   # Run the container exposing port 8501
   docker run -p 8501:8501 travelsathi
   ```

### 🐍 Option B: Local Setup (Without Docker)
1. Clone the repository and navigate to the project directory:
   ```bash
   git clone https://code.swecha.org/Shamanth_Chowdary/TravelSathi.git
   cd TravelSathi
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### 🏃 Running the Application
1. **Docker**: Once the container is running, open your browser and navigate to:
   👉 **`http://localhost:8501`**
2. **Local**: Launch the Streamlit application:
   ```bash
   streamlit run app.py
   ```
   Open your browser and navigate to the local URL (usually `http://localhost:8501` or `http://localhost:8502`).

### ⚙️ How to Test & Evaluate
TravelSathi supports both local offline AI execution and cloud-based API inference.

1. Open the **Settings (అమరికలు)** page in the sidebar.
2. Select your language preference (**English / Telugu / Hindi**).
3. Set the **AI Provider** to **Groq**, **Gemini**, or **OpenRouter**.
4. Enter your personal API Key / token.
5. Click **Save Settings**.
6. Navigate to the **Trip Planner**, **Festival Explorer**, or **Phrase Assistant** to test full AI generation grounded with local RAG context!

*(If you are running the project completely offline on your local computer, select **Ollama** or the **Offline Mock** provider).*

---

## Contributing

We welcome contributions to TravelSathi! Please read our [CONTRIBUTING.md](file:///Users/tippusalma/TravelSathi/CONTRIBUTING.md) to learn how you can contribute, report issues, and follow our development guidelines.

By contributing to TravelSathi, you agree to maintain a respectful and collaborative environment as outlined in our [CODE_OF_CONDUCT.md](file:///Users/tippusalma/TravelSathi/CODE_OF_CONDUCT.md).
