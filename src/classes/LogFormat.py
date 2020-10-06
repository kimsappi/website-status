import logging

class LogFormat:
  def __new__(cls) -> str:
    return '%(asctime)s\t%(levelname)s\t%(message)s'
