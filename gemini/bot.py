"""
Discord Bot 1 - Google Gemini
Usage: @BotName <your question>
"""

import discord
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash-preview-04-17")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"[Gemini Bot] Logged in as {client.user}")

@client.event
async def on_message(message):
    # Ignore messages from bots
    if message.author.bot:
        return

    # Only respond when mentioned
    if client.user not in message.mentions:
        return

    # Strip the mention and get the query
    query = message.content.replace(f"<@{client.user.id}>", "").strip()

    if not query:
        await message.reply("Please include a question after mentioning me!")
        return

    # Ignore image attachments
    if message.attachments:
        await message.reply("I don't support images. Please send text only.")
        return

    async with message.channel.typing():
        try:
            response = model.generate_content(query)
            reply = response.text

            # Discord has a 2000 char limit per message
            if len(reply) > 1990:
                reply = reply[:1990] + "..."

            await message.reply(reply)
        except Exception as e:
            await message.reply(f"Error: {str(e)}")

client.run(DISCORD_TOKEN)
