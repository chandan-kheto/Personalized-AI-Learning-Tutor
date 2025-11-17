
import streamlit as st
import os, sys, threading
import speech_recognition as sr
import pyttsx3
import pythoncom

# Link backend: add your backend folder (one level up) to sys.path so we can import ask_model.
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend"))
sys.path.append(backend_path)
from model import ask_model  # your ask_model function (from previous file)

# --- Page Setup ---
st.set_page_config(
    page_title="🎓 Personalized AI Learning Tutor (Online Cloud Model)",
    page_icon="🤖",
    layout="wide"
)
st.title("🧠 Personalized AI Learning Tutor")
st.markdown("💬 Ask me any topic — I’ll teach you in simple words 👨‍🏫")

# --- State Variables (stored across Streamlit reruns) ---
# history_display: simple tuples for showing role + text in UI
# history_api: structured messages for sending to the model API
# engine: holds pyttsx3 engine instance while speaking (optional)
# speaking: boolean flag showing whether TTS is active
if "history_display" not in st.session_state:
    st.session_state.history_display = []
if "history_api" not in st.session_state:
    st.session_state.history_api = []
if "engine" not in st.session_state:
    st.session_state.engine = None
if "speaking" not in st.session_state:
    st.session_state.speaking = False

# --- Voice Engine Setup ---
def init_tts():
    """
    Initialize pyttsx3 TTS engine.
    Note: pythoncom.CoInitialize required on Windows when using COM objects on threads.
    """
    pythoncom.CoInitialize()  # ensures COM is initialized for the thread (Windows)
    # Use SAPI5 driver (Windows). On other platforms, driverName may differ or be omitted.
    engine = pyttsx3.init(driverName="sapi5")
    engine.setProperty("rate", 175)  # speech speed
    voices = engine.getProperty("voices")
    # pick second voice if available (usually female), else default to first
    engine.setProperty("voice", voices[1].id if len(voices) > 1 else voices[0].id)
    return engine

def speak_async(text):
    """
    Run TTS on a daemon thread so Streamlit UI doesn't block.
    We re-initialize the engine inside thread to avoid cross-thread COM issues.
    """
    def _speak():
        try:
            st.session_state.speaking = True
            eng = init_tts()
            st.session_state.engine = eng
            eng.say(text)         # queue text to speak
            eng.runAndWait()      # block until speaking finished
        except Exception as e:
            # Print server/log output for debugging (Streamlit will show logs)
            print("Speech error:", e)
        finally:
            # Clear flags/engine when done
            st.session_state.speaking = False
            st.session_state.engine = None

    # Start speaking in a background thread so main Streamlit thread can continue
    threading.Thread(target=_speak, daemon=True).start()

def stop_voice():
    """
    Stop current TTS if running. Use try/except because engine may be None or not responding.
    """
    try:
        if st.session_state.speaking and st.session_state.engine:
            st.session_state.engine.stop()
            st.session_state.speaking = False
    except Exception as e:
        print("Stop error:", e)

# --- UI Input ---
# text_input returns a string (empty string when nothing)
user_query = st.text_input("💭 Ask your question:")

# create 4 equal columns for action buttons
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

# --- Send Button (text) ---
with col1:
    if st.button("💬 Send Message"):
        # ensure non-empty input
        if user_query.strip():
            with st.spinner("🤖 Thinking..."):
                # call your backend model API function (synchronous)
                response = ask_model(user_query, st.session_state.history_api)

            # append conversation to the API-style history (for context)
            st.session_state.history_api.append({"role": "user", "content": user_query})
            st.session_state.history_api.append({"role": "assistant", "content": response})

            # append to display history for UI (simple tuples)
            st.session_state.history_display.append(("🧍 You", user_query))
            st.session_state.history_display.append(("🤖 AI", response))

            # speak response asynchronously
            speak_async(response)

# --- Voice Button (record from mic, convert to text, send to model) ---
with col2:
    if st.button("🎙️ Speak Now"):
        recognizer = sr.Recognizer()
        # using Microphone() will attempt to access the default recording device
        # If microphone permission is not granted or no device exists, this will raise.
        try:
            with sr.Microphone() as source:
                st.info("🎧 Listening... Speak now!")
                # listen() may block; you have timeout and phrase_time_limit set
                audio = recognizer.listen(source, timeout=8, phrase_time_limit=10)

            # recognize with Google Web Speech API (requires internet)
            query = recognizer.recognize_google(audio)
            st.success(f"✅ You said: **{query}**")

            with st.spinner("🤖 Thinking..."):
                response = ask_model(query, st.session_state.history_api)

            # maintain both API context and UI display
            st.session_state.history_api.append({"role": "user", "content": query})
            st.session_state.history_api.append({"role": "assistant", "content": response})
            st.session_state.history_display.append(("🧍 You", query))
            st.session_state.history_display.append(("🤖 AI", response))

            speak_async(response)
        except sr.WaitTimeoutError:
            st.error("⚠️ Listening timed out — no speech detected.")
        except sr.RequestError as e:
            # API was unreachable or unresponsive
            st.error(f"⚠️ Speech recognition service error: {e}")
        except sr.UnknownValueError:
            # speech was unintelligible
            st.error("⚠️ Could not understand audio.")
        except Exception as e:
            # catch-all for other errors (like Microphone not found)
            st.error(f"⚠️ Voice Input Error: {e}")

# --- Stop Voice Button ---
with col3:
    if st.button("🔇 Stop Voice"):
        stop_voice()
        st.warning("🛑 Voice stopped.")

# --- Clear Memory Button ---
with col4:
    if st.button("🧹 Clear Memory"):
        st.session_state.history_display.clear()
        st.session_state.history_api.clear()
        st.warning("🧠 Chat memory cleared!")

# --- Display History (last 10 messages) ---
st.markdown("---")
st.subheader("🗨️ Conversation History")
# show in reverse so newest appears first; limit to last 10 display entries
for role, text in reversed(st.session_state.history_display[-10:]):
    st.markdown(f"**{role}:** {text}")

st.markdown("---")
st.caption("⚡ Powered by Llama-3 • OpenRouter API • Built with ❤️ by Chandan Kheto")
