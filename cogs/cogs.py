from discord.ext import commands
from discord import Embed, Colour
import os

def get_cogs():
    cogs = []
    for cog in os.listdir("cogs"):
        if os.path.isfile(os.path.join("cogs", cog)):
            cogs.append(cog[:-3])
    return cogs

def cogs_embed(action, unable):
    embed = Embed(title=f"{action}ed all cogs", colour=Colour.green())
    if unable: embed.description = f"Unable to {action.lower()}: ```{', '.join(unable)}```"
    return embed

def cog_embed(action, cog):
    title = f"{action}ed cog: `{cog}`"
    return Embed(title=title, colour=Colour.green())

def error_embed(title, info):
    return Embed(title=f"**{title}**", description=f"```{info}```", colour=Colour.red())

class Cogs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, cog):
        if cog == "all":
            unable = []
            for cog in get_cogs():
                try: self.bot.load_extension("cogs." + cog)
                except: unable.append(cog)
            embed = cogs_embed("Load", unable)
        else:
            try:
                self.bot.load_extension("cogs." + cog)
                embed = cog_embed("Load", cog)
            except Exception as e:
                embed = error_embed(f"Failed to load cog: `{cog}`", str(e))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, cog):
        if cog == "all":
            unable = ["cogs"]
            for cog in get_cogs():
                if cog != "cogs":
                    try: self.bot.unload_extension("cogs." + cog)
                    except: unable.append(cog)
            embed = cogs_embed("Unload", unable)
        else:
            try:
                self.bot.unload_extension("cogs." + cog)
                embed = cog_embed("Unload", cog)
            except Exception as e:
                embed = error_embed(f"Failed to unload cog: `{cog}`", str(e))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog):
        if cog == "all":
            unable = []
            for cog in get_cogs():
                try:
                    self.bot.unload_extension("cogs." + cog)
                    self.bot.load_extension("cogs." + cog)
                except: unable.append(cog)
            embed = cogs_embed("Reload", unable)
        else:
            try:
                self.bot.unload_extension("cogs." + cog)
                self.bot.load_extension("cogs." + cog)
                embed = cog_embed("Reload", cog)
            except Exception as e:
                embed = error_embed(f"Failed to reload cog: `{cog}`", str(e))
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Cogs(bot))