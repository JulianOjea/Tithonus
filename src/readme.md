execution command: 

py -m PyInstaller --onefile --windowed --icon=assets/tithonus_logo.ico --hidden-import=yt_dlp --hidden-import=yt_dlp.utils --hidden-import=yt_dlp.extractor --hidden-import=PIL.Image --add-data "assets;assets" download_youtube.py

