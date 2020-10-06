import unittest
import sys

sys.path.append('../src')

from classes.IntervalParser import IntervalParser

class TestIntervalParser(unittest.TestCase):
  def testSeconds(self):
    self.assertEqual(0, IntervalParser('0 second'))
    self.assertEqual(1, IntervalParser('1 second'))
    self.assertEqual(1, IntervalParser('1 seconds'))
    self.assertEqual(5, IntervalParser('5 seconds'))
    self.assertEqual(35949563543, IntervalParser('35949563543 second'))

  def testMinutes(self):
    self.assertEqual(0, IntervalParser('0 minutes'))
    self.assertEqual(1 * 60, IntervalParser('1 minute'))
    self.assertEqual(1 * 60, IntervalParser('1 minutes'))
    self.assertEqual(5 * 60, IntervalParser('5 minutes'))
    self.assertEqual(549743565 * 60, IntervalParser('549743565 minute'))

  def testHours(self):
    self.assertEqual(0, IntervalParser('0 hour'))
    self.assertEqual(1 * 60 * 60, IntervalParser('1 hour'))
    self.assertEqual(1 * 60 * 60, IntervalParser('1 hours'))
    self.assertEqual(5 * 60 * 60, IntervalParser('5 hours'))
    self.assertEqual(7433 * 60 * 60, IntervalParser('7433 hour'))

  def testNegative(self):
    # While negative numbers are acceptable, a minimum interval is enforced
    self.assertEqual(-5, IntervalParser('-5 seconds'))
    self.assertEqual(-13 * 60, IntervalParser('-13 minute'))
    self.assertEqual(-991 * 60 * 60, IntervalParser('-991 hour'))

  def testFloat(self):
    self.assertRaises(Exception, IntervalParser, '0.1 seconds')
    self.assertRaises(Exception, IntervalParser, '1.1 minutes')
    self.assertRaises(Exception, IntervalParser, '17.1 hour')
    self.assertRaises(Exception, IntervalParser, '-27.1 minute')

  def testInvalid(self):
    self.assertRaises(Exception, IntervalParser, '')
    self.assertRaises(Exception, IntervalParser, '1')
    self.assertRaises(Exception, IntervalParser, '1minutes')
    self.assertRaises(Exception, IntervalParser, '1 minutes 2')
    self.assertRaises(Exception, IntervalParser, '1 min')
    self.assertRaises(Exception, IntervalParser, 1)
    self.assertRaises(Exception, IntervalParser, b'1 minute')

if __name__ == '__main__':
  unittest.main()
