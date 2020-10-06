import logging

# class LogFormatter(logging.Formatter):
#   FORMATS = {
#     logging.INFO: DEFAULT_FORMAT,
#     logging.WARNING: DEFAULT_FORMAT,
#     logging.ERROR: DEFAULT_FORMAT,
#     logging.CRITICAL: DEFAULT_FORMAT,
#     'default': '%(asctime)s\tUNDEFINED\t%(message)s',
#   }

#   def __init__(self):
#     logging.Formatter.__init__(self)

#   def format(record):
#     return logging.Formatter.format(
#       self,
#       LogFormatter.FORMATS.get(
#         record.levelno,
#         LogFormatter.FORMATS['default']
#       )
#     )

class LogFormat:
  def __new__(cls) -> str:
    return '%(asctime)s\t%(levelname)s\t%(message)s'
