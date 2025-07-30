import discord
from discord.ext import commands
from datetime import datetime, timezone
#elastic search password jQjVhOSCbQD2eMwxZu6H
class Stuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_alert_embed(self, message, content, link, reason):
        embed = discord.Embed(
            title=f"Flagged Message Detected",
            description=f"[{content}]({link})",
            color=discord.Color.red()
        )
        embed.add_field(name="User", value=f"{message.author} (`{message.author.id}`)", inline=True)
        embed.add_field(name="Channel", value=message.channel.name, inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text=f"Flagged at {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC")

        # Iterate through all text channels in the guild to find the alerts channel
        alert_channel = discord.utils.get(message.guild.text_channels, name="alerts")

        if alert_channel:
            print(f"Alert channel found: {alert_channel.name}")
            await alert_channel.send(embed=embed)
        else:
            print(f"No #alerts channel found in {message.guild.name}.")
async def setup(bot):
    await bot.add_cog(Stuff(bot))
