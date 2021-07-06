from discord.ext import commands
import validators
import asyncio
import aiohttp
import discord
import os

class Export(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="import")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _import(self, ctx, *url):
        path = f"data/{ctx.guild.id}"
        if not os.path.exists(path):
            os.makedirs(path)

        await ctx.message.add_reaction("⏲️")

        attachments = ctx.message.attachments
        if attachments:
            if attachments.filename.lower().endswith(".json"):
                await attachments[0].save(path + "/bbgm.json")
            else:
                await ctx.send("The attachment is not a json file")
                return
        else:
            if not len(ctx.message.content) > 8:
                await ctx.reply("No attachment or link provided")
                return

            url = ctx.message.content[8:]
            if not validators.url(url):
                await ctx.reply("Not a valid link")
                return

            sema = asyncio.BoundedSemaphore(5)
            async with sema, aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    assert resp.status == 200
                    data = await resp.read()

            with open(path + "/bbgm.json", "wb") as file:
                file.write(data)

        await ctx.reply(content="Successfully imported file")

        # TODO cache stuff

def setup(bot):
    bot.add_cog(Export(bot))