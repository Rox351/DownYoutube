import yt_dlp
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import sys
import threading
import os
import audioread
from pydub import AudioSegment
from moviepy.editor import AudioFileClip

# Classe para redirecionar a saída para o widget de texto
class RedirectOutput:
    def __init__(self, widget):
        self.widget = widget

    def write(self, message):
        self.widget.insert(tk.END, message)
        self.widget.see(tk.END)  # Auto scroll to the end
        self.widget.update()     # Atualiza a interface em tempo real

    def flush(self):
        pass  # Necessário para compatibilidade com sys.stdout

# Função para iniciar o download em uma nova thread
def baixar_videos():
    video_urls = [entry.get() for entry in url_entries if entry.get().strip()]
    if not video_urls:
        messagebox.showwarning("Atenção", "Adicione pelo menos um URL.")
        return
    if not output_directory:
        messagebox.showwarning("Atenção", "Escolha um diretório de salvamento.")
        return

    # Executa o processo de download em uma thread separada
    thread = threading.Thread(target=executar_download, args=(video_urls,))
    thread.start()

# Função para executar o download e mostrar progresso
def executar_download(video_urls):
    # Define o formato de download com base na escolha do usuário
    if formato_download.get() == "video":
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{output_directory}/%(title)s.%(ext)s',  # Caminho de salvamento
            'nocheckcertificate': True,
            'progress_hooks': [progresso_download]  # Callback para progresso
        }
    elif formato_download.get() == "audio":
        ydl_opts = {
            'format': 'bestaudio/best',  # Melhor áudio disponível
            'outtmpl': f'{output_directory}/%(title)s.%(ext)s',  # Caminho de salvamento
            'nocheckcertificate': True,
            'progress_hooks': [progresso_download],  # Callback para progresso
            'extractaudio': True,  # Baixar apenas o áudio
            'audioquality': 0,  # Qualidade máxima de áudio
            'writethumbnail': False,  # Não baixar a miniatura
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(video_urls)

        # Após o download, converter para MP3 (se necessário)
        if formato_download.get() == "audio":
            for file in os.listdir(output_directory):
                if file.endswith(".webm"):
                    input_path = os.path.join(output_directory, file)
                    output_path = os.path.join(output_directory, file.replace(".webm", ".mp3"))
                    converter_para_mp3(input_path, output_path)

        messagebox.showinfo("Sucesso", "Download(s) concluído(s) e convertido(s)!")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")



# Função para converter .webm para .mp3 usando moviepy
def converter_para_mp3(input_path, output_path):
    try:
        # Carrega o arquivo .webm como um objeto de áudio
        audio_clip = AudioFileClip(input_path)
        
        # Salva como .mp3
        audio_clip.write_audiofile(output_path, codec='mp3')
        
        # Remover o arquivo original .webm após conversão
        os.remove(input_path)

        print(f"Arquivo convertido com sucesso para {output_path}")
    
    except Exception as e:
        print(f"Erro na conversão: {e}")

# Callback para progresso do download
def progresso_download(d):
    if d['status'] == 'downloading':
        mensagem = f"Baixando: {d['_percent_str']} - {d['_eta_str']} restantes\n"
    elif d['status'] == 'finished':
        mensagem = "Download concluído!\n"
    else:
        mensagem = "Preparando para download...\n"

    text_output.insert(tk.END, mensagem)
    text_output.see(tk.END)  # Auto scroll
    text_output.update()     # Atualiza a interface em tempo real

# Função para adicionar um novo campo de URL
def adicionar_campo_url():
    entry = tk.Entry(frame_urls, width=60)
    entry.pack(pady=2)
    url_entries.append(entry)

# Função para remover o último campo de URL
def remover_campo_url():
    if url_entries:
        entry = url_entries.pop()
        entry.destroy()

# Função para escolher o diretório de salvamento
def escolher_diretorio():
    global output_directory
    output_directory = filedialog.askdirectory()
    label_diretorio.config(text=output_directory if output_directory else "Escolha um diretório")

# Configuração da interface principal
root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("600x550")

label_mensagem = tk.Label(root, text="Insira um Link no campo abaixo:", font=("Arial", 12))
label_mensagem.pack(pady=5)

# Diretório de saída inicial vazio
output_directory = ""

# Lista de entradas de URLs
url_entries = []

# Frame para URLs
frame_urls = tk.Frame(root)
frame_urls.pack(pady=10)

# Botões para adicionar e remover campos de URL
btn_adicionar = tk.Button(root, text="Adicionar URL", command=adicionar_campo_url)
btn_adicionar.pack(pady=5)
btn_remover = tk.Button(root, text="Remover Última URL", command=remover_campo_url)
btn_remover.pack(pady=5)

# Botão para escolher diretório
btn_escolher_diretorio = tk.Button(root, text="Escolher Diretório de Salvamento", command=escolher_diretorio)
btn_escolher_diretorio.pack(pady=10)

# Rótulo para mostrar o diretório de salvamento selecionado
label_diretorio = tk.Label(root, text="Escolha um diretório")
label_diretorio.pack(pady=5)

# Opções de formato (vídeo ou áudio)
formato_download = tk.StringVar(value="video")
frame_formatos = tk.Frame(root)
frame_formatos.pack(pady=10)
tk.Label(frame_formatos, text="Escolha o formato de download:").pack(side=tk.LEFT)
radio_video = tk.Radiobutton(frame_formatos, text="Vídeo", variable=formato_download, value="video")
radio_video.pack(side=tk.LEFT, padx=5)
radio_audio = tk.Radiobutton(frame_formatos, text="Áudio (MP3)", variable=formato_download, value="audio")
radio_audio.pack(side=tk.LEFT, padx=5)

# Botão para baixar os vídeos
btn_baixar = tk.Button(root, text="Baixar Vídeos", command=baixar_videos)
btn_baixar.pack(pady=20)

label_mensagem = tk.Label(root, text="Desenvolvido por: LeoRox351", font=("Arial", 8))
label_mensagem.pack(pady=5)

# Área de texto para exibir as mensagens do terminal
text_output = ScrolledText(root, wrap=tk.WORD, height=10)
text_output.pack(pady=10, fill=tk.BOTH, expand=True)

# Redireciona a saída do terminal para o widget de texto
sys.stdout = RedirectOutput(text_output)
sys.stderr = RedirectOutput(text_output)

# Adicionar um campo inicial de URL
adicionar_campo_url()

root.mainloop()
