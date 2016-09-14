"""
The main script for the agent. Run this to make a single trade. Create a
cronjob to run this periodically (i.e. every minute, 10 minutes, hour, etc.
that the market is open).

Be sure to create a config file called `config.ini` as specified in README.md
to read in the authentication information (agent id, username, and password) in
order to connect to the TDF.

If you cannot import `configparser`, make sure that you are running Python 3.
"""
from sample_agent import SampleAgent
import configparser
import os

URL = 'http://45.56.15.67:8680'  # TODO switch to production when ready


if __name__ == '__main__':
    # Read authentication information

    # Need to fetch an absolute path of the config file relative to the current
    # file so that an execution of this script from another location (such as
    # by a crontab) will not lose the loction of the config.
    config_loc = os.path.join(os.path.dirname(__file__), 'config.ini')

    config = configparser.ConfigParser()
    config.read(config_loc)

    agent = SampleAgent(config, URL)
    agent.execute()
