from typing import List
import time
import asyncio
import logging
from aiohttp import ClientSession

from .Config import Config
from .Request import Request
from .IntervalParser import IntervalParser

logger = logging.getLogger()

def filterRequestReturnValue(requestResult: int, *args: int) -> bool:
  """
  Filter function for filtering the results array to successes, warnings, errors
  """
  for mod in args:
    if not requestResult % mod:
      return True
  return False

class RequestMaker:
  DEFAULT_INTERVAL = 60
  DEFAULT_TIMEOUT = 10

  def __init__(self, config: Config):
    try:
      self.__config = config.parseConfig()
    except Exception as e:
      raise Exception(f'Couldn\'t read config: {e}')

    try:
      if hasattr(self.__config, 'interval'):
        self.__config['interval'] = IntervalParser(self.__config['interval'])
      else:
        raise Exception('Interval not found in configuration file')
    except Exception as e:
      self.__config['interval'] = self.DEFAULT_INTERVAL
      logger.error(f'Falling back to default interval {self.DEFAULT_INTERVAL} '
      f'seconds: {e}')
    self.__timeout = (
      self.__config['timeout'] if 'timeout' in self.__config
        else self.DEFAULT_TIMEOUT
    )

  def __calculateClassTotals(self, results: List[int]):
    """
    Calculating total amount of results in each class
    """
    successTotal = len(list(filter(
      lambda arr: filterRequestReturnValue(arr, Request.requestResult['success']),
      results
    )))

    errorTotal = len(list(filter(
      lambda arr: filterRequestReturnValue(arr, Request.requestResult['error']),
      results
    )))

    warningTotal = len(list(filter(
      lambda arr: filterRequestReturnValue(
        arr, Request.requestResult['status'], Request.requestResult['content']
      ),
      results
    )))

    self.__totals = {
      'success': successTotal,
      'warning': warningTotal,
      'error': errorTotal
    }

  async def run(self) -> int:
    """
    Handles making requests asynchronously. Returns time to sleep
    """
    logger.info(f'STARTING {len(self.__config["urls"])} requests')
    tasks = []
    startTime = time.monotonic()
    async with ClientSession() as session:
      for target in self.__config['urls']:
        request = Request(target)
        task = asyncio.ensure_future(request.fetch(session, self.__timeout))
        tasks.append(task)

      results = await asyncio.gather(*tasks)
      self.__calculateClassTotals(results)

      logger.info('\t'.join([
        f'COMPLETED {len(results)} requests.',
        f'ERROR={self.__totals["error"]}',
        f'WARNING={self.__totals["warning"]}',
        f'SUCCESS={self.__totals["success"]}'
      ]))

      endTime = time.monotonic()

      # Enforce a minimum interval of 1 second after completion of this round
      return max(
        self.__config['interval'] - (endTime - startTime),
        1
      )
