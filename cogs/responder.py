import discord
from discord.ext import commands
import google.generativeai as genai

genai.configure(api_key="AIzaSyBJs6VsBiCKCAHlzlsnU71SgkzDYg7Q8-4")  # Replace with your Gemini API key

class ChatSession(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_sessions = {}  # {user_id: Gemini chat object}

    @commands.command(name="initiate_conversation")
    async def initiate_conversation(self, ctx):
        user_id = ctx.author.id
        if user_id in self.active_sessions:
            await ctx.send(f"{ctx.author.mention}, you already have an active AI conversation.")
            return

        model = genai.GenerativeModel('models/gemini-1.5-flash')
        convo = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        "You're a helpful assistant in a Discord server. Be friendly and casual, but not overly formal. If the user switches tone using commands, adjust accordingly."
                    ]
                }
            ]
        )

        self.active_sessions[user_id] = convo
        await ctx.send(f"{ctx.author.mention}, AI conversation started! Mention me or reply to me to chat. Use `!end_ai` to end it.")

    @commands.command(name="end_ai")
    async def end_conversation(self, ctx):
        user_id = ctx.author.id
        if user_id in self.active_sessions:
            del self.active_sessions[user_id]
            await ctx.send(f"{ctx.author.mention}, your AI conversation has ended.")
        else:
            await ctx.send("You don’t have an active conversation.")

    @commands.command(name="be_chaotic")
    async def be_chaotic(self, ctx):
        await self._update_personality(ctx, "ok so you're a chaotic discord mod with terminally online energy. type in all lowercase like you're always on discord. roast people with love, be dramatic, sarcastic, and iconic. use innuendo and fake insults but don’t ever actually say anything hurtful. drop up to 3 emojis every 2 messages — not in every single one. put them at the end when you do use them. you're spicy but not offensive, think drag queen meets mod with power issues. act like everyone else is just barely keeping up with your energy 😈"
)

    @commands.command(name="be_strict")
    async def be_strict(self, ctx):
        await self._update_personality(ctx, "Switch to a strict and professional tone. Be serious, neutral, and focused on being helpful with no jokes or sarcasm.")

    @commands.command(name="be_helpful")
    async def be_helpful(self, ctx):
        await self._update_personality(ctx, "Switch to a friendly, casual, and helpful assistant tone. Be supportive, relaxed, and conversational.")

    async def _update_personality(self, ctx, instruction):
        user_id = ctx.author.id
        if user_id not in self.active_sessions:
            await ctx.send("Start a conversation first using `!initiate_conversation`.")
            return

        convo = self.active_sessions[user_id]
        convo.history.append({
            "role": "user",
            "parts": [instruction]
        })

        await ctx.send(f"Personality updated, {ctx.author.mention}!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = message.author.id
        if user_id not in self.active_sessions:
            return

        is_reply_to_bot = (
            message.reference
            and isinstance(message.reference.resolved, discord.Message)
            and message.reference.resolved.author.id == self.bot.user.id
        )
        is_mention = self.bot.user in message.mentions

        if not (is_reply_to_bot or is_mention):
            return

        convo = self.active_sessions[user_id]
        try:
            response = convo.send_message(message.content)
            await message.reply(response.text)
        except Exception as e:
            print(f"[Gemini Error]: {e}")
            await message.channel.send("Something went wrong while chatting with Gemini.")

async def setup(bot):
    await bot.add_cog(ChatSession(bot))
    print("ChatSession cog loaded.")
