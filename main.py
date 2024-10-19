import tkinter
import customtkinter
from pytubefix import YouTube
import re
import os
import subprocess
import time


def is_valid_youtube_url(url):
    # Regular expression to validate YouTube URL
    youtube_regex = re.compile(r'(https?://)?(www\.)?(youtube)\.(com|be)/.+')
    return youtube_regex.match(url)

def create_download_directory(folder):
    download_path = os.path.join(os.getcwd(), folder)
    os.makedirs(download_path, exist_ok=True)
    return download_path

def get_unique_filename(directory, filename):
    base, extension = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base} ({counter}){extension}"
        counter += 1
    return new_filename

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    
    # Update the percentage label
    pPercentage.configure(text=f"{percentage:.2f}%")
    pPercentage.update()
    
    # Update the progress bar (value should be between 0 and 1)
    progressBar.set(bytes_downloaded / total_size)

def merge_video_audio(video_path, audio_path, output_path):
    ffmpeg_path = r'E:\bin\ffmpeg.exe'

    # Merge video and audio using ffmpeg
    ffmpeg_command = [
        ffmpeg_path, '-i', video_path, '-i', audio_path, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', output_path
    ]
    subprocess.run(ffmpeg_command, check=True)

    # Delete video and audio files
    os.remove(video_path)
    os.remove(audio_path)

def startDownload():
    url = link.get()
    print(f"URL entered: {url}\n")  # Log the URL entered
    if not is_valid_youtube_url(url):
        finish.configure(text="Invalid YouTube URL")
        return

    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        
        # Get the highest resolution video stream
        video_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True).order_by('resolution').desc().first()
        
        # Get the highest quality audio stream
        audio_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_audio=True).order_by('abr').desc().first()

        download_video_path = create_download_directory("videos")  # Create directory and get path
        download_sounds_path = create_download_directory("sounds")  # Create directory and get path
        mergefiles_path = create_download_directory("downloads")  # Create directory and get path
        
        filename = video_stream.default_filename
        unique_filename = get_unique_filename(download_video_path, filename)
        
        # Download video and audio streams
        video_stream.download(download_video_path, filename=unique_filename) # Download with unique filename
        
        # Merge video and audio
        video_path = os.path.join(download_video_path, unique_filename)
        time.sleep(0.5)

        audio_stream.download(download_sounds_path, filename=unique_filename)  # Download with unique filename
        audio_path = os.path.join(download_sounds_path, unique_filename)
        time.sleep(0.5)

        if os.path.exists(video_path) and os.path.exists(audio_path):
            # Merge video and audio
            final_output_path = os.path.join(mergefiles_path, f"{unique_filename}")
            merge_video_audio(video_path, audio_path, final_output_path)

        else:
            print("Error: Video or audio download failed.")

    except Exception as e:
        print("Error: " + str(e))
    finish.configure(text="Download Completed to " + os.path.join(mergefiles_path, unique_filename))

# System settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# App frame
app = customtkinter.CTk()
app.geometry("800x520")
app.title("YouTube Download")

# UI elements
title = customtkinter.CTkLabel(app, text="Insert YouTube Link")
title.pack(padx=10, pady=10)

# Link input
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=450, height=40, textvariable=url_var)
link.pack()

# Download button
download = customtkinter.CTkButton(app, text="Download", command=startDownload)
download.pack(padx=20, pady=20)

# Progress bar
pPercentage = customtkinter.CTkLabel(app, text="0%")
pPercentage.pack()

progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)
progressBar.pack(padx=10, pady=10)

#Finish Download
finish = customtkinter.CTkLabel(app, text="")
finish.pack()

# Run app
app.mainloop()