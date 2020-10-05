import sys
import urllib.request
import logging
import asyncio

from classes.Config import Config
from classes.RequestMaker import RequestMaker

logging.basicConfig(
  level=logging.NOTSET
)
logger = logging.getLogger()

async def websiteStatus(configPath: str):
  configObj = Config(configPath)
  requestMaker = RequestMaker(configObj)
  await requestMaker.run()

if __name__ == '__main__':
  """
  CLI use
  """
  if len(sys.argv) != 2:
    sys.exit('Configuration file path must be provided'
    f'(e.g. python3 {__file__} /path/to/cfg). Exiting.')

  try:
    # Checking that configuration can be loaded properly at start
    configObj = Config(sys.argv[1])
    config = configObj.parseConfig()
  except Exception as e:
    sys.exit('Encountered error upon initial configuration load:\n'
    f'{e}\n'
    'Exiting.')
  
  asyncio.run(websiteStatus(sys.argv[1]))
  