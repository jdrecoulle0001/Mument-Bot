import os
import discord
from dotenv import load_dotenv
from server import keep_alive
from help import help_dict

load_dotenv()
TOKEN = os.getenv('TOKEN')

from discord.ext import commands, tasks

client = discord.Client()

bot = commands.Bot(command_prefix='$', help_command=None)

import error_handler

error_handler.setup(bot)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='help')
async def help(ctx, args=None):
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
        help_embed.add_field(name="Idiot",
                             value="{}...That's not a command.".format(
                                 ctx.message.author.mention))

    await ctx.send(embed=help_embed)


@bot.command(name='join')
async def join_channel(ctx):
    channel = ctx.message.author.voice.channel
    print(channel)
    await channel.connect()


@bot.command(name='move')
async def move_person(ctx, person: discord.Member, given_name):
    for channel in ctx.guild.channels:
        if channel.name == given_name:
            wanted_channel_id = channel.id

    channel = ctx.message.guild.get_channel(wanted_channel_id)

    await person.move_to(channel)


@bot.command(name='mitch')
async def move_mitch(ctx):
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


@bot.command(name='moveall')
async def move_all(ctx, given_name):

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


@bot.command(name='leave')
async def leave_channel(ctx):
    await ctx.voice_client.disconnect()


keep_alive()
bot.run(TOKEN)
