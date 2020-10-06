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
Configuration needs to be in JSON format with the following values:
* `interval` (string): Specify the interval at which the service is run. Values are natural language strings like `5 seconds`. Allowed values: `second, seconds, minute, minutes, hour, hours`. `1 seconds` is considered acceptable, as is `5 hour`. There is a minimum enforced interval of 1 second. The number must be an integer
* `urls` (array): This array contains objects with the following values:
  * `url` (string): URL to be checked.
  * Second value whose key can be either `status` or `content`:
    * `status` (int): Request is considered successful if the response status is the value specified here.
    * `content` (string): Response body contains this string.
