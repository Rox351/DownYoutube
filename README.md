# YouTube Downloader - Interface Gráfica em Python

Este projeto é uma ferramenta de download de vídeos e áudios do YouTube com interface gráfica, construída em Python usando `tkinter` e `yt_dlp`. Com ele, você pode baixar vídeos em formato de vídeo ou apenas o áudio em MP3.

## Funcionalidades

- **Download de Múltiplos Vídeos**: Adicione um ou mais links para download.
- **Escolha de Formato**: Baixe o vídeo completo ou apenas o áudio em MP3.
- **Seleção de Diretório**: Escolha onde deseja salvar os arquivos baixados.
- **Conversão para MP3**: Após o download, o áudio pode ser convertido automaticamente para o formato MP3.
- **Interface Simples**: Interface amigável e intuitiva com atualizações de progresso.

## Requisitos

Para executar este projeto, você precisa das seguintes bibliotecas instaladas:

- `yt_dlp`: Ferramenta para download de vídeos de sites como o YouTube.
- `tkinter`: Biblioteca padrão do Python para criar interfaces gráficas.
- `audioread` e `pydub`: Necessárias para a conversão de arquivos de áudio.
- `moviepy`: Usada para converter áudio em diferentes formatos.

Uso da Interface:

Insira o link(s) do YouTube que deseja baixar.
Escolha o formato de download (vídeo ou áudio).
Selecione o diretório de destino onde os arquivos serão salvos.
Clique em "Baixar Vídeos" e acompanhe o progresso na área de mensagens.
Autor
Desenvolvido por LeoRox351

Licença
Este projeto é licenciado sob a MIT License.

Instale as dependências usando o comando abaixo:
```bash
pip install yt-dlp pydub moviepy audioread

