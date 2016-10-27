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
from sample_agent import LstmAgent
import configparser
import os

URL = 'http://45.56.15.67:8680'


def agent_factory(config, url=None, **kwargs):
    """Builds and returns an agent.

    Required if the agent manager is to be used. Helpful even if not.

    Parameters
    ----------
    config : object
        Contains key 'TDFConnect' with another object. This other object
        contains keys 'email', 'password', and 'id'. Reading the `config.ini`
        as specified by the documentation will create such an object. The
        agent manager will also create such an object.
    url : str, default=None
        The url of the TDF instance to which to connect. If None, uses the
        default TDF location.
    **kwargs : key word arguments
        Optional key word arguments to pass in to the agent. Used only by
        the agent manager.
    """
    if url is None:
        url = URL

    #agent = SampleAgent(config, url)
    agent = LstmAgent(config, url)
    return agent


if __name__ == '__main__':
    # Read authentication information

    # Need to fetch an absolute path of the config file relative to the current
    # file so that an execution of this script from another location (such as
    # by a crontab) will not lose the loction of the config.
    config_loc = os.path.join(os.path.dirname(__file__), 'config.ini')

    config = configparser.ConfigParser()
    config.read(config_loc)

    agent = agent_factory(config, URL)
    agent.update_lstm_models()
