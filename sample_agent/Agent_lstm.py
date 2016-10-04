from base_agent import BaseAgent
import numpy as np
import pandas as pd
import sys
import os
from scipy.optimize import linprog
import cPickle as pickle
import time

class LstmAgent(BaseAgent):
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
   
    def pull_data(self):
        cwd = os.getcwd()
        tickers = self.ticker_list()
        for t in tickers:
            print t
            try:
                #prices = self.prices(ticker=t.strip(),type='this-month')
                prices = self.prices(ticker=t.strip(),n=10000)
                prices.to_pickle(cwd+'/sample_agent/data/'+str(t)+'.pkl')
            except:
                print(sys.exc_info()[0])
                print('error for stock: '+t)

    def create_initial_lstm_models(self):
        '''
        pull down all data and save
        what data will we pull? historic? bid? ask? or all        
        '''

    def execute(self):
        """The main agent logic. Computes and executes a single trade.
        """
        self.pull_data()
        sys.exit()
        composition = {}
        for i in range(0,len(portfolio)):
            if portfolio[i] > 0:
                composition[tickers[i]] = portfolio[i]

        '''
        av_returns = self.returns(historic).mean()
                
        security = argmax_d(av_returns.to_dict())
        print('Trading in {} (last 10 minutes average returns): {}'.format(
            security, av_returns[security]
        ))
        composition = {security: 0.95}
        '''
        print(composition)
        trading = True
        num_trade = 0
        while(trading):
            try:
                self.composition_trade(composition)
                time.sleep(30)
                trading = False
            except:
                # too expensive, lowed the number of shares
                portfolio*.5
                for i in range(0,len(portfolio)):
                    if portfolio[i] > 0:
                        composition[tickers[i]] = portfolio[i]
                #self.composition_trade(composition)
                print(portfolio)
                print(num_trade)
                num_trade = num_trade + 1
            if num_trade > 15:
                trading = False



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

