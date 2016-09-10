from base_agent import BaseAgent


class SampleAgent(BaseAgent):
    """A sample agent.

    Looks at the most recent returns across the S&P 500 and invests 95% of the
    portfolio in the single security with the highest returns.
    """

    def __init__(self, config):
        BaseAgent.__init__(self, config)
