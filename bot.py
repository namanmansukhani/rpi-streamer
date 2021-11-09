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

@bot.command()
async def anime(ctx, *, anime):
    results = await bot.streamer.search_anime(anime)
    anime_name = results['name']
    anime_names = results['titles']
    links = results['links']

    embed = discord.Embed(name = ctx.author.display_name, icon_url=ctx.author.avatar_url, title = f"{anime_name.title()} - {len(links)} Search Results", color = discord.Color.green())
    embed.set_thumbnail(url="https://gogoanime.vc/img/icon/logo.png")
    if len(links) == 0:
        embed.colour = discord.Color.red()

    for i in range(len(anime_names)):
        embed.add_field(name= f'{i+1}. {anime_names[i]}', value='\u200b')
    
    await ctx.send(embed = embed)

    n = len(anime_names)
    response_message = await get_response_message(bot, ctx.author, ctx.channel, lambda x: x.isdigit() and 0 < int(x) <= n)
    selection = int(response_message.content)

    show_link = links[selection-1]
    num_episodes = await bot.streamer.get_num_episodes(show_link)
    await ctx.send(f'Choose an episode: 1 to {num_episodes}')
    
    response_message = await get_response_message(bot, ctx.author, ctx.channel, lambda x: x.isdigit() and 0 < int(x) <= num_episodes)
    ep_number = int(response_message.content)

    episode_base_link = show_link.replace('/category', '')
    episode_link = f'{episode_base_link}-episode-{ep_number}'

    await ctx.send(f'{episode_link}')

    details = await bot.streamer.stream_details(episode_link)
    await ctx.send(f'```{json.dumps(details)}```')

@bot.command()
async def ne(ctx, url):
    print(await bot.streamer.get_num_episodes(url))

bot.run(creds['bot_token'])
