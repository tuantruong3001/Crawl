#Set up evironment

pip install customtkinter

pip install pytubefix

pip install tk

set PYTHONPATH=C:\Users\tuantv\Desktop\StudyCode\New folder

#confifure ffmpeg

Step 1: Add FFmpeg to System PATH
Open Environment Variables:

Open the Start Menu, search for "Environment Variables", and select "Edit the system environment variables".
In the System Properties window, click on the "Environment Variables" button.
Edit the PATH Variable:

In the Environment Variables window, find the "Path" variable in the "System variables" section and select it, then click "Edit".
Click "New" and add the path to the bin directory of your FFmpeg folder (e.g., E:\bin).
Click "OK" to close all windows.
Verify FFmpeg Installation:

Open a new Command Prompt window and type ffmpeg -version. You should see the version information of FFmpeg if it is correctly installed and added to the PATH.

#Run
python .\main.py