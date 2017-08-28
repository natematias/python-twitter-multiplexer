# Python Twitter Multiplexer
This project offers stub code for wrapping python-twitter to use tokens from multiple users when querying the Twitter API. This is a common pattern for many apps that use the Twitter API, and it's a basic part of the functionality for the code behind [CivilServant](https://civilservant.io), which uses API access to support citizen testing of ideas for improving social experiences online.

This project is in alpha stage and will probably not receive close attention or maintenance. However, I hope it will be useful to others who need to use this design pattern in your own projets.

## Requirements
(from requirements.txt)
* pytest
* python-twitter
* logging
* cloghandler
* retrying
* mock

## How To Use This Project
This project has two parts. Use https://github.com/natematias/Donate-API-Access as an example for collecting donated API tokens in the first place. Then use this code to use the pool of tokens to query the Twitter API. In this public example, we use in-memory tracking and configuration files. In CivilServant and in your project, you may want to store tokens and token state in a database where they can be dynamically added/removed, etc. 

To set up the software

1. Use Donate-API-Access to collect tokens
2. Copy [config/configuration_environment.json.example](https://github.com/natematias/python-twitter-multiplexer/blob/master/config/configuration_environment.json.example) to config/configuration_development.json
3. Add the path of the tokens to configuration_development.json (can be absolute or relative)
4. Copy [config/twitter_auth_environment.json.example](https://github.com/natematias/python-twitter-multiplexer/blob/master/config/twitter_auth_environment.json.example) to config/twitter_auth_development.json
5. Add your app's `consumer_secret` and `consumer_key` to the configuration file
6. run `py.test tests` to confirm that all is working

## Other notes
* Logs are stored (and log-rotated in) logs/

