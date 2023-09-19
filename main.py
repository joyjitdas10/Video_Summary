import tkinter as tk
from tkinter import filedialog
import os
import moviepy.editor as mp
import moviepy.audio.fx.all as afx
import speech_recognition as sr

def browse_and_convert():
    video_file_path = filedialog.askopenfilename(
        filetypes=[("Video Files", "*.mp4 *.avi *.mkv")]
    )
    if video_file_path:
        # Extract the filename from the full path
        filename = os.path.basename(video_file_path)

        # Define the output WAV file name (same as the video file with .wav extension)
        wav_file_path = os.path.splitext(filename)[0] + ".wav"

        # Convert the video's audio to a WAV file (PCM format)
        video = mp.VideoFileClip(video_file_path)
        audio = video.audio.fx(afx.audio_normalize)
        audio.write_audiofile(wav_file_path)

        file_label.config(text="Conversion successful.")

        # Convert the WAV file to English text
        text = convert_wav_to_text(wav_file_path, language="en-US")
        text_label.config(text="English Text from WAV:\n" + text)

        # Automatically save the converted text to a file with the same name as the video
        text_filename = os.path.splitext(filename)[0] + "_english.txt"
        try:
            with open(text_filename, "w", encoding="utf-8") as text_file:
                text_file.write(text)
            save_label.config(text="Text saved to: " + text_filename)
        except Exception as e:
            save_label.config(text="Error saving text: " + str(e))

def convert_wav_to_text(wav_file, language="en-US"):
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_file) as source:
        audio = recognizer.record(source)  # Read the entire audio file
    try:
        text = recognizer.recognize_google(audio, language=language)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return "Error with the request: {0}".format(e)

# Create the main window
root = tk.Tk()
root.title("Video to English Text Converter")

# Set the window size to 700x700 pixels
root.geometry("700x700")

# Create a label to display conversion status
file_label = tk.Label(root, text="")
file_label.pack(pady=10)

# Create a button to trigger the file dialog for video files and conversion
convert_button = tk.Button(root, text="Convert Video to English Text", command=browse_and_convert)
convert_button.pack()

# Create a label to display the converted English text
text_label = tk.Label(root, text="")
text_label.pack()

# Create a label to display save status
save_label = tk.Label(root, text="")
save_label.pack()

# Run the Tkinter main loop
root.mainloop()
