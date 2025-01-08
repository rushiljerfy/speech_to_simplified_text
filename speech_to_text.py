import os
from openai import OpenAI
import speech_recognition as sr
from dotenv import load_dotenv

# Load environment variables (e.g., OpenAI API key)
load_dotenv("config.env")

# Initialize the OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")  # Load the API key from the environment
)

# Initialize the recognizer
r = sr.Recognizer()

# Function to record speech
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

# Function to save output to a file
def generate_output(recorded_text):
    if recorded_text:  # Check if recorded_text is not None
        with open("output.txt", "a") as f:
            f.write(recorded_text + "\n")  # Write text to the file
            print("Text written to file.")
    else:
        print("No text to write.")

# Function to simplify text using OpenAI API
def simplify_text(text):
    try:
        print("Simplifying text...")
        # Call the OpenAI API with the correct method
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that simplifies text."
                },
                {
                    "role": "user",
                    "content": f"Simplify this text: {text}"
                }
            ],
            model="gpt-4",  # Replace with "gpt-3.5-turbo" if GPT-4 is unavailable
        )
        # Extract the simplified text
        #simplified_text = response["choices"][0]["message"]["content"].strip()
        simplified_text = response.choices[0].message.content.strip()
        print(f"Simplified text: {simplified_text}")
        return simplified_text
    except Exception as e:
        print(f"Error simplifying text: {e}")
        return None

# Main program
try:
    while True:
        recorded_text = record()  # Record speech
        if recorded_text:
            simplified_text = simplify_text(recorded_text)  # Simplify the recorded text
            if simplified_text:
                generate_output(simplified_text)  # Save simplified text to file
                print("Generated simplified text")
        else:
            print("No valid text recorded. Please repeat.")
except KeyboardInterrupt:
    print("\nExiting program. Goodbye!")
