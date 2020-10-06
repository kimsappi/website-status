import unittest
import sys
import pathlib
import json

sys.path.append('../src')

from classes.Config import Config

DIR = str(pathlib.Path(__file__).parent.absolute())
CONFIG_DIR = DIR + '/configFiles/'

class TestConfig(unittest.TestCase):
  def testValid(self):
    config = Config(CONFIG_DIR + 'valid1.json')
    with open(CONFIG_DIR + 'valid1.json') as f:
      configDict = json.loads(f.read())
    self.assertDictEqual(config.parseConfig(), configDict)

    try:
      config = Config('https://raw.githubusercontent.com/kimsappi/website-status/main/config.json')
      # This will apparently print some kind of warning, since the log file is never actually used. Oh well
      config = config.parseConfig()
    except:
      self.fail()

  def testInvalid(self):
    config = Config('/definitely/invalid/path')
    self.assertRaises(IOError, config.parseConfig)

    # This file is supposed to be valid, but its permissions should be set such
    # that it's unreadable (can't commit to git if I can't read it, though)
    config = Config(CONFIG_DIR + 'invalidPerm.json')
    self.assertRaises(IOError, config.parseConfig)

    config = Config(CONFIG_DIR + 'invalidLogpath.json')
    self.assertRaises(Exception, config.parseConfig)

    config = Config(CONFIG_DIR + 'invalidJson.json')
    self.assertRaises(Exception, config.parseConfig)

    config = Config('https://example.com/hopefully404')
    self.assertRaises(Exception, config.parseConfig)

if __name__ == '__main__':
  unittest.main()
