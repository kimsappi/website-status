import sys
import urllib.request
import logging

from classes.Config import Config

logging.basicConfig(
  level=logging.NOTSET
)
logger = logging.getLogger()

def websiteStatus(configPath: str):
  try:
    # Checking that configuration can be loaded properly at start
    configObj = Config(configPath)
    config = configObj.parseConfig()  
  except Exception as e:
    sys.exit('Encountered error upon initial configuration load:\n'
    f'{e}\n'
    'Exiting.')


if __name__ == '__main__':
  """
  CLI use
  """
  if len(sys.argv) != 2:
    sys.exit('Configuration file path must be provided'
    f'(e.g. python3 {__file__} /path/to/cfg). Exiting.')
  
  websiteStatus(sys.argv[1])
  