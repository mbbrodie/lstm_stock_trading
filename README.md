## Description ##

In this agent, trades are made naively, by choosing the security with the
highest average returns over the last 10 minutes of collected data time period
and investing 95% of the portfolio value un that security (the remaining 5% in
cash).

This agent is designed to be a starting point for new python agents that trade
on the TDF. Either fork the repo or copy the code to make a new TDF agent.

## Installation - Ubuntu

NOTE: these instructions are written for Ubuntu 16.04. However, this code should
work on OS-X by following analogous installation procedures.

### Installing Python 3 ###

We also recommend that these agents run under a Python 3 environment (they
should work with Python 2.7 as well; however, this is not tested). To install
Python 3, its development toolkits, and other dependencies:

        $ sudo apt-get install python3 python3-dev python-pip libffi-dev

### Creating a Virtual Environment ###

We recommend that python TDF agents be installed within their own virtual
environments. The utility `mkvirtualenv` is a great tool to create such
virtual environments.

Follow the instructions at
<http://virtualenvwrapper.readthedocs.io/en/latest/install.html> to install the
virtual environment wrapper. In short:

        $ sudo pip install virtualenv virtualenvwrapper

You will need to configure your bash to find `mkvirtualenv`. To do this, add
the following 3 lines to your bash startup file (probably `.bashrc`, but
possibly also `.profile` or something else), changing PROJECT_HOME to suit
your preferences:

        export WORKON_HOME=$HOME/.virtualenvs
        export PROJECT_HOME=$HOME/Development
        source /usr/local/bin/virtualenvwrapper.sh

Then reload the bash startup script:

        $ source ~/.bashrc

Now find the location where Python 3 has been installed:

        $ which python3
        > /usr/bin/python3

Now create the environment:

        $ mkvirtualenv --python=/usr/bin/python3 myagent

The virtual environment will activate immediately on install. To exit the
virtual environment, simply use:

        $ deactivate

And to enter the virtual environment again, use:

        $ workon myagent

You can tell that you are in the virtual environment with the text `(myagent)`
at the far left of the bash lines.

If you want, you can configure the virtual environment to navigate to your
project directory on activation. To do this, while the virtual environment is
active, open `$VIRTUAL_ENV/bin/postactivate` in your favorite text editor and
add the following line:

        cd ~/path/to/myagent

Save and close. Test the script by deactivating and reactivating the virtual
environment:

        $ deactivate
        $ cd ~
        $ workon myagent

### Install `numpy`

Install `numpy` and `pandas` with (installation sometimes doesn't work well
with the setup.py develop script, so we will do it here first):

        pip install -U numpy pandas

### Install `pytdf-base-agent`

Install the `pytdf-base-agent` at <https://gitlab.com/idealabs/pytdf-base-agent>
while within the virtual environment for this project. In short:

        (myagent) $ python setup.py develop

Note, this may take a while, especially while installing pandas.

### Install this Agent

Now install this agent while in the virtual environment:

        (myagent) $ python setup.py develop

## Configuration

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

## Automatic and Periodic Trading

A crontab will allow you to execute the agent periodically throughout the day.
The markets are only open from 9:30AM EST to 4:00PM EST, and TDF collects data
once a minute during those times. As such, you will want your agent to execute
only during these times. To create an agent that executes every minute while
the market is open (supposing MST), open the crontab file with:

        $ crontab -e

And add the following lines (making sure to change your paths):

        # 10:00am to 4:00pm EST M-F
        * 8-14 * * Mon,Tue,Wed,Thu,Fri /path/to/your/virtualenv/bin/python /path/to/your/agent/main.py
        # 9:30am to 9:59am EST M-F
        30-59 7 * * Mon,Tue,Wed,Thu,Fri /path/to/your/virtualenv/bin/python /path/to/your/agent/main.py
