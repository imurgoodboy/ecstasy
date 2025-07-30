import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")
print(f"Token loaded.") 

if not token:
    raise ValueError("Token not found in environment variables")


intents = discord.Intents.default()
intents.message_content = True
intents.guild_messages = True
intents.guild_typing = True
intents.guilds = True
intents.messages = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="@", intents=intents)

@bot.event
async def on_ready():
    print(f"Connected to the following guilds: {[guild.name for guild in bot.guilds]}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if bot.user in message.mentions:
        content = message.content.lower()

        if "help" in content:
            command_list = []
            for command in bot.commands:
                if not command.hidden:
                    aliases = f" (aliases: {', '.join(command.aliases)})" if command.aliases else ""
                    command_list.append(f"`{command.name}`{aliases} – {command.help or 'No description'}")

            help_text = "**🧠 Available Commands:**\n" + "\n".join(command_list)
            await message.channel.send(help_text)
            return

    await bot.process_commands(message)


    try:
        if "cogs.moderation" not in bot.extensions:
            await bot.load_extension("cogs.moderation")
            print("Loaded moderation cog.")
    except Exception as e:
        print(f"Failed to load moderation cog: {e}")

    try:
        if "cogs.datastorage3" not in bot.extensions:
            await bot.load_extension("cogs.datastorage3")
            print("Loaded datastorage cog.")
    except Exception as e:
        print(f"Failed to load datastorage cog: {e}")

    try: 
        if 'cogs.training' not in bot.extensions: 
            await bot.load_extension('cogs.training')
            print("loaded training")
    except Exception as e: 
        print(f"coudn't load {e}")
    try: 
        if 'cogs.responder' not in bot.extensions: 
            await bot.load_extension('cogs.responder')
            print("loaded responder")
    except Exception as e: 
        print(f"coudn't load {e}")
    try:
        if 'cogs.voicechat' not in bot.extensions:
            await bot.load_extension('cogs.voicechat')
            print("successfully loaded voicechat cogs")
    except Exception as e:
        print(f"Couldn't load extension: {e}")


bot.run(token)
