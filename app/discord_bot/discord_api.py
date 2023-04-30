from dotenv import load_dotenv
import discord
from discord import Embed
import os
from app.chatgpt_ai.openai import chatgpt_response
from replit import db

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')


class MyCLient(discord.Client):

  async def on_ready(self):

    print(f"Successfully logged in as {self.user}")

  async def on_message(self, message):

    print(message.content)

    if message.author == self.user:
      return
    command, user_message = None, None

    for text in ['/ai']:
      if message.content.startswith(text):

        command = message.content.split(' ')[0]

        user_message = message.content.replace(text, '')

        print(command, user_message)

    if command == '/ai':
      context = db.get("context")

      if context is None:
        context = {}

      # Store the context information
      prompt = user_message
      bot_response = chatgpt_response(prompt, context)

      # Update the context information
      context["previous_prompt"] = prompt
      context["previous_response"] = bot_response
      db.set("context", context)
      await message.channel.send(f"```ansi\n\Answer: {bot_response}```")


intents = discord.Intents.default()
intents.message_content = True
# print(db["context"])

client = MyCLient(intents=intents)


#
