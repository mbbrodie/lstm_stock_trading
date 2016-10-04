from base_agent import BaseAgent
import sys
import sys
from scipy.optimize import linprog


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

    def calc_simplex(self, df):
	num_timesteps = df.shape[0]
	num_stocks = df.shape[1]
	stock_means = df.mean()
	improving = True
	loops_without_improve = 0
	mu = 0
	best_ret = 0
	best_portfolio = []
	while improving: #find mu/composition from 1 to n that maximizes return-risk
	#print 'mu: '+str(mu)
	    mu = mu + 1
	    c = np.zeros((num_stocks+num_timesteps))
	    c[0:num_stocks] = stock_means
	    c[num_stocks:] = -1.0*mu /num_timesteps
	    c = c * -1
	    A = np.zeros((2+num_timesteps, num_stocks+num_timesteps))
	    A[0,0:num_stocks] = 1
	    A[1,0:num_stocks] = -1
	    A[2:,0:num_stocks] = df - stock_means
	    A[2:,num_stocks:] = -1 * np.eye(num_timesteps)
	    b = np.zeros((2+num_timesteps))
	    b[0] = 1
	    b[1] = -1

	    res = linprog(c, A_ub=A, b_ub=b, options={"disp": True}, method='simplex')
	    portfolio = res.x[0:num_stocks]
	    #print '\t'.join(map(str,[round(i, 3) for i in res.x[0:num_stocks]]))
	    ret = np.dot(portfolio, stock_means)
	    risk = np.average(np.dot((np.absolute(df-stock_means)),portfolio))
	    print 'diff'
	    print str(ret-risk)
	    diff = ret - risk
	    if diff > best_ret:
		loops_without_improve = 0
		best_ret = diff
		best_portfolio = portfolio 
	    else:
		loops_without_improve = loops_without_improve + 1
	    
	    if loops_without_improve > 2:
		improving = False

	return best_portfolio
	 
    def execute(self):
	"""The main agent logic. Computes and executes a single trade.
	"""

	# agent, league, position = self.agent_info()
	# prices = self.prices('MSFT', type='n', n=5)
	# print(prices)
	# returns = self.returns(prices)
	# print(returns)
	tickers = self.ticker_list()
	# print(tickers)
	# historic = self.historic(type='n', n=5)
	# print(historic)
	# self.basic_trade({'GOOG': 22, 'MSFT': 15})
	# self.state_trade({'GOOG': 21, 'MSFT': 10})
	# self.composition_trade({'GOOG': .78, 'MSFT': .1})
	#for t in self.ticker_list():
	#    prices = self.prices(ticker=t, type='this-month')
	#    print(prices)
	#    sys.exit()
	historic = self.historic(type='n', n=100, side='ask')
	    portfolio = self.calc_simplex(historic)
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
