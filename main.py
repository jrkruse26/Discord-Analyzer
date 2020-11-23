import discord
from discord.ext.commands import Bot
import configparser
import sqlite3


running = False

# declare intents
intents = discord.Intents.default()
intents.members = True
intents.presences = True

# init client
BOT_PREFIX = '-------------'
client = Bot(command_prefix=BOT_PREFIX, intents=intents)

# load private bot keys and attach to client
keyfile = configparser.ConfigParser()
keyfile.read('keys.config')
client.keys = keyfile


@client.event
async def on_ready():
    """Run when bot connects and is ready"""
    global running

    # Only execute if bot is not already running
    if not running:
        c = client.get_channel(388781269275901955)
        messages = []
        i = 0
        conn = sqlite3.connect('messages.db')
        async for message in c.history(limit=None):
            i += 1
            if i % 100 == 0:
                print(i)
            messages.append((message.id, message.author.id, message.author.name, message.channel.id, message.guild.id,
                             message.author.bot, message.content, len(message.attachments), message.created_at,
                             message.edited_at))
        c = conn.cursor()
        c.executemany('INSERT INTO messages (message_id, author_id, author, channel_id, guild_id, is_bot, content,'
                      'attachments, created_at, edited_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', messages)
        conn.commit()
        print('DONE')
        conn.close()
        await client.close()

client.run(client.keys['Discord']['bot'], bot=True)
