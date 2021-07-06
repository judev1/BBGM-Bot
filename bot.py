from discord.ext import commands
import os

TOKEN = "TOKEN"

if not os.path.exists("data"):
    os.makedirs("data")

bot = commands.Bot(command_prefix="!", owner_id=671791003065384987)

for cog in os.listdir("cogs"):
    if os.path.isfile(os.path.join("cogs", cog)):
        print(f"Loading {cog}... ", end="")
        bot.load_extension(f"cogs.{cog[:-3]}")
        print("Done!")

@bot.event
async def on_ready():
    print(f"Ready and logged in as {bot.user}")

bot.run(TOKEN)