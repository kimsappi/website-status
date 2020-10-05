# About
Service that checks that websites/URLs listed in a specified configuration file respond correctly.

# Configuration
Configuration needs to be in JSON format with the following values:
* `interval` (string): Specify the interval at which the service is run. Values are natural language strings like `5 seconds`. Allowed values: `second, seconds, minute, minutes, hour, hours`. `1 seconds` is considered acceptable, as is `5 hour`. There is a minimum enforced interval of 1 second. The number must be an integer
* `urls` (array): This array contains objects with the following values:
  * `url` (string): URL to be checked.
  * Second value whose key can be either `status` or `content`:
    * `status` (int): Request is considered successful if the response status is the value specified here.
    * `content` (string): Response body contains this string.
