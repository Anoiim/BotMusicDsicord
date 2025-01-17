import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio
import config 

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None) # Prefixo para os comandos do bot

ytdl_format_options = {
    'format': 'bestaudio/best',
    'noplaylist': True
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

music_queue = []
playing = False  

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}!')

@bot.command(name='join')
async def join(ctx):
    """Conecta o bot ao canal de voz do usuário."""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await channel.connect()
            await ctx.send("Entrei no canal de voz!")
        else:
            await ctx.send("Já estou em um canal de voz.")
    else:
        await ctx.send("Você precisa estar em um canal de voz!")

@bot.command(name='leave')
async def leave(ctx):
    """Desconecta o bot do canal de voz."""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Saí do canal de voz!")
    else:
        await ctx.send("Não estou em um canal de voz!")

@bot.command(name='play')
async def play(ctx, *, song_name: str):
    """Busca e toca uma música pelo nome no YouTube."""
    global music_queue, playing

    if not ctx.voice_client:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("Você precisa estar em um canal de voz primeiro!")
            return

    try:
        # Buscar a música no YouTube
        search_query = f"ytsearch:{song_name}"
        info = ytdl.extract_info(search_query, download=False)['entries'][0]

        # Adiciona à fila
        music_queue.append((info['title'], info['url']))
        await ctx.send(f"Adicionado à fila: {info['title']}")

        # Se não estiver tocando nada, começa a tocar
        if not playing:
            await play_next(ctx)

    except Exception as e:
        await ctx.send(f"Erro ao adicionar música: {e}")

async def play_next(ctx):
    """Toca a próxima música na fila."""
    global music_queue, playing

    if len(music_queue) > 0:
        playing = True
        title, url = music_queue.pop(0)

        try:
            FFMPEG_OPTIONS = {'options': '-vn'}
            with youtube_dl.YoutubeDL(ytdl_format_options) as ydl:
                info = ydl.extract_info(url, download=False)
                audio_url = info['url']

            # Toca o áudio
            source = discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS)
            ctx.voice_client.play(source, after=lambda e: bot.loop.create_task(play_next(ctx)))

            await ctx.send(f"🎵 Tocando agora: {title}")

        except Exception as e:
            await ctx.send(f"Erro ao reproduzir música: {e}")
            playing = False  # Resetar para evitar loop infinito
    else:
        playing = False
        await ctx.send("A fila está vazia!")

@bot.command(name='pause')
async def pause(ctx):
    """Pausa a música atual."""
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("⏸️ Música pausada!")
    else:
        await ctx.send("Nenhuma música está tocando no momento.")

@bot.command(name='resume')
async def resume(ctx):
    """Retoma a música pausada."""
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("▶️ Música retomada!")
    else:
        await ctx.send("Nenhuma música está pausada no momento.")

@bot.command(name='stop')
async def stop(ctx):
    """Para completamente a música."""
    global playing
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        playing = False  # Resetar estado de reprodução
        await ctx.send("⏹️ Música parada!")
    else:
        await ctx.send("Nenhuma música está tocando no momento.")

@bot.command(name='queue')
async def queue(ctx):
    """Mostra as músicas na fila."""
    if music_queue:
        queue_list = "\n".join([f"{idx+1}. {title}" for idx, (title, _) in enumerate(music_queue)])
        await ctx.send(f"📜 **Fila de músicas:**\n{queue_list}")
    else:
        await ctx.send("A fila está vazia!")

@bot.command(name='next')
async def next(ctx):
    """Pula para a próxima música."""
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏭️ Pulando para a próxima música...")
    else:
        await ctx.send("Nenhuma música está tocando no momento para pular.")

@bot.command(name='help')
async def help_command(ctx):
    """Exibe os comandos disponíveis."""
    help_message = (
        "**🎵 Comandos disponíveis:**\n\n"
        "**!join** - Faz o bot entrar no canal de voz onde você está.\n"
        "**!leave** - Faz o bot sair do canal de voz.\n"
        "**!play <nome da música>** - Busca e adiciona uma música à fila.\n"
        "**!pause** - Pausa a música atual.\n"
        "**!resume** - Retoma a música pausada.\n"
        "**!stop** - Para completamente a música.\n"
        "**!queue** - Mostra as músicas na fila.\n"
        "**!next** - Pula para a próxima música na fila.\n"
        "**!help** - Mostra esta mensagem de ajuda.\n\n"
        "📢 **Use os comandos no chat de texto enquanto estiver em um canal de voz!**"
    )
    await ctx.send(help_message)

bot.run(config.TOKEN)