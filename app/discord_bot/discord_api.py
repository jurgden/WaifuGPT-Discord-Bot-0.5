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

      elif message.content.startswith("/ti"):
        # Extract the field names and number of rows from the user's message
        table_info = message.content.split("/ti ")[1]
        field_names = table_info.split(" fields: ")[1].split(";")
        num_rows = int(table_info.split("rows: ")[1].split(";")[0])

        # Ask the user for the data to be filled in the cells
        cell_data = []
        for i in range(num_rows):
          row_data = []
          for field_name in field_names:
            await message.channel.send(
              f"Please provide data for field {field_name} in row {i + 1}:")
            data = await self.wait_for("message")
            row_data.append(data.content)
          cell_data.append(row_data)

        # Create a table header row with the field names
        header_row = ""
        for field_name in field_names:
          header_row += f"| {field_name} "
        header_row += "|"

        # Create the table body with filled rows
        table_body = ""
        for i in range(num_rows):
          row = ""
          for data in cell_data[i]:
            row += f"| {data} "
          row += "|"
          table_body += row + "\n"

        # Combine the header row and table body to form the complete table
        table = header_row + "\n" + table_body

        # Create a rich embed with the table as its description
        embed = Embed(title="Table", description=table)
        await message.channel.send(embed=embed)
      elif message.content.startswith("/help"):
        await message.channel.send(
          "/ai for general text\n/ti for a formatted table\nformatted tables are created as follows (/ti table fields:fieldX,fieldY,fieldZ rows:x(amount of rows) )"
        )

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
      await message.channel.send(f"Answer: {bot_response}")


intents = discord.Intents.default()
intents.message_content = True
# print(db["context"])

client = MyCLient(intents=intents)
