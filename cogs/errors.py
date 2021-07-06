from discord.ext import commands
import discord

class Errors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if hasattr(ctx.command, "on_error"): return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        if type(error) is commands.CommandNotFound:
            return
        elif type(error) is commands.MissingPermissions:
            return
        elif type(error) is commands.NotOwner:
            return
        elif type(error) is commands.MessageNotFound:
            return
        elif type(error) is commands.BadArgument:
            await ctx.reply("**Bad argument.** Looks like one of the arguments you entered is a bit off...")
        elif type(error) is commands.MissingRequiredArgument:
            await ctx.reply("**Command missing an argument.** You've missed an argument for this command")
        elif type(error) is commands.NoPrivateMessage:
            await ctx.reply("**Server only command.** This command can only be used in a server")
        elif type(error) is commands.UserNotFound:
            await ctx.reply("**No user found.** Hmm we couldn't find that user, maybe try something else")
        elif type(error) is commands.UserNotFound:
            await ctx.reply("User not found")
        elif type(error) is commands.ChannelNotFound:
            await ctx.reply("Channel not found")
        elif type(error) is commands.GuildNotFound:
            await ctx.reply("Guild not found")
        else:
            if type(error) is commands.CommandInvokeError:
                if type(error.original) is discord.Forbidden:
                    error = error.original
                    if error.text == "Missing Permissions":
                        try:
                            await ctx.reply("I'm missing permissions to complete this action")
                        except:
                            channel = await ctx.author.create_dm()
                            await channel.send(f"I don't have permissions to send messages in <#{ctx.message.id}>")
                elif type(error.original) is discord.errors.NotFound:
                    if error.original.text == "Unknown User":
                        await ctx.reply("Looks like that member doesn't exist")
                else: raise error
            else: raise error


def setup(bot):
    bot.add_cog(Errors(bot))