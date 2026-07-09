# 🎙️ AI Voice Assistant

An end-to-end AI-powered voice assistant built with **Python, OpenAI Whisper, GPT-4o mini, OpenAI Text-to-Speech, and Streamlit**.

The application allows users to record voice messages directly from their browser, converts speech into text using Whisper, generates intelligent contextual responses with GPT-4o mini, converts those responses back into natural speech, and maintains conversation memory throughout the chat session.

🌐 **Live Demo:** https://voiceassistwiq.streamlit.app/

---

## 📌 Overview

Modern AI assistants combine multiple artificial intelligence technologies to enable natural human-computer interaction.

This project implements a complete voice-based conversational pipeline:

```text
Browser Microphone
        ↓
   Audio Recording
        ↓
  Speech-to-Text
  OpenAI Whisper
        ↓
 Conversation Memory
        ↓
    GPT-4o mini
        ↓
   AI Response
        ↓
  Text-to-Speech
        ↓
 Browser Audio Playback
```

The assistant supports multi-turn conversations, allowing the AI to remember previous messages within the current session and answer follow-up questions contextually.

---

## ✨ Features

- 🎤 **Browser-Based Voice Recording** — Record voice messages directly through the browser using Streamlit's native audio input.
- 🧠 **Speech-to-Text with Whisper** — Transcribe spoken audio using OpenAI Whisper.
- 🤖 **GPT-4o mini Integration** — Generate intelligent and conversational AI responses.
- 💬 **Conversation Memory** — Maintain multi-turn conversational context throughout the current session.
- 🔊 **AI Text-to-Speech** — Convert generated responses into natural spoken audio.
- ▶️ **Browser Audio Playback** — Play AI-generated speech directly in the web interface.
- 📜 **Full Chat History** — Display all user and assistant messages in a conversational interface.
- 🗑️ **Clear Conversation** — Reset both frontend chat history and backend LLM memory.
- 🚫 **Duplicate Audio Protection** — Prevent the same browser recording from being processed repeatedly using SHA-256 hashing.
- 🔇 **Silence Detection** — Gracefully handle recordings where no speech is detected.
- ⚠️ **Error Handling** — Handle transcription failures, API errors, empty recordings, and other pipeline exceptions.
- 🔐 **Secure API Key Management** — Keep API credentials outside source control using environment variables and Streamlit Secrets.
- ☁️ **Cloud Deployment** — Fully deployed using Streamlit Community Cloud.
- 🖥️ **Local and Web Architecture** — Separate local desktop audio functionality from browser-based deployment logic.

---

## 🚀 Live Demo

Try the deployed application here:

**https://voiceassistwiq.streamlit.app/**

### How to use

1. Open the live application.
2. Allow microphone access when prompted by your browser.
3. Click the microphone recorder.
4. Speak your question or message.
5. Stop the recording.
6. Wait while the assistant:
   - transcribes your voice,
   - processes the conversation,
   - generates an AI response,
   - and creates spoken audio.
7. Read the response and listen to the generated speech.
8. Continue recording new messages for a contextual multi-turn conversation.
9. Use **Clear Chat** to reset the entire conversation.

---

## 🧠 System Architecture

The application follows a modular architecture where each component has a single responsibility.

```text
┌───────────────────────────────┐
│       Browser Microphone      │
│       Streamlit Audio Input   │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       Temporary WAV File      │
│     Browser Audio Storage     │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│      Speech-to-Text Layer     │
│       OpenAI Whisper          │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│      Conversation Memory      │
│  User + Assistant Messages    │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│          LLM Layer            │
│        GPT-4o mini            │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│      Text-to-Speech Layer     │
│         OpenAI TTS            │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│      Browser Audio Player     │
│        Streamlit Audio        │
└───────────────────────────────┘
```

---

## 🔄 Application Workflow

The complete processing workflow is:

1. The user records a voice message through the browser.
2. Streamlit receives the recorded audio.
3. The application generates a SHA-256 hash of the audio to prevent duplicate processing.
4. The audio is temporarily saved as a WAV file.
5. Whisper converts the speech into text.
6. The application validates that meaningful speech was detected.
7. The user's message is added to conversation memory.
8. The complete conversation context is sent to GPT-4o mini.
9. GPT generates a contextual response.
10. The assistant response is added to conversation memory.
11. OpenAI TTS converts the response into speech.
12. The generated MP3 is read as audio bytes.
13. The user and assistant messages are stored in Streamlit session state.
14. The complete conversation history is rendered in the browser.
15. The AI-generated speech is played through the browser audio player.

---

## 🗂️ Project Structure

```text
AI-Voice-Assistant/
│
├── app.py
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── services/
│   ├── __init__.py
│   ├── assistant.py
│   ├── local_assistant.py
│   └── memory.py
│
├── stt/
│   ├── __init__.py
│   └── speech_to_text.py
│
├── llm/
│   ├── __init__.py
│   └── llm_client.py
│
├── tts/
│   ├── __init__.py
│   └── text_to_speech.py
│
├── audio/
│   ├── __init__.py
│   ├── recorder.py
│   ├── player.py
│   └── temp/
│
├── utils/
│   ├── __init__.py
│   ├── helpers.py
│   └── prompts.py
│
├── requirements.txt
├── packages.txt
├── .gitignore
└── README.md
```

