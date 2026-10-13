
from flask import Flask, render_template, request, send_file
import pyttsx3
import os

# Initialize Flask
app = Flask(__name__)

# Create output folder
OUTPUT_FOLDER = "outputs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# Display the webpage
def show_page(message="", text="", speed=160, volume=100):
    return render_template(
        "index.html",
        message=message,
        text=text,
        speed=speed,
        volume=volume
    )


# Home page
@app.route("/")
def home():
    return show_page()


# Convert text to speech
@app.route("/speak", methods=["POST"])
def speak():
    text = request.form.get("text", "").strip()

    # Validate speech settings
    try:
        speed = int(request.form.get("speed", 160))
        volume = int(request.form.get("volume", 100))
        speed = max(100, min(250, speed))
        volume = max(0, min(100, volume))
    except ValueError:
        return show_page("Invalid speed or volume.", text)

    # Check for empty text
    if not text:
        return show_page("Please enter some text.", text, speed, volume)

    # Generate speech
    engine = pyttsx3.init()
    engine.setProperty("rate", speed)
    engine.setProperty("volume", volume / 100)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

    return show_page("Speech completed!", text, speed, volume)


# Save speech as a WAV file
@app.route("/save", methods=["POST"])
def save():
    text = request.form.get("text", "").strip()

    # Validate speech settings
    try:
        speed = int(request.form.get("speed", 160))
        volume = int(request.form.get("volume", 100))
        speed = max(100, min(250, speed))
        volume = max(0, min(100, volume))
    except ValueError:
        return show_page("Invalid speed or volume.", text)

    # Check for empty text
    if not text:
        return show_page("Please enter some text.", text, speed, volume)

    # Set the audio file path
    file_path = os.path.abspath(
        os.path.join(OUTPUT_FOLDER, "voicemate.wav")
    )

    # Generate the audio file
    engine = pyttsx3.init()
    engine.setProperty("rate", speed)
    engine.setProperty("volume", volume / 100)
    engine.save_to_file(text, file_path)
    engine.runAndWait()
    engine.stop()

    # Check file creation
    if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
        return show_page(
            "Could not create the audio file.", text, speed, volume
        )

    # Download the audio file
    return send_file(
        file_path,
        as_attachment=True,
        download_name="voicemate.wav"
    )


# Start the application
if __name__ == "__main__":
    app.run(debug=True)
