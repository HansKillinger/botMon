from classicAPI import claim_all
from configparser import ConfigParser
from argparse import ArgumentParser

config = ConfigParser()

parser = ArgumentParser()
parser.add_argument("configfile", help="config file.ini to use")

if __name__ == '__main__':
    args = parser.parse_args()
    config.read(args.configfile)
    bot_settings = config['settings']
    wallet = bot_settings['wallet']
    sessionID = bot_settings['sessionid']
    print(claim_all(sessionID, wallet))
