
import discord
import traceback
import sys
from discord.ext import commands
from error_messages import command_error_dict

class CommandErrorHandler(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):

    if hasattr(ctx.command, 'on_error'):
      return

    cog = ctx.cog
    if cog:
      if cog._get_overridden_method(cog.cog_command_error) is not None:
        return

    ignored = (commands.CommandNotFound, )
    error = getattr(error, 'original', error)

    if isinstance(error, ignored):
      await ctx.send("That's just not even a command, my guy. Check out $help")
      return

    if isinstance(error, commands.DisabledCommand):
      await ctx.send(f'{ctx.command} has been disabled. F')

    elif isinstance(error, commands.NoPrivateMessage):
      try:
        await ctx.author.send(f'{ctx.command} can not be used in Private Message. F')
      except discord.HTTPException:
        pass

    else:
      if isinstance(error, commands.MissingRequiredArgument):
        if command_error_dict[ctx.command.name]:
          await ctx.send("You messed it up hey...\n" + command_error_dict[ctx.command.name])
        else:
          await ctx.send("I don't know what you did wrong, bud.")
          print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
          traceback.print_exception(type(error), error, error.__traceback__, file = sys.stderr)
      else:
        print(sys.exc_info())

  @commands.command(name='repeat', aliases=['mimic', 'copy'])
  async def do_repeat(self, ctx, *, inp: str):
    await ctx.send(inp)

  @do_repeat.error
  async def do_repeat_handler(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      if error.param.name == 'inp':
        await ctx.send("You forgot to give me input to repeat!")

def setup(bot):
  bot.add_cog(CommandErrorHandler(bot))