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

        # agent, league, position = self.agent_info()
        prices = self.prices('MSFT', type='n', n=20)
        returns = self.returns(prices)
        print(prices)
        print(returns)