> The exact structure may vary slightly depending on the local-only modules retained in the repository.

---

## 🧩 Module Responsibilities

### `app.py`

The main Streamlit web application responsible for:

- Browser microphone input
- Streamlit session state
- Audio duplicate detection
- Calling the AI assistant pipeline
- Displaying conversation history
- Browser audio playback
- Clear-chat functionality
- User-facing error messages

### `services/assistant.py`

The central orchestration layer connecting:

```text
Audio
  ↓
Speech-to-Text
  ↓
Conversation Memory
  ↓
LLM
  ↓
Text-to-Speech
```

This service is platform-independent and accepts an existing audio file instead of directly controlling a microphone or speaker.

### `services/local_assistant.py`

Provides optional local desktop functionality by combining:

- Local microphone recording
- Core AI assistant pipeline
- Local speaker playback

This separation prevents browser deployment from depending directly on local hardware-specific behavior.

### `services/memory.py`

Manages multi-turn conversation context by:

- storing user messages,
- storing assistant responses,
- returning complete message history to the LLM,
- and resetting memory when the user clears the conversation.

### `stt/speech_to_text.py`

Loads the Whisper model and converts recorded speech into text.

The implementation supports device selection such as:

```python
device = "cuda" if torch.cuda.is_available() else "cpu"
```

This allows GPU acceleration locally when CUDA is available while falling back to CPU in cloud environments.

### `llm/llm_client.py`

Communicates with the OpenAI Responses API and uses **GPT-4o mini** to generate contextual responses based on conversation history.

### `tts/text_to_speech.py`

Converts AI-generated text responses into spoken MP3 audio using OpenAI's Text-to-Speech API.

### `utils/prompts.py`

Contains the system prompt that defines the assistant's default behavior and conversational style.

### `config/settings.py`

Centralizes application configuration, including:

- API credentials
- Model names
- Whisper configuration
- Temporary audio paths
- Recording settings
- TTS settings

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application and browser UI |
| OpenAI Whisper | Speech-to-Text transcription |
| GPT-4o mini | Intelligent conversational responses |
| OpenAI TTS | Text-to-Speech generation |
| PyTorch | Whisper model execution |
| FFmpeg | Audio processing support |
| python-dotenv | Local environment variable management |
| SHA-256 | Duplicate audio detection |
| Git & GitHub | Version control and source hosting |
| Streamlit Community Cloud | Application deployment |

---

## ⚙️ Installation and Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/wasidkhan7/Ai-voice-Assitant.git
cd Ai-voice-Assitant
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install Python dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install FFmpeg

On Ubuntu/Debian:

```bash
sudo apt update
sudo apt install ffmpeg
```

On macOS with Homebrew:

```bash
brew install ffmpeg
```

For Windows, install FFmpeg and ensure it is available through the system `PATH`.

### 5. Configure environment variables

Create a `.env` file in the project root:

```text
OPENAI_API_KEY=your_openai_api_key_here
```

Never commit `.env` to GitHub.

Your `.gitignore` should include:

```gitignore
.env
.venv/
__pycache__/
*.pyc
audio/temp/*.wav
audio/temp/*.mp3
```

### 6. Run the application

```bash
streamlit run app.py
```

Then open the local URL shown in your terminal, typically:

```text
http://localhost:8501
```

---

## 🔐 Environment Variables and Security

The project uses environment variables to protect sensitive API credentials.

Required variable:

```text
OPENAI_API_KEY
```

For local development, store the key in `.env`.

For Streamlit Community Cloud, add it through the application's **Secrets** configuration:

```toml
OPENAI_API_KEY = "your_openai_api_key_here"
```

The API key must never be hardcoded into Python files or committed to source control.

---

## ☁️ Streamlit Cloud Deployment

The application is deployed on Streamlit Community Cloud.

Deployment configuration:

```text
Repository: wasidkhan7/Ai-voice-Assitant
Branch: main
Main file: app.py
```

The deployment uses:

### `requirements.txt`

For Python dependencies.

### `packages.txt`

For system-level packages required by the application:

```text
ffmpeg
```

### Streamlit Secrets

The OpenAI API key is securely configured through Streamlit's secret management system.

---

## 💬 Conversation Memory

The assistant maintains contextual conversation history during the current session.

Example:

```text
User:
The capital of Pakistan is Islamabad, right?

Assistant:
Yes, Islamabad is the capital of Pakistan.

User:
Who is the prime minister of it?

Assistant:
The assistant understands that "it" refers to Pakistan.
```

Each conversation stores messages in the following conceptual format:

```python
{
    "role": "user",
    "content": "Hello"
}
```

and:

```python
{
    "role": "assistant",
    "content": "Hi! How can I help you?"
}
```

