import discord
from discord.ext import commands
import json
import os

TRAINING_FILE = "training_data.json"

class Training(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not os.path.exists(TRAINING_FILE):
            with open(TRAINING_FILE, "w") as f:
                json.dump([], f)

    @commands.command(name="train_model")
    @commands.has_permissions(administrator=True)
    async def train_model(self, ctx, awkward_input: str, expected_response: str):
        """Admins can train the bot to avoid awkward replies."""
        # Load existing data
        with open(TRAINING_FILE, "r") as f:
            data = json.load(f)

        # Add new pair
        data.append({
            "awkward_input": awkward_input,
            "expected_response": expected_response
        })

        # Save it
        with open(TRAINING_FILE, "w") as f:
            json.dump(data, f, indent=4)

        await ctx.send("✅ Training data added!")

    @train_model.error
    async def train_model_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You need administrator permissions to use this command.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("⚠️ Please use it like: `!train_model \"awkward msg\" \"better msg\"`")
        else:
            await ctx.send("⚠️ Something went wrong.")

async def setup(bot):
    await bot.add_cog(Training(bot))
