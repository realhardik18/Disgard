import os
import json
from datetime import datetime
import nextcord
from nextcord.ext import commands
from creds import BOT_TOKEN
from nextcord import Interaction, SlashOption

intents = nextcord.Intents.default()
intents.guilds = True 
bot = commands.Bot(command_prefix="/", intents=intents)

DB_FILE = 'db.json'

def update_db(user_display_name, channel_id, image_links):
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as file:
            db_data = json.load(file)
    else:
        db_data = []

    new_entry = {
        "user_display_name": user_display_name,
        "channel_id": channel_id,
        "created_time": datetime.now().isoformat(),
        "images": image_links
    }

    # Append new entry
    db_data.append(new_entry)

    with open(DB_FILE, 'w') as file:
        json.dump(db_data, file, indent=4)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.sync_application_commands()

@bot.slash_command(description="Says hello")
async def test(interaction: Interaction):
    await interaction.response.send_message('Hello')

@bot.slash_command(
    name="create_channel",
    description="Creates a new channel with the specified name and uploads images from the given file location"
)
async def create_channel(
    interaction: Interaction,
    file_location: str = SlashOption(description="The file location", required=True),
    name: str = SlashOption(description="The name of the new channel", required=True)
):
    guild = interaction.guild

    new_channel = await guild.create_text_channel(name)

    await interaction.response.send_message(f'Created new channel: {new_channel.mention}')

    image_links = []

    if os.path.exists(file_location) and os.path.isdir(file_location):        
        for filename in os.listdir(file_location):
            file_path = os.path.join(file_location, filename)
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                with open(file_path, 'rb') as file:
                    message = await new_channel.send(file=nextcord.File(file, filename))
                    image_links.append(message.attachments[0].url)
    else:
        await new_channel.send("The provided file location does not exist or is not a directory.")

    # Update the JSON database
    update_db(interaction.user.display_name, new_channel.id, image_links)

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot.run(BOT_TOKEN)