import discord
from discord.ext import commands
import os
import asyncio
import aiohttp
import json
from subprocess import Popen
from datetime import datetime

from discord_tools.tools import get_confirmation, get_response_message
from discord_tools.streamer import Streamer
#retreive credentials from config.py
from config import creds

# import discord_tools.tools as tools

bot = commands.Bot(command_prefix='-')
bot.streamer = Streamer()

@bot.event
async def on_ready():
    print("rpi-streamer started")

@bot.command()
async def history():
    pass

# @bot.command()
# async def anime(ctx, anime):
#     await ctx.send("Enter episode number: ")
#     episode = await get_response_message(ctx.author, ctx.channel, lambda x: x.is_digit())
     
#     await bot.change_presence(
#         activity = discord.Activity(type=discord.ActivityType.watching, name=bot.streamer.status())
#     )

bot.run(creds['bot_token'])
