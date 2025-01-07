import speech_recognition as sr
import openai
from dotenv import load_dotenv
import os


# environment vars loaded
load_dotenv("config.env")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize the recognizer
r = sr.Recognizer()

def record():
    try:
        with sr.Microphone() as source2:
            print("Listening...")
            r.adjust_for_ambient_noise(source2, duration=0.2)  # Adjust for background noise
            audio2 = r.listen(source2)  # Capture audio input

            # Recognize speech using Google Web Speech API
            MyText = r.recognize_google(audio2)
            print(f"Recognized text: {MyText}")
            return MyText

    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None

    except sr.UnknownValueError:
        print("Could not understand the audio. Please repeat.")
        return None

def generate_output(recorded_text):
    if recorded_text:  # Check if recorded_text is not None
        with open("output.txt", "a") as f:
            f.write(recorded_text + "\n")  # Write text to the file
            print("Text written to file.")
    else:
        print("No text to write.")

while True:
    recorded_text = record()
    if recorded_text:  # Ensure valid input before writing
        generate_output(recorded_text)
    else:
        print("No valid text recorded. Please repeat.")
