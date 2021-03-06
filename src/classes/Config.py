import json
import errno
import urllib.request
import logging
import time

from .LogFormat import LogFormat

class Config:
  """
  Configuration file parser
  """
  # PUBLIC METHODS

  def __init__(self, path: str):
    self.__path = path
    self.__url = True if path.startswith('http') else False

  def parseConfig(self):
    if not self.__url:
      config = self.__readLocalFile()
    else:
      config = self.__readFromWeb()
    
    try:
      config = json.loads(config)
    except:
      raise Exception('Configuration file could not be read as JSON. '\
      'Please check the formatting.')

    # Setting log location to path specified in config
    try:
      newLogFileHandler = logging.FileHandler(config['logPath'], 'a')
      formatter = logging.Formatter(LogFormat())
      formatter.converter = time.gmtime
      newLogFileHandler.setFormatter(formatter)
    except Exception as e:
      try:
        raise Exception(f'Cannot write to new log path: {config["logPath"]}')
      except:
        raise Exception('No "logPath" in configuration file')
    logger = logging.getLogger()
    for handler in logger.handlers[:]:
      logger.removeHandler(handler)
    logger.addHandler(newLogFileHandler)
    return config

    # PRIVATE METHODS
  
  def __readLocalFile(self):
    """
    Read a configuration that is a local file as opposed to a file on the web.
    """
    try:
      with open(self.__path) as f:
        return f.read()
    except IOError as err:
      if err.errno == errno.ENOENT:
        raise IOError(f'Could not find configuration file \'{self.__path}\'')
      elif err.errno == errno.EACCES:
        raise IOError('Configuration file found but unreadable')
      else:
        raise Exception('Something went wrong when reading the file')
    except:
      raise Exception('Something went wrong when reading the file (!IOError)')

  def __readFromWeb(self):
    """
    Read a configuration file from the web
    """
    try:
      return urllib.request.urlopen(self.__path).read()
    except:
      raise Exception('Could not open configuration URL.')
    