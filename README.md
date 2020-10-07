# About
Service that checks that websites/URLs listed in a specified configuration file respond correctly. *Asynchronous requesting* makes things go quicker especially if many servers are slow to respond, although it may cause problems with if servers consider your requests to be spam.

There is also an extremely basic web interface available in the [flask branch](https://github.com/kimsappi/website-status/tree/flask). A version of the web interface is available [here](http://kimsappi-website-status.herokuapp.com/).

# Requirements
* Python 3.7 (for `asyncio.run`) & pip
  * Python 3.8 is required for `tests/testRequest` (`unittest.IsolatedAsyncioTestCase`)
* Python `venv` or similar recommended
* Python module `aiohttp` (+its dependencies) for asynchronous requests
* Python module `flask` (+its dependencies) for the optional web interface

# Instructions
## CLI interface
```shell
git clone http://github.com/kimsappi/website-status.git
cd website-status

# The following block is optional: virtual environment setup
python3 -m venv env
source env/bin/activate

pip3 install -r requirements.txt
python3 src/app.py /path/to/config # path can also be a URL to a JSON file

# Finally, you can run the tests if you want
./test.sh
```

## Web interface
```shell
git clone http://github.com/kimsappi/website-status.git
cd website-status

# The following block is optional: virtual environment setup
python3 -m venv env
source env/bin/activate

pip3 install -r requirements.txt
python3 src/web.py
```
This will start a web server at `http://localhost:3000`.

# Configuration
The configuration file **must not** be named `http*` if called with just the filename. If called with a path, file names can be acceptable. This is because a path starting with `http` is considered a URL.

Configuration needs to be in JSON format with the following values:
* `logPath` (string, **required**): Specify the path of the file you wish the output to be logged to. File must be writable. This can be an absolute path or relative to the directory the app is run from.
* `interval` (string, *optional* (but will log an error if not present or invalid), default 60 seconds): Specify the interval at which the service is run. Values are natural language strings like `5 seconds`. Allowed values: `second, seconds, minute, minutes, hour, hours`. `1 seconds` is considered acceptable, as is `5 hour`. There is a minimum enforced interval of 1 second. The number must be an integer.
* `timeout` (int, *optional*, default 10 seconds): Specify the request timeout time in seconds.
* `urls` (array, **required**): This array contains objects with the following values:
  * `url` (string): URL to be checked.
  * At least one of the following (technically neither is required, but in that case any response (even e.g. a 404) is considered a success):
    * `status` (int): Request is considered successful if the response status is the value specified here.
    * `content` (string): Response body contains this string.

# Log file format
The format of a request line is (columns are tab-separated):
`<datetime> <level> URL=<url> STATUS=<response status code || 'error'> TIME=<response time> MSG=<message about request success/failure>`

Each block starts and ends with an `INFO` line containing data about the block.
```
2020-10-07 04:53:36,848	INFO	STARTING 6 requests
2020-10-07 04:53:36,858	ERROR	URL=http://localhost:60000	STATUS=error	TIME=0.006	MSG=Connection refused
2020-10-07 04:53:37,115	INFO	URL=https://google.com	STATUS=200	TIME=0.267	MSG=Success
2020-10-07 04:53:37,174	WARNING	URL=http://example.com/thispageprobablydoesnotexist	STATUS=404	TIME=0.322	MSG=Server responded with wrong status. Expected 200
2020-10-07 04:53:37,186	INFO	URL=https://github.com	STATUS=200	TIME=0.335	MSG=Success
2020-10-07 04:53:37,265	WARNING	URL=https://stackoverflow.com	STATUS=200	TIME=0.414	MSG=Both status and content checks failed. Expected 404, 'This string will hopefully not be found 34ef4ewgsregrg'
2020-10-07 04:53:47,232	ERROR	URL=http://google.com:81	STATUS=error	TIME=10.380	MSG=Request timed out
2020-10-07 04:53:47,232	INFO	COMPLETED 6 requests.	ERROR=2	WARNING=2	SUCCESS=2
```

# Considerations
* I chose to reread the configuration on every run, so the surveyed websites can be changed dynamically and 
* `time.sleep()` probably isn't the ideal solution. A tool like `cron` or some external application controlling the requests would probably be a better solution.
* Timing may break completely if more than 100 URLs (`aiohttp` default simultaneous connections) are added. Lower-level tinkering would be needed to figure out when requests are actually made.
* I'm sure better separation of concerns is possible, e.g. logging for a specific request is made inside `Request.fetch()` itself. However, this was my first attempt as async Python so I wasn't entirely sure how that could be possible while keeping the logging real-time.
* Asynchronous requests may not be the best idea if multiple requests are directed at the same server, since they may be considered spam.
* The service could also be implemented as a daemon.

# Optional: Design question
Premise: "Responses and latencies need to be logged from several locations."

Instead of writing to a single log file or sending each log line to a central server ephemerally, it would make sense to propagate the data either via an API or database(s) to a central hub, from which the global data would then be accessible.

## API considerations
Each server could offer an API for the central server to poll. The API could be protected by an API key if sensitive.

## Database considerations
Each server could log their data to either a local (internet-connected) or global database server. Each server should have write access to a limited area. The central server can then query the (all of the) database(s) for the data it needs.
