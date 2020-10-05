import sys

from classes.Config import Config

def websiteStatus(configPath: str):
  config = Config(configPath)
  print(config.parseConfig())


if __name__ == '__main__':
  """
  CLI use
  """
  if len(sys.argv) != 2:
    print(f'Configuration file path must be provided (e.g. python3 {__file__} '
    '/path/to/cfg). Exiting.')
    sys.exit()
  
  websiteStatus(sys.argv[1])
  