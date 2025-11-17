
import os
import requests
from dotenv import load_dotenv

# Load environment variables from a .env file in the project root
# (Requires python-dotenv: pip install python-dotenv)
load_dotenv()

# Read the OpenRouter API key from environment variables
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Model name to send to OpenRouter (you can change this if needed)
MODEL_NAME = "meta-llama/llama-3-8b-instruct"

def ask_model(prompt: str, history=None) -> str:
    """Ask OpenRouter API with contextual memory.

    Args:
        prompt: The user prompt to send to the model.
        history: Optional list of previous messages (each message should be a dict
                 like {"role": "user"/"assistant"/"system", "content": "..."}).

    Returns:
        The assistant reply as a string, or an error message prefixed with ⚠️.
    """
    # If API key is missing, return a friendly error message immediately
    if not OPENROUTER_API_KEY:
        return "⚠️ Missing API key. Add OPENROUTER_API_KEY to your .env file."

    try:
        # OpenRouter chat completion endpoint
        url = "https://openrouter.ai/api/v1/chat/completions"

        # Request headers
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",  # required auth header
            "Content-Type": "application/json",
            # Optional metadata headers you added — fine but not required by API
            "HTTP-Referer": "https://github.com/chandan-ai-bot",
            "X-Title": "AI Voice Chatbot",
        }

        # Keep only the last 10 messages to limit payload size and token usage.
        # `history` expected to be a list of message dicts. If None, default to [].
        limited_history = (history or [])[-10:]

        # Build the messages payload:
        # - Start with a system message to set assistant behavior.
        # - Extend with limited_history (previous messages).
        # - Append current user prompt as the last message.
        messages = [
            {
                "role": "system",
                "content": "You are a friendly and helpful AI assistant that remembers context."
            }
        ]
        messages.extend(limited_history)
        messages.append({"role": "user", "content": prompt.strip()})

        # Request payload sent to OpenRouter
        payload = {
            "model": MODEL_NAME,
            "messages": messages,
            # max_tokens controls the response length. Adjust as needed.
            "max_tokens": 600,
            # temperature controls randomness. 0.7 is moderately creative.
            "temperature": 0.7,
        }

        # Send request to OpenRouter with timeout to avoid hanging requests
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()  # raise exception for HTTP errors

        # Parse JSON response
        data = response.json()

        # Typical successful response contains choices -> [ { "message": {...} } ]
        if data.get("choices") and data["choices"][0].get("message"):
            # Return the assistant's content, stripped of surrounding whitespace
            return data["choices"][0]["message"]["content"].strip()
        elif data.get("error"):
            # If API returned an error payload (structured), show the message
            return f"⚠️ API Error: {data['error'].get('message', 'Unknown error')}"
        else:
            # Unexpected response structure — helpful for debugging
            return f"⚠️ Unexpected response: {data}"

    except requests.exceptions.RequestException as e:
        # Network-related errors, timeouts, DNS issues, etc.
        return f"⚠️ Network Error: {e}"
    except Exception as e:
        # Catch-all for any other unexpected exception
        return f"⚠️ Unexpected Error: {e}"
