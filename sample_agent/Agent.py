from base_agent import BaseAgent


class SampleAgent(BaseAgent):
    """A sample agent.

    Looks at the most recent returns across the S&P 500 and invests 95% of the
    portfolio in the single security with the highest returns.

    Parameters
    ----------
    config : ConfigParser
        The configuration object for connection to an agent at TDF.
    url : str
        The TDF url.
    """

    def __init__(self, config, url):
        BaseAgent.__init__(self, config, url)
