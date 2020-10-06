import time
import asyncio
from aiohttp import ClientSession

from .Config import Config
from .Request import Request

class RequestMaker:
  def __init__(self, config: Config):
    self.__startTime = time.monotonic()
    try:
      self.__config = config.parseConfig()
    except:
      raise Exception('Couldn\'t read config')

  async def run(self):
    tasks = []
    async with ClientSession() as session:
      for target in self.__config['urls']:
        request = Request(target)
        task = asyncio.ensure_future(request.fetch(session))
        tasks.append(task)

      results = await asyncio.gather(*tasks)
      endTime = time.monotonic()
