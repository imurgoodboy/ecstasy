import discord
from discord.ext import commands
import asyncio 
from discord.utils import find 
class VoiceChatCreation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="voicecreate")
    @commands.has_permissions(manage_channels=True)
    async def voice_create(self, ctx, user_limit: int, *, category_name: str = None):
        """Creates a voice channel with a user-specified name and limit."""

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.send("What do you want to name the voice channel?")

        try:
            msg = await self.bot.wait_for('message', timeout=30.0, check=check)
            channel_name = msg.content
        except asyncio.TimeoutError:
            return await ctx.send("You took too long to respond. Cancelling.")

        category = discord.utils.get(ctx.guild.categories, name=category_name) if category_name else None

        try:
            voice_channel = await ctx.guild.create_voice_channel(
                name=channel_name,
                user_limit=user_limit,
                category=category,
                reason=f"Requested by {ctx.author}"
            )
            await ctx.send(f"Voice channel created: {voice_channel.mention}")
        except Exception as e:
            await ctx.send(f"Failed to create voice channel: {e}\n"
                           f"Make sure I have the 'Manage Channels' permission!")
    @commands.command(name="voicedelete")
    @commands.has_permissions(manage_channels = True)    
    async def voice_delete(self, ctx, channel_name = str): 
                        def check(m): 
                            return m.author == ctx.author and m.channel == ctx.channel 
                        await ctx.send("enter the channel name to delete")

                        try: 
                            msg = await self.bot.wait_for('message', timeout = 30.0, check = check)
                            channel_name = msg.content
                        except asyncio.TimeoutError: 
                            return await ctx.send("stop being this slow, you only have 30 seconds")
                        voice_channel = find(lambda c: c.name.lower() == channel_name.lower(), ctx.guild.voice_channels)

                        if voice_channel:
                            try: 
                                await voice_channel.delete()
                            except Exception as e: 
                                    ctx.channel.send(f"{e}")
                            except discord.Forbidden: 
                                ctx.send("no permissions for this")
                            except discord.HTTPException as e:
                                ctx.send(f"failed to delete {e}")   

async def setup(bot):
    await bot.add_cog(VoiceChatCreation(bot))
