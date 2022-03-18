
import os
import discord
from error_messages import command_error_dict
from dotenv import load_dotenv
from server import keep_alive
from help import help_dict

load_dotenv()
TOKEN = os.getenv('TOKEN')

from discord.ext import commands

client = discord.Client()

bot = commands.Bot(command_prefix='$', help_command=None)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='help')
async def help(ctx, args=None):
  """
    Bot command for providing users with custom definitions of commands library.
    param ctx: context of command call
  """

  help_embed = discord.Embed(title="Mument Bot Help!")
  command_names_list = [x.name for x in bot.commands]

  if not args:
      help_embed.add_field(
          name="List of supported commands:",
          value=
          "***For commands with `<parameter(s)>`, enter the parameter asked for with out the `'<>'` symbols***\n\n"
          + "\n\n".join([
              str() + "`{}:` {}".format(key, value)
              for key, value in help_dict.items()
          ]),
          inline=False)
      help_embed.add_field(
          name="Details",
          value=
          "Type `!help <command name>` for more details about each command.",
          inline=False)

  elif args in command_names_list:
      help_embed.add_field(name=args, value=bot.get_command(args).help)

  else:
      help_embed.add_field(name="Silly",
                            value="{}...That's not a command.".format(
                                ctx.message.author.mention))

  await ctx.send(embed=help_embed)


# @bot.command(name='liked_tracks')
# async def liked_tracks(ctx, args=None):
#   # TODO: 
#   """
#     Implement Spotify Integration so that bot will play music from liked songs of user
#     param ctx: context of call (see Discord API Reference). Included with all bot commands
#   """ 
  
#   await ctx.send("This feature is still being implemented. Sorry :(")
#   return

#   auth_manager = SpotifyClientCredentials()
  
#   sp = spotipy.Spotify(auth_manager=auth_manager)

#   results = sp.current_user_saved_tracks()

#   tracks = enumerate(results['items'])
#   i = 0
#   while(i < 10):
#     print(tracks[i])

# Bot Command "$join"
@bot.command(name='join')
async def join_channel(ctx):
  """
    Mument Bot joins the current voice channel of the caller.
    param ctx: context of the call
  """
  channel = ctx.message.author.voice.channel
  print(channel)
  await channel.connect()


# Bot command "$move"
@bot.command(name='move')
async def move_person(ctx, person: discord.Member, given_name):
  """
    Mument Bot moves member of discord server to another voice channel.
    param ctx: context of the call
    param person<discord.Member>: person to move to channel
    param given_name: name of the voice channel to move person to
  """
  for channel in ctx.guild.channels:
      if channel.name == given_name:
          wanted_channel_id = channel.id
  
  try:
    channel = ctx.message.guild.get_channel(wanted_channel_id)
    await person.move_to(channel)
  except:
    await ctx.send(f'```No. That\'s not how you do that.\n{command_error_dict["move"]}```')

# Bot command "$mitch"
# Bot moves Mitch to any other channel than the one the caller is in
@bot.command(name='mitch')
async def move_mitch(ctx):
  """
    Mument bot will boot mitch to another random voice channel if he is in the caller's current voice channel.
    param ctx: context of the call
  """
  mitch_id = "601493771858870277"

  author_channel = ctx.message.author.voice.channel
  for channel in ctx.guild.channels:
      if not channel.name == author_channel.name and channel.type is discord.ChannelType.voice:
          wanted_channel_id = channel.id

  print(wanted_channel_id)
  mitch_user = await bot.fetch_user(mitch_id)
  mitch_member = await ctx.guild.fetch_member(mitch_id)

  new_mitch_channel = ctx.message.guild.get_channel(wanted_channel_id)

  await mitch_member.move_to(new_mitch_channel)

  await ctx.send(f'What\'s the shape of Italy {mitch_user.mention}?')


# Bot command "$moveall"
@bot.command(name='moveall')
async def move_all(ctx, given_name):
  """
    Mument Bot will move everyone from the current voice channel of the caller to the other voice channel defined.
    param ctx: context of the call
    param given_name: voice channel to move all users, in current voice, channel to
  """

  for channel in ctx.guild.channels:
      if channel.name == given_name:
          channel_id = channel.id

  channel = ctx.message.guild.get_channel(channel_id)

  vc = ctx.message.guild.get_channel(
      ctx.message.author.voice.channel.id).voice_states

  print(list(vc))

  for user in vc:
      id = await ctx.guild.fetch_member(user)
      await id.move_to(channel)


# Bot command "$leave"
@bot.command(name='leave')
async def leave_channel(ctx):
  """
    Mument will leave the voice channel it is currently in.
    param ctx: context of the call
  """
  await ctx.voice_client.disconnect()


keep_alive()
bot.run(TOKEN)
