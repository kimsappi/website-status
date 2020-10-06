import sys
import logging
import asyncio
import time
from pathlib import Path

from classes.Config import Config
from classes.RequestMaker import RequestMaker

logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger()
logging.getLogger('asyncio').disabled = True

async def websiteStatus(configPath: str):
  while True:
    try:
      configObj = Config(configPath)
      requestMaker = RequestMaker(configObj)
      timeToSleep = await requestMaker.run()
    except Exception as e:
      timeToSleep = 60
      try:
        logger.critical(e)
      except:
        print('Critical error: cannot write to log file')
    finally:
      time.sleep(timeToSleep)

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
  