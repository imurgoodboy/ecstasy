import discord
import google.generativeai as genai
from discord.ext import commands
from discord.ext import commands


genai.configure(api_key="AIzaSyBJs6VsBiCKCAHlzlsnU71SgkzDYg7Q8-4")

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        action_required = await self.check_behaviour(message)

        if action_required:
            print(f"[Flagged] Message from {message.author}: {message.content}")

            data_cog = self.bot.get_cog("DataStorage")
            if data_cog:
                await data_cog.log_flagged_message(message, reason_type="AutoMod Rule Violation")
            else:
                print("DataStorage cog not found.")

    async def check_behaviour(self, message):
        try:
            model = genai.GenerativeModel('models/gemini-1.5-flash')
            convo = model.start_chat()
            prompt = f"""You are a moderation bot for the Call of Duty: Mobile Discord Server. Your task is to send a report or alert in a channel whenever a user sends a message containing:
1. Hate Speech
2. Sexually Suggestive Comments
3. Messages which contain extreme profanity like "Faggot", "Kike" etc. Censor of those words like F*ggot or general censors like using b1t3ch to bypass etc is also not allowed and should be flagged
4. Messages containing threats of violence or actions like Doxxing/DDOS are also not allowed.
5. Anything which contains a talk about selling/trading/buying codm accounts or any accounts in general. These messages are to be labelled as messages which go against the activision terms of use.

However, light banter such as "crap, what's happening?" or calling each other crap, gay, ass etc is ALLOWED. Do not action those messages. Anything related to taking a dump/shit etc is allowed.

Respond with yes if the message is appropriate and no if not.

Message to check: \"{message.content}\""""

            response = convo.send_message(prompt)
            decision = response.text.strip().lower()

            print(f"[Gemini]: {decision}")
            return decision == "no"

        except Exception as e:
            print(f"[Gemini API Error]: {e}")
            return False

async def setup(bot):
    await bot.add_cog(AutoMod(bot))
    print("AutoMod cog loaded successfully.")
