from discord.ext import commands
import discord
import json
import os

class Changes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def viewchanges(self, ctx):
        path = f"data/{ctx.guild.id}"
        if not os.path.exists(path):
            os.makedirs(path)

        if not os.path.exists(path + "/changes.json"):
            await ctx.reply("No changes to view")
        else:
            file = discord.File(fp=path + "/changes.json")
            await ctx.send(file=file)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def clearchanges(self, ctx):
        path = f"data/{ctx.guild.id}"
        if not os.path.exists(path):
            os.makedirs(path)

        if not os.path.exists(path + "/changes.json"):
            await ctx.reply("No changes to clear")
        else:
            os.remove(path + "/changes.json")
            await ctx.message.add_reaction("✅")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def syncchanges(self, ctx):
        path = f"data/{ctx.guild.id}"
        if not os.path.exists(path):
            os.makedirs(path)

        if not os.path.exists(path + "/changes.json"):
            await ctx.reply("No changes to sync")
        elif not os.path.exists(path + "/bbgm.json"):
            await ctx.reply("⚠️ **No file found!** Attach a file and use `!import` to import it")
        else:

            # TODO errorchecking for non-bbgm files

            await ctx.message.add_reaction("⏲️")

            with open(path + "/changes.json") as file:
                changes = json.load(file)

            with open(path + "/bbgm.json", "rb") as file:
                data = json.load(file)

            for player in data["players"]:
                pid = player["pid"]
                for changed_player in changes["changes"]:
                    if pid == changed_player["pid"]:
                        stats = changed_player["stats"]
                        for stat in stats:
                            player["ratings"][0][stat] += stats[stat]
                        break

            with open(path + "/bbgm.json", "w") as file:
                json.dump(data, file)
            os.remove(path + "/changes.json")

            await ctx.message.add_reaction("✅")

def setup(bot):
    bot.add_cog(Changes(bot))