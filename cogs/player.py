from discord.ext import commands
import json
import os

stat_names = ["stre", "spd", "jmp", "endu", "ins", "dnk", "ft", "fg", "tp", "oiq", "diq", "drb", "pss", "reb"]

class Export(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ups(self, ctx, pid, *stats):
        path = f"data/{ctx.guild.id}"
        if not os.path.exists(path):
            os.makedirs(path)

        # TODO errorchecking for non-bbgm files

        await ctx.message.add_reaction("⏲️")

        if os.path.exists(path + "/changes.json"):
            with open(path + "/changes.json") as file:
                changes = json.load(file)
        else: changes = {"changes": list()}

        if os.path.exists(path + "/bbgm.json"):
            with open(path + "/bbgm.json", "rb") as file:
                data = json.load(file)
        else: data = None

        if not pid.isdigit():
           await ctx.reply("Player id is invalid")
           return
        else:
            pid = int(pid)

        if data:
            found = False
            for player in data["players"]:
                if player["pid"] == pid:
                    found = True
                    player_stats = player["ratings"][0]
                    break
            if not found:
                await ctx.reply("Player id is invalid")
                return

        change_stats = None
        for player in changes["changes"]:
            if player["pid"] == pid:
                player["stats"] = dict()
                change_stats = player["stats"]

        if not change_stats:
            player = {"pid": pid, "stats": dict()}
            changes["changes"].append(player)
            change_stats = player["stats"]

        for stat_change in stats:
            if not "+" in stat_change:
                await ctx.reply("Invalid stat change format")
                return
            stat, change = stat_change.split("+")
            if stat not in stat_names:
                await ctx.reply("`{stat}` is an invalid stat name")
                return
            if data:
                if player_stats[stat] + int(change) > 100:
                    await ctx.reply("Stat change overflows 100")
                    return
            change_stats[stat] = int(change)

        with open(path + "/changes.json", "w") as file:
            json.dump(changes, file)

        await ctx.message.add_reaction("✅")

def setup(bot):
    bot.add_cog(Export(bot))