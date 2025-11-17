🎓 Personalized AI Learning Tutor (AI Teaching Assistant)

An intelligent AI-powered learning tutor that explains any topic in simple words — with text + voice conversation, context memory, cloud LLM support, and a beautiful Streamlit interface.

Built using Llama-3 (OpenRouter API) + Streamlit UI + Voice Input/Output.
Fully online — no model downloads needed.

🚀 Features
🧠 Smart Learning Assistant

Explains any topic in simple words

Step-by-step learning responses

Conversation memory (keeps your last questions)

🎙️ Voice Input

Ask questions using your mic, powered by SpeechRecognition.

🔊 Voice Output

AI tutor speaks back using pyttsx3.

🌐 Cloud LLM (No local GPU needed)

Uses:

meta-llama/llama-3-8b-instruct via OpenRouter

Fully online → zero model downloads

📚 Session History

Displays your last 10 conversations.

🖥️ Beautiful Streamlit UI

Modern and clean design.

🔐 Secure with .env

API key stored safely and hidden.

🗂️ Project Structure
AI-Personalized-Tutor/
│── app.py
│── model.py
│── requirements.txt
│── .env
│── __pycache__/

🔧 Installation
1️⃣ Clone the repository
git clone https://github.com/your-username/AI-Personalized-Learning-Tutor.git
cd AI-Personalized-Learning-Tutor

2️⃣ Create a virtual environment (recommended)
python -m venv venv
venv/Scripts/activate     # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

🔑 Setup API Key
1️⃣ Get your OpenRouter API Key

Go to 👉 https://openrouter.ai/settings/keys

Create a new key → copy it.

2️⃣ Add it in backend/.env

Create: .env

Paste:  OPENROUTER_API_KEY=sk-or-v1-your-key-here

▶️ Running the Application
1️⃣ Run the frontend (Streamlit)

streamlit run app.py

2️⃣ Your app will open at:
http://localhost:8501


Now you can:

Type questions

Speak questions

Hear AI responses

Review chat history

🧪 API Model Used

meta-llama/llama-3-8b-instruct
via
https://openrouter.ai/api/v1/chat/completions

🔍 How It Works (Architecture)
🟦 Frontend (Streamlit)

Gets user input (text/voice)

Displays responses

Plays voice output

Shows conversation history

🟨 Backend (model.py)

Loads API key

Builds chat messages

Sends request to OpenRouter API

Returns model response

Handles errors, rate limits, unauthorized access

🗣️ Voice Features
🎤 Speech Recognition

Powered by:

speech_recognition + Google Speech API

🔊 Text-to-Speech

Powered by:

pyttsx3 (offline, no internet needed)

🪪 Environment Variables

Use .env.example as reference.

Variable	Description
OPENROUTER_API_KEY	Your OpenRouter API key

👨‍💻 Technologies Used

Streamlit (Frontend UI)

OpenRouter API (LLM)

Llama-3 8B (Model)

Python Requests

SpeechRecognition

pyttsx3

dotenv


📌 Future Improvements

Add PDF learning mode (upload chapter → ask AI questions)

Add video lessons generator

Add model selector (Llama 3, Gemma 2, DeepSeek)

Add dark/light mode UI

Deploy to Hugging Face Spaces for web use

🏆 Author

Chandan Kheto
💻 AI Developer
📍 India

⭐ Like This Project?

If this project helped you, please ⭐ star the repo!
It motivates further development 🙌
