from typing import Dict
import aiohttp
import asyncio
import logging
import time

logger = logging.getLogger()

class Request:
  # PUBLIC VARIABLES AND METHODS

  # Dict of prime numbers (!1) to designate whether the response was as desired
  # A status of 15 means that both response status and content failed checks
  requestResult = {
    'none': 1,
    'success': 2,
    'status': 3,
    'content': 5,
    'error': 7
  }

  def __init__(self, url: Dict):
    self.__url = url['url']
    self.__status = url['status'] if 'status' in url else None
    self.__content = url['content'] if 'content' in url else None
    self.__result = self.requestResult['none']
    self.__responseStatus = 'error'

  async def fetch(self, session: aiohttp.ClientSession, timeout: int) -> int:
    try:
      self.__startTime = time.monotonic()
      async with session.get(self.__url, timeout=timeout) as response:
        # Setting the request time here in case reading the response is slow
        self.__setRequestTime()
        await self.__checkSuccess(response)
    except aiohttp.client_exceptions.ClientConnectorError:
      self.__responseError('Connection refused')
    except asyncio.exceptions.TimeoutError:
      self.__responseError('Request timed out')
    except:
      self.__responseError('Connection error (not timeout or refusal)')
    finally:
      self.__setRequestTime()
      self.__log()
      return self.__result

  # PRIVATE METHODS

  def __setRequestTime(self):
    """
    Set the total response time.
    """
    # Successful requests will already have set this before reading the response
    if not hasattr(self, '__time'):
      endTime = time.monotonic()
      self.__time = endTime - self.__startTime

  async def __checkSuccess(self, response: aiohttp.client_reqrep.ClientResponse):
    self.__responseStatus = response.status
    
    # Check that response status matches specified status
    if self.__status and self.__status != response.status:
      self.__result = self.__result * self.requestResult['status']

    # Check that response content contains specified content
    if self.__content:
      responseContent = await response.read()
      if self.__content.encode(encoding='UTF-8') not in responseContent:
        self.__result = self.__result * self.requestResult['content']

    if self.__result == self.requestResult['none']:
      self.__result = self.requestResult['success']

  def __responseError(self, reason: str):
    self.__error = reason
    self.__result = self.requestResult['error']

  def __log(self):
    """
    Commit this request to the log
    """
    if self.__result == self.requestResult['error']:
      logger.error(str(self))
    elif not self.__result % self.requestResult['status'] or\
    not self.__result % self.requestResult['content']:
      logger.warning(str(self))
    elif self.__result == self.requestResult['success']:
      logger.info(str(self))
    else:
      # This should only trigger if someone modifies this file improperly
      logger.critical(str(self))

  # I suppose this is technically public but it shouldn't be used outside
  # because it depends on values that are may not be finalised yet
  def __str__(self) -> str:
    if self.__result == self.requestResult['error']:
      reason = self.__error

    elif not self.__result % self.requestResult['status'] and\
    not self.__result % self.requestResult['content']:
      reason = 'Both status and content checks failed. '\
      f'Expected {self.__status}, \'{self.__content}\''

    elif not self.__result % self.requestResult['status']:
      reason = 'Server responded with wrong status. '\
      f'Expected {self.__status}'

    elif not self.__result % self.requestResult['content']:
      reason = 'Expected content not found in response. '\
      f'Expected \'{self.__content}\''
    
    elif self.__result == self.requestResult['success']:
      reason = 'Success'

    else:
      reason = 'Request.__result is set incorrectly, status undefined.'\
      'Fix src/classes/Request.py'

    return '\t'.join([
      f'URL={self.__url}',
      f'STATUS={self.__responseStatus}',
      f'TIME={self.__time:.3f}',
      f'MSG={reason}'
    ])
