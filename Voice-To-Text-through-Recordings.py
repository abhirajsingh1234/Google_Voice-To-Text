import gradio as gr
import speech_recognition as sr
import pyttsx3
import tempfile
import os

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speech rate

def voice_assistant(audio):
    """
    Processes voice input, converts it to text, and responds via speech.
    """
    try:
        with sr.AudioFile(audio) as source:
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data).lower()
        print("You said:", text)

        # Stop if user says "stop"
        if text == "stop":
            response = "Goodbye!"
        else:
            response = f"You said {text}"

        # Generate speech response as an audio file
        temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_audio_path = temp_audio_file.name
        temp_audio_file.close()  # Close so pyttsx3 can write to it

        engine.save_to_file(response, temp_audio_path)
        engine.runAndWait()

        return response# Text response

    except sr.UnknownValueError:
        return "Couldn't understand. Try again.", None
    except sr.RequestError:
        return "Network error. Check your internet connection.", None

# Gradio Interface
app = gr.Interface(
    fn=voice_assistant,
    inputs=gr.Audio(type="filepath"),
    outputs=gr.Textbox(),  # Output: text + generated speech
    title="Voice-to-Voice Assistant",
    description="Speak into the microphone, and the assistant will respond.",
)

if __name__ == "__main__":
    app.launch()
