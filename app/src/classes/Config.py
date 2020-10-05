import json
import urllib.request

class Config:
  """
  Configuration file parser
  """
  def __init__(self, path: str):
    self.__path = path
    self.__url = True if path.startswith('http') else False

  def readLocalFile(self):
    """
    Read a configuration that is a local file as opposed to a file on the web.
    """
    try:
      with open(self.__path) as f:
        return f.read()
    except IOError as err:
      if x.errno == errno.ENOENT:
        raise Exception(f'Could not find configuration file \'{self.__path}\'')
      if x.errno == errno.EACCES:
        raise Exception('Configuration file found but unreadable')
    except:
      raise Exception('Something went wrong when reading the file')

  def readFromWeb(self):
    """
    Read a configuration file from the web
    """
    try:
      return urllib.request.urlopen(self.__path).read()
    except:
      raise Exception('Could not open configuration URL.')

  def parseConfig(self):
    if not self.__url:
      config = self.readLocalFile()
    else:
      config = self.readFromWeb()
    
    try:
      return json.loads(config)
    except:
      raise Exception('Configuration file could not be read as JSON. '
      'Please check the formatting.')
