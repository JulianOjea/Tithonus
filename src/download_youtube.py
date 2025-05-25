import os
import threading
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from yt_dlp import YoutubeDL
from datetime import datetime
import re

def quitar_ansi(texto):
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        return ansi_escape.sub('', texto)

class DescargadorMP3App:
    def __init__(self, root):
        self.root = root
        self.root.title("Descargador de MP3 de YouTube")
        self.root.geometry("600x400")

        self.output_folder = "mp3_playlist"
        os.makedirs(self.output_folder, exist_ok=True)
        self.error_log = os.path.join(self.output_folder, "errores.txt")

        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="URL de la playlist de YouTube:").pack(anchor='w')
        self.entry_url = tk.Entry(frame, width=70)
        self.entry_url.pack()

        btn_descargar = tk.Button(frame, text="Descargar MP3", command=self.iniciar_descarga)
        btn_descargar.pack(pady=10)

        self.log_text = tk.Text(self.root, height=15, wrap=tk.WORD)
        self.log_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.progress_label = tk.Label(self.root, text="")
        self.progress_label.pack(padx=10, pady=5)

    def obtener_urls_individuales(self, playlist_url):
        opts = {
            'quiet': True,
            'skip_download': True,
            'extract_flat': True,
        }
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            videos = []
            for entry in info.get('entries', []):
                url = entry.get('url')
                if url.startswith('http'):
                    videos.append(url)
                else:
                    videos.append(f"https://www.youtube.com/watch?v={url}")
            return videos

    def hook_progreso(self, d):
        if d['status'] == 'downloading':
            porcentaje = d.get('_percent_str', '').strip()
            porcentaje_limpio = quitar_ansi(porcentaje)
            self.progress_label.after(0, lambda: self.progress_label.config(text=porcentaje_limpio))
        elif d['status'] == 'finished':
            texto = "100%"
            self.progress_label.after(0, lambda: self.progress_label.config(text=texto))


    def descargar_playlist(self, url):
        self.log_text.insert(tk.END, "🔍 Obteniendo lista de vídeos...\n")
        self.log_text.see(tk.END)

        try:
            videos = self.obtener_urls_individuales(url)
        except Exception as e:
            self.log_text.insert(tk.END, f"❌ Error al obtener vídeos: {e}\n")
            return

        self.log_text.insert(tk.END, f"🎥 {len(videos)} vídeos encontrados.\n\n")

        for idx, video_url in enumerate(videos, 1):
            self.log_text.insert(tk.END, f"[{idx}/{len(videos)}] Descargando...\n")
            self.log_text.see(tk.END)
            try:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': os.path.join(self.output_folder, '%(title)s.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'noplaylist': True,
                    'quiet': True,
                    'no_warnings': True,
                    'progress_hooks': [self.hook_progreso]
                }

                with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=True)
                    title = info.get('title', 'Sin título')
                    self.log_text.insert(tk.END, f"✅ {title}\n")
            except Exception as e:
                self.log_text.insert(tk.END, f"❌ Error en {video_url}\n")
                with open(self.error_log, 'a', encoding='utf-8') as f:
                    f.write(f"{datetime.now()} | {video_url} | {str(e)}\n")

        self.log_text.insert(tk.END, "\n🎵 ¡Descarga completada!\n")

    def iniciar_descarga(self):
        url = self.entry_url.get()
        if not url:
            messagebox.showwarning("Error", "Introduce una URL válida.")
            return

        threading.Thread(target=self.descargar_playlist, args=(url,), daemon=True).start()


# --- Lanzar aplicación ---
if __name__ == "__main__":
    root = tk.Tk()
    app = DescargadorMP3App(root)
    root.mainloop()