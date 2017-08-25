import simplejson as json
import os, sys, glob, random, datetime, time, inspect
import twitter
import app.cs_logger

ENV =  os.environ['CS_ENV']


class TwitterConnect():
    def __init__(self, log=None):
        BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), "../..")

        ## LOAD LOGGER
        if(log):
            self.log = log
        else:
            self.log = app.cs_logger.get_logger(ENV, BASE_DIR)
        
        ## LOAD INFORMATION ABOUT KEYS (relative or absolute path)
        config_path = os.path.join(BASE_DIR, "config", "configuration_" + ENV + ".json")
        with open(config_path, "r") as config:
            self.config = json.loads(config.read())
        if(self.config['key_path'][0] == "/"):
            token_path = self.config['key_path']
        else:
            token_path = os.path.join(BASE_DIR, self.config['key_path'])

        self.tokens = []
        for filename in glob.glob(os.path.join(token_path, "*.json")):
            with open(filename, "r") as f:
                token = json.loads(f.read())
                token["valid"] = True
                token["available"] = True
                token["next_available"] = None
            self.tokens.append(token)

        ## LOAD BASE CONFIGURATION INFORMATION
        twitter_config_path = os.path.join(BASE_DIR, "config", "twitter_auth_" + ENV + ".json")
        with open(twitter_config_path, 'r') as t_config:
            twitter_config = json.loads(t_config.read())
        self.consumer_key = twitter_config["consumer_key"]
        self.consumer_secret = twitter_config["consumer_secret"]

        token = self.select_available_token()
        if(self.apply_token(token)):
            self.log.info("Twitter API connection verified under ID {0}".format(self.token['user_id']))

    ## This method takes a token and tries to adjust the API to query using the token
    def apply_token(self, token):
        self.api = twitter.Api(consumer_key = self.consumer_key,
                               consumer_secret = self.consumer_secret,
                               access_token_key = token['oauth_token'],
                               access_token_secret = token['oauth_token_secret'])
        try:
            verification = self.api.VerifyCredentials()
        except TwitterError as e:
            self.log.error("Twitter: Failed to connect to API with User ID {0}. Remove from token set. Error: {1}.".format(token['user_id'], str(e)))
            token['valid'] = False
            self.token = None
            return False
        self.token = token
        return True

    ## This method will randomly select from available tokens
    ## or if no tokens are available, wait until the next token 
    ## becomes available, based on information from the Twitter API
    ## then return that token
    def select_available_token(self):
        available_token = random.choice([token for token in self.tokens if (token['available'] and token['valid'])])
        if(available_token is None):
            available_token = sorted(self.tokens, key=lambda x: x['next_available'])[0]
            if(available_token is None):
                self.log.error("Twitter: failed to find any valid tokens. Ending process.")
                sys.exit("Twitter: failed to find any valid tokens. Ending process")

            seconds_until_available = (available_token['next_available'] - datetime.datetime.utcnow()).total_seconds()
            time.sleep(seconds_until_available)
        return available_token
