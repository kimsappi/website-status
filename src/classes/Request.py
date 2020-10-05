from typing import Dict
from aiohttp import ClientSession

class Request:
  def __init__(self, url: Dict):
    self.__url = url['url']
    self.__status = url['status'] if 'status' in url else None
    self.__content = url['content'] if 'content' in url else None

  async def fetch(self, session: ClientSession):
    async with session.get(self.__url, timeout=10) as response:
      print(response)
