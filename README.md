# About
Service that checks that websites/URLs listed in a specified configuration file respond correctly.

# Requirements
* Python 3 (>=3.6 I believe, for f-string support) & pip
* Python `venv` or similar recommended

# Instructions
```shell
git clone http://github.com/kimsappi/website-status.git
cd website-status

# The following block is optional: virtual environment setup
python3 -m venv env
source env/bin/activate

pip3 install -r requirements.txt
python3 app.py /path/to/config # path can also be a URL to a JSON file
```

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

# Considerations
* Timing may break completely if more than 100 URLs (`aiohttp` default simultaneous connections) are added. Lower-level tinkering would be needed to figure out when requests are actually made.
* I'm sure better separation of concerns is possible, e.g. logging for a specific request is made inside `Request.fetch()` itself. However, this was my first attempt as async Python so I wasn't entirely sure how that could be possible while keeping the logging real-time.
