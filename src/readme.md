
Add package ffmpeg to /src/ffmpeg
download from https://www.gyan.dev/ffmpeg/builds/
-> ffmpeg-2025-06-02-git-688f3944ce-essentials_build.7z
execution command: 

py -m PyInstaller --onefile --windowed --icon=assets/tithonus_logo.ico --hidden-import=yt_dlp --hidden-import=yt_dlp.utils --hidden-import=yt_dlp.extractor --hidden-import=PIL.Image --add-data "assets;assets" --add-data "ffmpeg;ffmpeg" --name=Tithonus_v1.3 download_youtube.py 
