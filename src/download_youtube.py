import os
import sys
import threading
import tkinter as tk
from tkinter import messagebox, filedialog
from yt_dlp import YoutubeDL
from datetime import datetime
import re
from PIL import Image, ImageTk

def quitar_ansi(texto):
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        return ansi_escape.sub('', texto)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

class DescargadorMP3App:
    def __init__(self, root):
        self.root = root
        self.root.title("Tithonus")
        self.root.geometry("600x500")
        self.centrar_ventana(600, 500)

        self.output_folder = "mp3_playlist"
        os.makedirs(self.output_folder, exist_ok=True)
        self.error_log = os.path.join(self.output_folder, "errores.txt")

        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        carpeta_frame = tk.Frame(frame)
        carpeta_frame.pack(pady=(10, 10), fill=tk.X)

        btn_carpeta = tk.Button(carpeta_frame, text="Seleccionar carpeta de destino", command=self.seleccionar_carpeta)
        btn_carpeta.pack(side=tk.LEFT)

        self.label_carpeta = tk.Label(carpeta_frame, text=f"Carpeta actual: {self.output_folder}")
        self.label_carpeta.pack(side=tk.LEFT, padx=(10, 0))

        boton_frame = tk.Frame(frame)
        boton_frame.pack(pady=10)

        tk.Label(boton_frame, text="URL de la playlist de YouTube:").pack(anchor='w')
        self.entry_url = tk.Entry(boton_frame, width=70)
        self.entry_url.pack(side=tk.LEFT, padx=(0, 10))

        self.btn_descargar = tk.Button(boton_frame, text="Descargar", command=self.iniciar_descarga)
        self.btn_descargar.pack(side=tk.LEFT, padx=(0, 10))  # espacio entre botones

        btn_info = tk.Button(boton_frame, text=" \u2139 ", command=self.mostrar_info)
        btn_info.pack(side=tk.LEFT)

        self.log_text = tk.Text(self.root, height=15, wrap=tk.WORD)
        self.log_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.progress_label = tk.Label(self.root, text=" ", height=1)
        self.progress_label.pack(padx=10, pady=5)

    def centrar_ventana(self, ancho=600, alto=500):
        # Obtener el tamaño de la pantalla
        pantalla_ancho = self.root.winfo_screenwidth()
        pantalla_alto = self.root.winfo_screenheight()

        # Calcular posición x, y para centrar
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)

        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

    def seleccionar_carpeta(self):
        carpeta = filedialog.askdirectory(initialdir=self.output_folder, title="Selecciona carpeta para guardar MP3")
        if carpeta:
            self.output_folder = carpeta
            self.label_carpeta.config(text=f"Carpeta actual: {self.output_folder}")
            self.error_log = os.path.join(self.output_folder, "errores.txt")

    def mostrar_info(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Cómo obtener la URL de una playlist")

        try:
            ruta_imagen = resource_path("assets/basic_instructions.PNG")
            img = Image.open(ruta_imagen)
            img = img.resize((800, 600), Image.LANCZOS)
            imagen_tk = ImageTk.PhotoImage(img)

            label_imagen = tk.Label(ventana, image=imagen_tk)
            label_imagen.image = imagen_tk  # mantener la referencia
            label_imagen.pack(padx=10, pady=10)
        except Exception as e:
            tk.Label(ventana, text=f"No se pudo cargar la imagen:\n{e}").pack(padx=10, pady=10)



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
            if not porcentaje_limpio:
                porcentaje_limpio = "Descargando..."
            self.progress_label.after(0, lambda: self.progress_label.config(text=porcentaje_limpio))
        elif d['status'] == 'finished':
            self.progress_label.after(0, lambda: self.progress_label.config(text="100%"))


    def descargar_playlist(self, url):
        self.btn_descargar.after(0, lambda: self.btn_descargar.config(state=tk.DISABLED))

        self.log_text.insert(tk.END, "🔍 Obteniendo lista de vídeos...\n")
        self.log_text.see(tk.END)

        try:
            videos = self.obtener_urls_individuales(url)
        except Exception as e:
            self.log_text.insert(tk.END, f"❌ Error al obtener vídeos: {e}\n")
            self.btn_descargar.after(0, lambda: self.btn_descargar.config(state=tk.NORMAL))
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
        self.btn_descargar.after(0, lambda: self.btn_descargar.config(state=tk.NORMAL))

    def iniciar_descarga(self):
        url = self.entry_url.get()
        if not url:
            messagebox.showwarning("Error", "Introduce una URL válida.")
            return

        threading.Thread(target=self.descargar_playlist, args=(url,), daemon=True).start()

# --- Lanzar aplicación ---
if __name__ == "__main__":
    root = tk.Tk()

    ruta_ico = resource_path("assets/tithonus_logo.ico")

    if os.path.exists(ruta_ico):
        try:
            root.iconbitmap(ruta_ico)
        except Exception as e:
            print(f"No se pudo cargar el icono .ico: {e}")
    else:
        print("Icono .ico no encontrado:", ruta_ico)

    ruta_ico = resource_path("assets/tithonus_logo.ico")
    ruta_png = resource_path("assets/tithonus_logo.png")

    root.update()

    try:
        icon_png = tk.PhotoImage(file=ruta_png)
        root.call('wm', 'iconphoto', root._w, icon_png)
    except Exception as e:
        print(f"No se pudo cargar el icono PNG: {e}")

    app = DescargadorMP3App(root)
    root.mainloop()