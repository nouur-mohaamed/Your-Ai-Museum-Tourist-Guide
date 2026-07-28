> 🏆 This repository is my official submission for the [ **Tips Hindawi** ](https://www.tipshindawi.com/) **Challenge (June–July) 2026**.

## 👤 Participant

| Field            | Value                                |
| ---------------- | ------------------------------------ |
| Full Name        |  Nour Mohammed said                                    |
| Project Name     |  Your AI museum tourist guide                                    |
| GitHub Username  |  nouur-mohaamed                                   |
| Challenge Batch  | June–July 2026                       |
| Training Program | Large Language Models (LLMs) Program |
| Organization     | [**Edrak for Ai**](https://edrak4ai.com/en)                         |

---

# 📖 Project Overview

AI Museum Tourist Guide is an intelligent museum assistant that allows visitors to upload or capture an image of an artifact and receive an interactive, story-driven explanation about it. The application combines computer vision, Retrieval-Augmented Generation (RAG), multilingual translation, and speech synthesis to create a personalized museum experience.

The system begins by accepting an uploaded image or a live camera capture. The image is converted into an embedding using a vision model, then matched against a ChromaDB image database to identify the artifact through similarity search.

Once the artifact is identified, the application retrieves relevant information from a dedicated knowledge base built from historical PDF documents. Each artifact has its own FAISS vector database, created by extracting text from PDFs, splitting the content into chunks, and embedding them using the **sentence-transformers/all-MiniLM-L6-v2** model. This Retrieval-Augmented Generation (RAG) pipeline ensures that responses are grounded in the provided historical sources.

After retrieving the relevant context, the application uses a custom Large Language Model integrated with LangChain to generate a complete museum-style narrative describing the artifact in a natural storytelling format. Additional LangChain output parsing extracts structured information such as the artifact's museum location and historical lifespan for separate display.

The generated explanation can be automatically translated into multiple languages (English, French, and Spanish), allowing visitors to interact with the guide in their preferred language. The translated story is then converted into speech, producing an audio tour that users can listen to while viewing the artifact.

Beyond the initial explanation, the application provides an interactive chatbot where visitors can ask follow-up questions about the identified artifact. For every question, the system retrieves the most relevant historical context from the artifact's vector database before generating an answer, ensuring accurate and context-aware responses instead of relying solely on the language model's internal knowledge.

The user interface is built with Streamlit and includes image upload, live camera capture, artifact analysis, multilingual support, audio playback, and a conversational chat interface. The application also features a custom museum-inspired theme with a black-and-gold design that enhances the visitor experience.



---

# ✨ Features

- Upload an image of a museum artifact.
- Capture an artifact image directly using the device camera.
- Automatically identify artifacts using computer vision and image similarity search.
- Generate detailed, story-driven descriptions of identified artifacts.
- Retrieve information from historical PDF documents using Retrieval-Augmented Generation (RAG).
- Display key artifact information, including museum location and historical lifespan.
- Ask follow-up questions through an interactive AI chatbot.
- Generate context-aware answers grounded in the retrieved historical documents.
- Support multiple languages (English, French, and Spanish).
- Translate both artifact descriptions and chatbot responses.
- Generate natural-sounding audio guides using text-to-speech.
- Preserve conversation history during the museum tour.
- Automatically reset the session when a new artifact is analyzed.
- Provide a responsive, museum-themed user interface built with Streamlit.

---

# 🛠️ Technologies Used

- **Python**
- **Streamlit** – Web application framework
- **LangChain** – LLM orchestration, prompt engineering, and structured output parsing
- **Retrieval-Augmented Generation (RAG)** – Context-aware response generation
- **FAISS** – Document vector database for semantic search
- **ChromaDB** – Image embedding storage and similarity search
- **Meta DINOv2** – Computer vision model for image embeddings and artifact recognition
- **Sentence Transformers (all-MiniLM-L6-v2)** – Document embedding model
- **PyPDF** – PDF text extraction
- **Custom LLM API** – Story generation and question answering
- **Machine Translation API** – Multilingual support
- **Text-to-Speech (TTS) API** – Audio guide generation
- **REST APIs** – Communication between the frontend and AI services
- **Kaggle** – AI model hosting and inference
- **ngrok** – Secure HTTPS tunnel for exposing the Kaggle inference server
- **NumPy** – Numerical computations
- **Pillow (PIL)** – Image processing
- **Requests** – HTTP communication with backend services
- **python-dotenv** – Environment variable management

---

# ⚙️ Installation and Usage

Follow the steps below to run the AI Museum Tourist Guide locally.

## Prerequisites

Before starting, make sure you have:

* Python 3.10 or later installed.
* A Git client.
* A Kaggle account.
* An ngrok account.

---

## 1. Clone the Repository

```bash
git clone https://github.com/nouur-mohaamed/Your-Ai-Museum-Tourist-Guide.git
cd Your-Ai-Museum-Tourist-Guide
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

---

## 4. Configure the Streamlit Application

Create a `.env` file in the project root.

```env
SECRET=your_secret_key
```

Choose any secure value for `SECRET`.

**Important:** This value **must be identical** to the `SECRET` configured in the Kaggle AI server.

---

# Running the AI Server

The AI models are hosted separately inside a Kaggle Notebook.

## 1. Open the Kaggle Notebook

Open the notebook that contains the AI server.

---

## 2. Enable Internet Access

From the notebook settings, enable **Internet**.

This is required so ngrok can expose the server to the internet.

---

## 3. Add Kaggle Secrets

Open:

**Add-ons → Secrets**

Create the following secrets:

| Secret      | Description                                                |
| ----------- | ---------------------------------------------------------- |
| `SECRET`    | Same value used in the Streamlit application's `.env` file |
| `NGROK_API` | Your ngrok authentication token                            |

You can obtain your ngrok authentication token from your ngrok dashboard.

---

## 4. Start the AI Server

Run all notebook cells.

The notebook will:

* Load all AI models.
* Start the API server.
* Create a secure HTTPS tunnel using ngrok.

When the server starts successfully, it will display a public ngrok URL similar to:

```
https://xxxxxxxx.ngrok-free.app
```

Copy this URL.

---

## 5. Update the API Endpoints

Replace the existing ngrok URL in the following files with your newly generated URL:

* `get_image_embedding.py`
* `generate_response.py`
* `generate_translation.py`
* `generate_speech.py`

For example:

```python
URL = "https://xxxxxxxx.ngrok-free.app/generate"
```

> **Note:** ngrok generates a new public URL every time the Kaggle notebook is restarted. If this happens, simply update the API URLs with the new address.

---

# Running the Streamlit Application

After the AI server is running, start the frontend:

```bash
streamlit run main.py
```

The application will be available at:

```
http://localhost:8501
```

Open this address in your web browser to begin using the AI Museum Tourist Guide.

---

# Usage

1. Start the Kaggle AI server.
2. Copy the generated ngrok URL.
3. Update the API URLs in the Streamlit project.
4. Launch the Streamlit application.
5. Upload an artifact image or capture one using your camera.
6. Wait while the artifact is identified.
7. Read or listen to the generated museum guide.
8. Ask follow-up questions through the AI chatbot.
9. Translate responses into a supported language if desired.


# 📸 Demo



---

# 📈 Results

* Built an end-to-end AI-powered museum guide integrating computer vision, RAG, translation, and text-to-speech.
* Implemented artifact recognition using **Meta DINOv2** and **ChromaDB**.
* Developed a context-aware RAG pipeline with **FAISS** and historical PDF documents.
* Integrated an LLM with **LangChain** for story generation and interactive question answering.
* Enabled multilingual support and AI-generated audio guides.
* Designed a scalable client-server architecture using **Streamlit**, **Kaggle**, and **ngrok**.


---

# 🔮 Future Improvements

* 1. Add **QR codes** beside each museum artifact as a backup to image recognition. Scanning a QR code would instantly identify the artifact, display its AI-generated story, and allow visitors to ask follow-up questions without taking a photo.
* 2. Upgrade to a more powerful **Large Language Model** to provide more accurate, detailed, and natural conversations, enabling the AI to answer both artifact-specific and broader historical questions like a real museum guide.
* 3. Introduce **Guided Tour** mode, allowing visitors to follow predefined museum routes, such as exploring artifacts in chronological order or by historical era.
* 4. Add a **Solo Exploration** mode, enabling visitors to navigate the museum freely and interact with the AI guide for each artifact at their own pace.

---

# 📚 About the Challenge

This project was developed as part of the [**Tips Hindawi**](https://www.tipshindawi.com/) **Challenge (June–July) 2026**.

[Tips Hindawi](https://www.tipshindawi.com/) is the internships department of [**Edrak for Ai**](https://edrak4ai.com/en), and the challenge encourages participants to build real-world projects, apply practical skills, and showcase their work through GitHub.

For more information about the challenge, training programs, and upcoming batches, visit the official [Tips Hindawi](https://www.tipshindawi.com/) website.

---

# 📄 License

This project is shared for educational and portfolio purposes.
