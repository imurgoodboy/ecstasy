import discord
from discord.ext import commands
from pymongo import MongoClient
from datetime import datetime, timezone
import asyncio

# MongoDB Setup
mongo_client = MongoClient("mongodb+srv://samarramsingh04:samar234@xpprofile.qo44i.mongodb.net/")
db = mongo_client["moderation"]
collection = db["flags"]

class DataStorage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("DataStorage Cog Loaded!")

    async def log_flagged_message(self, message, reason_type: str):
        """Logs the flagged message to MongoDB and sends an alert embed."""
        user_id = str(message.author.id)
        username = str(message.author)
        content = message.content
        channel_name = message.channel.name
        guild_id = str(message.guild.id)
        timestamp = datetime.now(timezone.utc).isoformat()

        message_link = f"https://discord.com/channels/{guild_id}/{message.channel.id}/{message.id}"

        record = {
            "user_id": user_id,
            "username": username,
            "message": content,
            "channel": channel_name,
            "timestamp": timestamp,
            "reason": reason_type,
            "message_link": message_link
        }

        # Insert to MongoDB in the background
        asyncio.create_task(self.insert_to_mongo(record))

        # Send alert embed
        await self.send_alert_embed(message, content, message_link, reason_type)

    async def insert_to_mongo(self, record):
        try:
            collection.insert_one(record)
            print(f"Message logged: {record['message_link']}")
        except Exception as e:
            print(f"MongoDB Insert Error: {e}")

    async def send_alert_embed(self, message, content, link, reason):
        embed = discord.Embed(
            title="🚩 Flagged Message Detected",
            description=f"[Click here to view the message]({link})",
            color=discord.Color.red()
        )
        embed.add_field(name="User", value=f"{message.author} (`{message.author.id}`)", inline=True)
        embed.add_field(name="Channel", value=message.channel.name, inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text=f"Flagged at {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC")

        alert_channel = discord.utils.get(message.guild.text_channels, name="alerts")
        if alert_channel:
            await alert_channel.send(embed=embed)
        else:
            print(f"No #alerts channel found in {message.guild.name}.")

# Setup function
#async def setup(bot):
    #await bot.add_cog(DataStorage(bot))
