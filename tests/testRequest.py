import unittest
import sys
from aiohttp import ClientSession

sys.path.append('../src')

from classes.Request import Request

class TestRequest(unittest.IsolatedAsyncioTestCase):
  """
  Apparently this uses some deprecated functionality so the logs are pretty
  wild, but it works
  """
  async def testValid(self):
    url = {'url': 'https://google.com'}
    request = Request(url)
    async with ClientSession() as session:
      self.assertEqual(await request.fetch(session, 2), Request.requestResult['success'])

  async def testValidStatus(self):
    url = {'url': 'https://google.com', 'status': 200}
    request = Request(url)
    async with ClientSession() as session:
      self.assertEqual(await request.fetch(session, 2), Request.requestResult['success'])

  async def testValidContent(self):
    url = {'url': 'https://google.com', 'content': 'html'}
    request = Request(url)
    async with ClientSession() as session:
      self.assertEqual(await request.fetch(session, 2), Request.requestResult['success'])

  async def testValidContentAndStatus(self):
    url = {'url': 'https://google.com', 'content': 'html', 'status': 200}
    request = Request(url)
    async with ClientSession() as session:
      self.assertEqual(await request.fetch(session, 2), Request.requestResult['success'])
  
  async def testStatusWarning(self):
    url = {'url': 'https://google.com', 'content': 'html', 'status': 201}
    request = Request(url)
    async with ClientSession() as session:
      self.assertEqual(await request.fetch(session, 2), Request.requestResult['status'])

  async def testContentWarning(self):
    url = {'url': 'https://google.com', 'content': 'RANDOM_STRING_34382583tng348gfqasd', 'status': 200}
    request = Request(url)
    async with ClientSession() as session:
      self.assertEqual(await request.fetch(session, 2), Request.requestResult['content'])

  async def testStatusAndContentWarning(self):
    url = {'url': 'https://google.com', 'content': 'RANDOM_STRING_34382583tng348gfqasd', 'status': 201}
    request = Request(url)
    async with ClientSession() as session:
      self.assertEqual(
        await request.fetch(session, 2),
        Request.requestResult['status'] * Request.requestResult['content']
      )

  async def testInvalid(self):
    url = {'url': 'https://google.com:81'}
    request = Request(url)
    async with ClientSession() as session:
      self.assertEqual(await request.fetch(session, 2), Request.requestResult['error'])

  async def testInvalidRefused(self):
    url = {'url': 'http://localhost:60001'}
    request = Request(url)
    async with ClientSession() as session:
      self.assertEqual(await request.fetch(session, 2), Request.requestResult['error'])

if __name__ == '__main__':
  unittest.main()
