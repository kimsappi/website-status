import asyncio
from flask import Flask, render_template
import threading
import logging

from app import websiteStatus

app = Flask(__name__)

responseTypeSortKey = {
  'INFO': 9,
  'WARNING': 5,
  'ERROR': 0,
  'CRITICAL': 0
}

def columnSplitter(column: str) -> str:
  arr = column.split('=')
  if len(arr) > 1:
    return '='.join(arr[1:])
  return ''

@app.route('/')
def index():
  startTime = 'placeholder'
  with open('log', 'r') as f:
    lines = f.readlines()
  for i in range(len(lines) - 1, 0, -1):
    cols = lines[i].split('\t')
    if len(cols) > 2 and cols[2].startswith('COMPLETED'):
      break
  if not len(lines) or i < 1:
    return render_template('_error.html')
  selectedRows = []
  for j in range(i - 1, 0, -1):
    cols = lines[j].split('\t')
    if len(cols) > 2 and cols[2].startswith('STARTING'):
      startTime = cols[0]
      break
    elif len(cols) > 2 and not cols[2].startswith('STARTING'):
      if cols[2].startswith('URL') and cols[3].startswith('STATUS'):
        selectedRows.append({
          'url': columnSplitter(cols[2]),
          'status': columnSplitter(cols[3]),
          'time': columnSplitter(cols[4]),
          'msg': columnSplitter(cols[5]),
          'responseType': cols[1]
        })
  if not len(selectedRows):
    return render_template('_error.html')

  selectedRows.sort(key=lambda row: float(row['time']), reverse=True)
  selectedRows.sort(key=lambda row: responseTypeSortKey[row['responseType']])
  return render_template(
    '_index.html',
    startTime=startTime,
    sites=selectedRows
  )

@app.route('/history/<url>')
def history(url: str):
  url = url.replace('@@SLASH@@', '/')
  with open('log', 'r') as f:
    lines = f.readlines()
  selectedRows = []
  for i in range(len(lines) - 1, 0, -1):
    cols = lines[i].split('\t')
    if len(cols) > 2 and cols[2] == f'URL={url}':
      selectedRows.append({
        'date': cols[0],
        'url': columnSplitter(cols[2]),
        'status': columnSplitter(cols[3]),
        'time': columnSplitter(cols[4]),
        'msg': columnSplitter(cols[5]),
        'responseType': cols[1]
      })
  if not len(selectedRows):
    return render_template('_error.html')
  else:
    return render_template('_history.html', rows=selectedRows)

@app.route('/raw')
def raw():
  with open('log', 'r') as f:
    return f.read()

def startStatus(configPath):
  asyncio.run(websiteStatus(configPath))

if __name__ == '__main__':
  flaskLogger = logging.getLogger('werkzeug')
  flaskLogger.disabled = True
  statusThread = threading.Thread(target=startStatus, args=['config.json'])
  statusThread.start()
  app.run(host='localhost', port=3000)
