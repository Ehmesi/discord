import os
import discord
from discord.ext import tasks, commands
from flask import Flask
from threading import Thread

# === CONFIGURATION ===
CHANNEL_ID = 1374155533774229584  # Replace with your channel ID
MESSAGE = "@everyone haggle retards"

# === KEEP ALIVE WEB SERVER ===
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# === DISCORD BOT ===
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    send_message.start()

@tasks.loop(minutes=240)
async def send_message():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(MESSAGE)
    else:
        print("Channel not found!")

# === START BOT ===
keep_alive()
TOKEN = os.environ['TOKEN']  # Token stored in Heroku config vars
bot.run(TOKEN)
