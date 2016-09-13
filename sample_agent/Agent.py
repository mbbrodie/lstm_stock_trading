from base_agent import BaseAgent


class SampleAgent(BaseAgent):
    """A sample agent.

    Looks at the most recent returns across the S&P 500 and invests 95% of the
    portfolio in the single security with the highest average returns over
    the last 10 minutes of collected data.

    Parameters
    ----------
    config : ConfigParser
        The configuration object for connection to an agent at TDF.
    url : str
        The TDF url.
    """

    def __init__(self, config, url):
        BaseAgent.__init__(self, config, url)

    def execute(self):
        """The main agent logic. Computes and executes a single trade.
        """

        # agent, league, position = self.agent_info()
        # prices = self.prices('MSFT', type='n', n=5)
        # print(prices)
        # returns = self.returns(prices)
        # print(returns)
        # tickers = self.ticker_list()
        # print(tickers)
        # historic = self.historic(type='n', n=5)
        # print(historic)

        # self.basic_trade({'GOOG': 22, 'MSFT': 15})
        # self.state_trade({'GOOG': 21, 'MSFT': 10})
        # self.composition_trade({'GOOG': .78, 'MSFT': .1})

        historic = self.historic(type='n', n=10, side='ask')
        av_returns = self.returns(historic).mean()
        security = argmax_d(av_returns.to_dict())
        print('Trading in {} (last 10 minutes average returns): {}'.format(
            security, av_returns[security]
        ))
        composition = {security: 0.95}
        self.composition_trade(composition)


def argmax_d(d):
    """Computes the argmax of the given dictionary

    Parameters
    ----------
    d : dictionary {[obj] -> number}

    Returns
    -------
    argmax : [obj]
    """
    return max(d.keys(), key=(lambda key: d[key]))