The full conversation history is provided to the LLM so that follow-up questions can be interpreted contextually.

The **Clear Chat** feature resets both:

- Streamlit UI chat history
- Backend LLM conversation memory

---

## 🎤 Browser Audio Input

The web version uses Streamlit's native browser audio recording functionality.

This is important because libraries such as `sounddevice` access the microphone of the machine running Python. In cloud deployment, that machine is the remote server rather than the user's device.

The deployed architecture instead uses:

```text
User's Browser Microphone
          ↓
   Streamlit Audio Input
          ↓
       Web Server
```

This allows visitors to use their own microphone from any supported browser.

---

## 🔊 Browser Audio Playback

The AI-generated speech is stored as audio bytes and rendered directly in the browser.

Each assistant message can contain:

```python
{
    "role": "assistant",
    "content": assistant_text,
    "audio": response_audio_bytes,
}
```

This prevents older chat messages from pointing to the same overwritten temporary MP3 file and ensures that each response retains its own corresponding speech output during the session.

---

## 🚫 Duplicate Audio Protection

Streamlit reruns the Python script whenever application state changes.

Without protection, the same recorded audio could accidentally be processed multiple times.

The application solves this by calculating a SHA-256 hash:

```python
audio_hash = hashlib.sha256(audio_bytes).hexdigest()
```

The hash is compared with the previously processed recording:

```python
if audio_hash != st.session_state.last_audio_hash:
```

This ensures that each unique recording is processed only once.

---

## ⚠️ Error Handling

The application handles several common failure scenarios.

### No speech detected

If Whisper returns empty text:

```text
No speech could be detected in the audio.
```

The application shows a user-friendly warning instead of crashing.

### API or pipeline failure

Unexpected failures are logged internally while the user receives a readable error message:

```text
Something went wrong while processing your voice. Please try again.
```

### Duplicate recordings

Previously processed recordings are ignored using audio hashing.

---

## 🧪 Example Interaction

```text
User:
Hello, what is the capital of Pakistan?

Assistant:
The capital of Pakistan is Islamabad.

User:
Can you tell me something interesting about it?

Assistant:
Certainly! Islamabad is known for its greenery, planned architecture,
and its location at the foothills of the Margalla Hills.
```

The second question is understood contextually because conversation memory retains the previous exchange.

---

## 📊 Evaluation Criteria

The project can be evaluated across the following areas:

- Speech recognition accuracy
- AI response quality
- Conversation-context retention
- Text-to-speech clarity
- End-to-end response latency
- Error handling
- User-interface usability
- Code modularity
- Browser compatibility
- Cloud deployment reliability

---

## 🚧 Current Limitations

- Whisper transcription accuracy may decrease with background noise, unclear pronunciation, or very short speech.
- The Whisper `base` model can require noticeable CPU processing time on free cloud infrastructure.
- LLM responses should not be assumed to contain real-time information unless a live search or external data source is integrated.
- Conversation memory currently lasts only for the active application session and is not persisted to a database.
- API usage may incur costs depending on the OpenAI account and selected models.
- The application requires an internet connection for OpenAI LLM and TTS requests.

---

## 🔮 Future Improvements

Potential future enhancements include:

- 🌐 Real-time web search for current information
- ⚡ Streaming LLM responses
- 🎙️ Real-time speech streaming
- 🔔 Wake-word detection such as `"Hey Assistant"`
- 💾 Persistent conversation storage using PostgreSQL or SQLite
- 👤 User authentication
- 🌍 Multilingual conversation support
- 🧠 Long-term semantic memory using a vector database
- 📱 Mobile-responsive UI improvements
- 🗣️ Multiple selectable AI voices
- 📊 Response latency and token analytics
- 📥 Conversation export
- 🐳 Docker containerization
- 🧪 Automated unit and integration tests

---

## 🎯 Learning Outcomes

This project demonstrates practical experience with:

- Building end-to-end AI applications
- Speech-to-Text systems
- Large Language Model API integration
- Text-to-Speech generation
- Conversation memory management
- Modular Python architecture
- Browser audio processing
- Streamlit session-state management
- Secure API-key handling
- Exception handling and logging
- Git and GitHub workflows
- Cloud deployment

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

To contribute:

1. Fork the repository.
2. Create a new feature branch.
3. Make your changes.
4. Commit your work.
5. Push the branch.
6. Open a pull request.

---

## 📄 License

This project is intended for educational, portfolio, and demonstration purposes.

If you plan to make the project openly reusable, consider adding an MIT License to the repository.

---

## 👨‍💻 Author

**Wasid Khan**

AI / Machine Learning and Data Science enthusiast focused on building practical applications using machine learning, deep learning, NLP, LLMs, RAG, and modern AI engineering tools.

---

## ⭐ Support

If you find this project useful, consider giving the repository a star.

**Live Application:** https://voiceassistwiq.streamlit.app/

**GitHub Repository:** https://github.com/wasidkhan7/Ai-voice-Assitant
