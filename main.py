import os
import requests
from flask import Flask, render_template, request, Response
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

app = Flask(__name__)

# Retrieve the API key from environment variables
DEEPINFRA_API_KEY = os.getenv("DEEPINFRA_API_KEY")
API_URL = "https://api.deepinfra.com/v1/openai/audio/speech"

@app.route('/')
def index():
    """
    Renders the main page of the application.
    """
    return render_template('index.html')

@app.route('/synthesize', methods=['POST'])
def synthesize():
    """
    Handles the text-to-speech synthesis request.
    """
    if not DEEPINFRA_API_KEY or DEEPINFRA_API_KEY == 'your_deepinfra_api_key_here':
        return Response("Error: DEEPINFRA_API_KEY not configured.", status=500, mimetype='text/plain')

    try:
        # Get text from the POST request form data
        text_to_synthesize = request.form.get('text')
        if not text_to_synthesize:
            return Response("Error: No text provided for synthesis.", status=400, mimetype='text/plain')

        # Set up the headers for the DeepInfra API request
        headers = {
            "Authorization": f"Bearer {DEEPINFRA_API_KEY}",
            "Content-Type": "application/json",
        }

        # Set up the payload in the OpenAI-compatible format
        payload = {
            "model": "hexgrad/kokoro-tts",
            "input": text_to_synthesize,
            "voice": "kokoro"
        }

        # Make the POST request to the DeepInfra API
        response = requests.post(API_URL, headers=headers, json=payload)

        # Check if the request was successful
        response.raise_for_status()

        # Return the audio data with the correct MIME type
        return Response(response.content, mimetype="audio/mpeg")

    except requests.exceptions.RequestException as e:
        # Handle potential network errors or API errors
        error_message = f"API request failed: {e}"
        # Log the error for debugging
        print(error_message)
        # Return a generic error message to the user
        return Response(f"Error synthesizing audio. Please check the server logs. Status code: {e.response.status_code if e.response else 'N/A'}", status=500, mimetype='text/plain')
    except Exception as e:
        # Handle other unexpected errors
        print(f"An unexpected error occurred: {e}")
        return Response("An unexpected error occurred.", status=500, mimetype='text/plain')

if __name__ == '__main__':
    # Runs the Flask application
    app.run(debug=True)
