BotMusicDiscord🎵

Um bot de música para Discord, desenvolvido em Python, que permite reproduzir músicas diretamente em canais de voz.


Funcionalidades 🚀

🎶 Reproduzir Músicas: Toque músicas diretamente do YouTube usando links ou nomes.

⏯️ Controle de Reprodução: Pause, retome ou pare as músicas.

📜 Fila de Músicas: Adicione múltiplas músicas à fila para reprodução contínua.

⏭️ Pular Músicas: Pule para a próxima música da fila.

🆘 Ajuda: Comando !help que exibe a lista de comandos disponíveis.


| Comando       | Descrição                                         |
|---------------|---------------------------------------------------|
| `!play [nome/link]` | Toca uma música pelo nome ou link do YouTube.  |
| `!pause`       | Pausa a música atual.                           |
| `!resume`      | Retoma a música pausada.                        |
|  `!queue`  	   | Exibe a fila de musica.
| `!stop`        | Para a reprodução e limpa a fila.               |
| `!next`        | Pula para a próxima música da fila.             |
| `!help`        | Mostra a lista de comandos e suas descrições.   |

Pré-requisitos

Python 3.8 ou superior instalado na máquina.

Um token de bot do Discord.


Passo a Passo

Clone este repositório:


git clone https://github.com/Anoiim/BotMusicDiscord.git

cd BotMusicDiscord

Instale as dependencias: pip install -r requirements.txt

3.Adicione o token do seu bot no arquivo "config.py"

TOKEN = "Seu token"


4.Execute o bot:


python app.py



obs. Faça a instalação do ffmpeg no seu computador caso a musica não toque.
https://www.ffmpeg.org/download.html
