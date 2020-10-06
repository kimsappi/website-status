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
python3 app.py /path/to/config
```

# Configuration
The configuration file **must not** be named `http*` if called with just the filename. If called with a path, file names can be acceptable. This is because a path starting with `http` is considered a URL.

Configuration needs to be in JSON format with the following values:
* `interval` (string): Specify the interval at which the service is run. Values are natural language strings like `5 seconds`. Allowed values: `second, seconds, minute, minutes, hour, hours`. `1 seconds` is considered acceptable, as is `5 hour`. There is a minimum enforced interval of 1 second. The number must be an integer.
* `logPath` (string): Specify the path of the file you wish the output to be logged to. File must be writable. This can be an absolute path or relative to the directory the app is run from.
* `urls` (array): This array contains objects with the following values:
  * `url` (string): URL to be checked.
  * Second value whose key can be either `status` or `content`:
    * `status` (int): Request is considered successful if the response status is the value specified here.
    * `content` (string): Response body contains this string.

# Considerations
* Timing may break completely if more than 100 URLs (`aiohttp` default simultaneous connections) are added. Lower-level tinkering would be needed to figure out when requests are actually made.
