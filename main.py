"""
The main script for the agent. Run this to make a single trade. Create a
cronjob to run this periodically (i.e. every minute, 10 minutes, hour, etc.
that the market is open).

Be sure to create a config file called `config.ini` to read in the
authentication information (agent id, username, and password) in order to
connect to the TDF.

The email and password are the same that you use to log in to the TDF
website. The agent id can be found on the TDF website. Look for your agent
either on the dashboard or on the "My Agents" page under the league in which
it is registered (you may need to expand the "My Agents" section in the
league panel). Click on the "Edit" button next to the agent. The id is found
on the first row in the "Current Status" panel.

Git is configured to ignore the config file so that your password in the config
file is not pushed to the cloud. However, for security, you should use a
password that is unique to TDF. If you need to change your password, you can
do so at the TDF website on the "Profile" page.

The `config.ini` file should look like this (replacing the information with
your own authentication):

    [TDFConnect]
    agent_id : 42
    email : myemail@example.com
    password : themeaningoflife

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
