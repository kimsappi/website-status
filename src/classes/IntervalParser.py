allowedIntervals = ['second', 'seconds', 'minute', 'minutes', 'hour', 'hours']

class IntervalParser:
  """
  Returns number of seconds interval given as string (e.g. '5 seconds',
  '1 hour').
  """
  def __new__(cls, interval: str) -> int:
    try: 
      arr = interval.split(' ')
    except:
      raise Exception('Time interval in invalid format')

    if len(arr) != 2:
      raise Exception('Time interval in invalid format (e.g. \'5 seconds\')')
    
    if arr[1] not in allowedIntervals:
      raise Exception(' '.join([
        'Disallowed time interval. Allowed values:',
        ', '.join(allowedIntervals)
      ]))

    try:
      timeUnit = int(arr[0])
    except:
      raise Exception('Time interval must be in the format \'integer unit\'')
    
    arrPos = allowedIntervals.index(arr[1])
    secondMultiplier = 1
    if arrPos > 1:
      secondMultiplier *= 60
    if arrPos > 3:
      secondMultiplier *= 60

    return timeUnit * secondMultiplier

"""
There must be packages for this, but this is quite a limited application
and I'd prefer to know how it works in all situations.
"""
