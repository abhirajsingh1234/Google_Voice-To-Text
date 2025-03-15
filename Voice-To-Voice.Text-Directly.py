# here you can directly speak and input will get converted to text and speech

import gradio as gr
import speech_recognition as sr
import pyttsx3
import sounddevice as sd
import numpy as np
import tempfile
import os
import wave

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Adjust speech rate

def record_audio(duration=5, samplerate=44100):
    """
    Records audio using sounddevice and saves it as a WAV file.
    """
    print("Recording... Speak now!")
    
    # Record the audio
    audio_data = sd.rec(
        int(samplerate * duration), samplerate=samplerate, channels=1, dtype=np.int16
    )
    sd.wait()  # Wait for recording to finish

    # Save as a WAV file
    temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_audio_path = temp_audio_file.name
    temp_audio_file.close()

    with wave.open(temp_audio_path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.tobytes())

    print("Recording saved:", temp_audio_path)
    return temp_audio_path

def voice_assistant():
    """
    Captures voice input, converts it to text, and responds via speech.
    """
    try:
        # Record user's speech
        audio_path = record_audio()

        # Convert speech to text
        with sr.AudioFile(audio_path) as source:
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data).lower()
        print("You said:", text)

        # Stop if user says "stop"
        if text == "stop":
            response = "Goodbye!"
        else:
            response = f"You said : {text}"

        # Generate speech response as an audio file
        temp_response_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        response_audio_path = temp_response_audio.name
        temp_response_audio.close()

        engine.save_to_file(response, response_audio_path)
        engine.runAndWait()

        return response, response_audio_path  # Text response + generated speech

    except sr.UnknownValueError:
        return "Couldn't understand. Try again.", None
    except sr.RequestError:
        return "Network error. Check your internet connection.", None

# Gradio Interface
app = gr.Interface(
    fn=voice_assistant,
    inputs=None,  # No input since it records automatically
    outputs=[gr.Textbox(), gr.Audio()],  # Outputs text + generated speech
    title="Voice-to-Voice Assistant",
    description="Click generate and speak, and the assistant will respond.",
)

if __name__ == "__main__":
    app.launch()
