import asyncio, aiohttp
import re
from bs4 import BeautifulSoup

class Streamer:
    def __init__(self):
        pass

    async def search_anime(self, anime_name):
        # anime_name = ' '.join(anime_name)
        og_anime_name = anime_name
        anime_name = r'%20'.join(anime_name.lower().split())
        url = f"https://gogoanime.vc//search.html?keyword={anime_name}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    text = await response.text()
                    # print(html)
                    soup = BeautifulSoup(text, 'html.parser')
                    list_elements = str(soup.find_all("ul", class_ = "items"))
                    anime_names = re.findall('alt=\".*?\"', list_elements)
                    anime_names = [i[5:-1] for i in anime_names]

                    links = re.findall('a href=\"/.*?\"', list_elements)
                    links = [i[8:-1] for i in links]
                    links = ["https://gogoanime.vc" + links[i] for i in range(0, len(links), 2)]

                    image_links = re.findall('src="(https:\/\/gogocdn.net\/.*?)"', list_elements)
                    release_years = re.findall('Released: (\d{4})', list_elements)
        
        return {
            'name': og_anime_name,
            'titles' : anime_names,
            'links' : links,
            'image_links' : image_links,
            'release_years' : release_years,
        }

    async def get_num_episodes(self, anime_url):
        async with aiohttp.ClientSession() as session:
            async with session.get(anime_url) as response:
                if response.status == 200:
                    text = await response.text()
                    soup = BeautifulSoup(text, 'html.parser')
                    number_of_episodes = soup.find(id = 'episode_page').find('a')['ep_end']
                    return int(number_of_episodes)
    
    async def stream_details(self, episode_link):
        async with aiohttp.ClientSession() as session:
            async with session.get(episode_link) as response:
                if response.status == 200:
                    text = await response.text()
                    # print(html)
                    soup = BeautifulSoup(text, 'html.parser')
                    referer = 'https:' + soup.find("li",class_="vidcdn").a['data-video']

        async with aiohttp.ClientSession() as session:
            async with session.get(referer) as response:
                if response.status == 200:
                    text = await response.text()
                    soup = BeautifulSoup(text, 'html.parser')
                    js_script = str(soup.find("div", class_="videocontent").script)
                    manifest = re.findall("file: '(http.*?\.m3u8)'", js_script)[0]
        
        return {
            'referer': referer,
            'manifest': manifest,
        }