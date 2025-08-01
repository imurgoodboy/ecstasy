import discord
from discord.ext import commands
from pymongo import MongoClient
from datetime import datetime, timezone
import asyncio
import logging
import json
import os

# MongoDB Setup
mongo_client = MongoClient("mongodb+srv://samarramsingh04:samar234@xpprofile.qo44i.mongodb.net/")
db = mongo_client["moderation"]
collection = db["flags"]

# Local backup file for failed MongoDB inserts
BACKUP_FILE = "failed_inserts.json"

class DataStorage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("DataStorage Cog Loaded!")
        # Load existing backup data
        self.failed_records = self.load_failed_records()
        self.bot.loop.create_task(self.retry_failed_inserts())

    def load_failed_records(self):
        """Load failed MongoDB inserts from a local file."""
        if os.path.exists(BACKUP_FILE):
            with open(BACKUP_FILE, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    logging.error("Failed to decode backup file.")
                    return []
        return []

    def save_failed_records(self):
        """Save failed MongoDB inserts to a local file."""
        with open(BACKUP_FILE, "w") as f:
            json.dump(self.failed_records, f, indent=4)

    async def retry_failed_inserts(self):
        """Periodically retry failed MongoDB inserts."""
        while True:
            if self.failed_records:
                logging.info(f"Retrying {len(self.failed_records)} failed inserts...")
                for record in self.failed_records[:]:
                    try:
                        collection.insert_one(record)
                        self.failed_records.remove(record)
                        logging.info(f"Successfully retried insert for {record['message_link']}")
                    except Exception as e:
                        logging.error(f"Retry failed for {record['message_link']}: {e}")
                self.save_failed_records()
            await asyncio.sleep(60)

    async def log_flagged_message(self, message, reason_type: str):
        """Logs the flagged message to MongoDB and sends an alert embed."""
        if not message.guild:
            return

        user_id = str(message.author.id)
        username = str(message.author)
        content = message.content
        guild_id = str(message.guild.id)
        timestamp = datetime.now(timezone.utc).isoformat()

        # Handle different channel types
        if isinstance(message.channel, discord.Thread):
            channel_name = f"{message.channel.parent.name} > {message.channel.name}"
        else:
            channel_name = message.channel.name
        message_link = f"https://discord.com/channels/{guild_id}/{message.channel.id}/{message.id}"

        # Prepare record for MongoDB
        record = {
            "user_id": user_id,
            "username": username,
            "message": content,
            "channel": channel_name,
            "timestamp": timestamp,
            "reason": reason_type,
            "message_link": message_link,
            "channel_type": message.channel.__class__.__name__
        }

        # Send the alert embed immediately, even if MongoDB is down
        await self.send_alert_embed(message, content, message_link, reason_type)

        # Attempt to log to MongoDB
        try:
            await self.bot.loop.run_in_executor(None, self.insert_to_mongo, record)
        except Exception as e:
            logging.error(f"MongoDB Insert Error: {e}")
            self.failed_records.append(record)
            self.save_failed_records()

    def insert_to_mongo(self, record):
        """Synchronous MongoDB insert operation"""
        try:
            collection.insert_one(record)
            print(f"Message logged: {record['message_link']}")
        except Exception as e:
            logging.error(f"MongoDB Insert Error: {e}")

    async def send_alert_embed(self, message, content, link, reason):
        embed = discord.Embed(
            title="Flagged Message Detected",
            description=f"[Click here to view the message]({link})\n\n**Content:** {content}",
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
async def setup(bot):
    await bot.add_cog(DataStorage(bot))
