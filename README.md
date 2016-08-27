## Description ##

In this agent, trades are made naively, by choosing the security with the 
highest returns in the last time period and investing 95% of the portfolio value 
in that security (the remaining 5% in cash). 

This agent is designed to be a starting point for new python agents that trade
on the TDF. Either fork the repo or copy the code to make a new TDF agent.

## Installation - Ubuntu

NOTE: these instructions are written for Ubuntu 16.04. However, this code should
work on OS-X by following analogous installation procedures.

### Installing Python 3 ###

We also recommend that these agents run under a Python 3 environment (they 
should work with Python 2.7 as well; however, this is not tested). To install
Python 3, its development toolkits, and other dependencies:

        $ sudo apt-get install python3 python3-dev libffi-dev
        
### Creating a Virtual Environment ###

We recommend that python TDF agents be installed within their own virtual 
environments. The utility `mkvirtualenv` is a great tool to create such 
virtual environments. 

Follow the instructions at 
<virtualenvwrapper.readthedocs.io/en/latest/install.html> to install the 
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
        
### Install `pytdf-base-agent`

Install the `pytdf-base-agent` at <https://gitlab.com/idealabs/pytdf-base-agent>
while within the virtual environment for this project. In short:

        (myagent) $ python setup.py develop