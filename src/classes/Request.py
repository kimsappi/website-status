from __future__ import annotations

from typing import Dict
import aiohttp
import asyncio
import time

class Request:

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

  def __setRequestTime(self):
    """
    Set the total response time.
    """
    # Successful requests will already have set this before reading the response
    if not hasattr(self, '__time'):
      endTime = time.monotonic()
      self.__time = endTime - self.__startTime

  async def __checkSuccess(self, response: aiohttp.client_reqrep.ClientResponse):
    # Check that response status matches specified status
    if self.__status and self.__status != response.status:
      self.__result = self.__result * self.requestResult['status']

    # Check that response content contains specified content
    if self.__content:
      responseContent = await response.read()
      if self.__content not in responseContent:
        self.__result = self.__result * self.requestResult['content']

  def __responseError(self, reason: str):
    self.__error(reason)
    self.__result = self.requestResult['error']

  async def fetch(self, session: aiohttp.ClientSession) -> Request:
    try:
      self.__startTime = time.monotonic()
      async with session.get(self.__url, timeout=10) as response:
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
      return self

  def __str__(self) -> str:
    return 'data about request'
