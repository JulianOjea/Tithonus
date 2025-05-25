import os
import yt_dlp
from datetime import datetime 

# Crear carpeta de descargas
output_folder = "mp3_playlist"
os.makedirs(output_folder, exist_ok=True)

# Pedir URL de la playlist
playlist_url = input("Introduce la URL de la playlist de YouTube: ")

# Archivo de log de errores
error_log = os.path.join(output_folder, "errores.txt")

# Opciones base de descarga
base_ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'noplaylist': True,  # Importante para descargar vídeo a vídeo
    'quiet': True,       # Modo silencioso
    'no_warnings': True, # No mostrar warnings
}

def descargar_video(url):
    """Descarga un solo vídeo."""
    try:
        with yt_dlp.YoutubeDL(base_ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            print(f"✅ Descargado: {info.get('title', 'Sin título')}")
    except Exception as e:
        print(f"❌ Error descargando: {url}")
        # Guardar error en log
        with open(error_log, 'a', encoding='utf-8') as f:
            f.write(f"Error en '{url}': {str(e)}\n")

def obtener_videos_uno_a_uno(playlist_url):
    """Obtiene todas las URLs individuales de una playlist."""
    videos = []
    opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True,  # No bajar vídeos, solo URLs
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)

        for entry in info.get('entries', []):
            if not entry:
                continue
            url = entry.get('url')
            if url.startswith('http'):
                videos.append(url)
            else:
                videos.append(f"https://www.youtube.com/watch?v={url}")
    
    return videos

# --- MAIN ---
print("\nObteniendo lista de vídeos (modo rápido)...")
videos = obtener_videos_uno_a_uno(playlist_url)
print(f"Se encontraron {len(videos)} vídeos.\n")

for idx, video_url in enumerate(videos, start=1):
    print(f"[{idx}/{len(videos)}] Descargando...")
    descargar_video(video_url)

print(f"\n🎵 Descarga completada. Los MP3 están en '{output_folder}'")
print(f"📜 Si hubo errores, están en '{error_log}'")
import os
import yt_dlp

# Crear carpeta de descargas
output_folder = "mp3_playlist"
os.makedirs(output_folder, exist_ok=True)

# Pedir URL de la playlist
playlist_url = input("Introduce la URL de la playlist de YouTube: ")

# Archivo de log de errores
error_log = os.path.join(output_folder, "errores.txt")

# Opciones base de descarga
base_ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'noplaylist': True,  # Importante para descargar vídeo a vídeo
    'quiet': True,       # Modo silencioso
    'no_warnings': True, # No mostrar warnings
}

def descargar_video(url):
    """Descarga un solo vídeo."""
    try:
        with yt_dlp.YoutubeDL(base_ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            print(f"✅ Descargado: {info.get('title', 'Sin título')}")
    except Exception as e:
        print(f"❌ Error descargando: {url}")
        # Guardar error en log
        with open(error_log, 'a', encoding='utf-8') as f:
            f.write(f"Error en '{url}': {str(e)}\n")

def obtener_videos_uno_a_uno(playlist_url):
    """Obtiene todas las URLs individuales de una playlist."""
    videos = []
    opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True,  # No bajar vídeos, solo URLs
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)

        for entry in info.get('entries', []):
            if not entry:
                continue
            url = entry.get('url')
            if url.startswith('http'):
                videos.append(url)
            else:
                videos.append(f"https://www.youtube.com/watch?v={url}")
    
    return videos

# --- MAIN ---
start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
with open(error_log, 'a', encoding='utf-8') as f:
    f.write(f"\n--- Nueva ejecución: {start_time} ---\n")
    
print("\nObteniendo lista de vídeos (modo rápido)...")
videos = obtener_videos_uno_a_uno(playlist_url)
print(f"Se encontraron {len(videos)} vídeos.\n")

for idx, video_url in enumerate(videos, start=1):
    print(f"[{idx}/{len(videos)}] Descargando...")
    descargar_video(video_url)

print(f"\n🎵 Descarga completada. Los MP3 están en '{output_folder}'")
print(f"📜 Si hubo errores, están en '{error_log}'")
