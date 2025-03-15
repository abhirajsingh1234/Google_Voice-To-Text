# in this program you have to upload recordings to convert to voice and text

import gradio as gr
import speech_recognition as sr
import pyttsx3
import tempfile
import os

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Adjust speech rate

def voice_assistant(audio_file):
    """
    Processes uploaded audio file, converts speech to text, and responds with generated speech.
    """
    try:
        # Convert the uploaded audio file into recognizable speech
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data).lower()
        print("You said:", text)

        # Stop if the user says "stop"
        if text == "stop":
            response = "Goodbye!"
        else:
            response = f"You said {text}"

        # Generate a speech response and save it as a WAV file
        temp_response_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        response_audio_path = temp_response_audio.name
        temp_response_audio.close()

        engine.save_to_file(response, response_audio_path)
        engine.runAndWait()

        return response, response_audio_path

    except sr.UnknownValueError:
        return "Couldn't understand. Try again.", None
    except sr.RequestError:
        return "Network error. Check your internet connection.", None

# Gradio Interface (Upload Audio Instead of Using a Microphone)
app = gr.Interface(
    fn=voice_assistant,
    inputs=gr.Audio(type="filepath"),  # Accepts audio file instead of mic
    outputs=[gr.Textbox(), gr.Audio()],  # Outputs text + generated speech
    title="Voice-to-Voice Assistant",
    description="Upload an audio file, and the assistant will respond with text and speech.",
)

if __name__ == "__main__":
    app.launch()
