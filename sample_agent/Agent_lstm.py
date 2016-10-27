from base_agent import BaseAgent
from sample_agent import SampleAgent
from lstm import *
import numpy as np
import pandas as pd
import sys
import os
import os.path
from scipy.optimize import linprog
import cPickle as pickle
import time
import h5py
from keras.models import load_model

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
        self.url = url
        self.config = config
        BaseAgent.__init__(self, config, url)
	
   
    def pull_data(self):
        '''
        After many different attempts (hence the commented out lines)
        this function trains 500 LSTM models on the the stock data from
        Sept 19-Oct 9
        Saves the concatenated dataset as a 121 MB stock_concat.pkl file
        '''
        cwd = os.getcwd()
        #prices = self.prices('MSFT', type='n', n=10000) 
        #print(prices.shape)
        tickers = self.ticker_list()
        df = None
        '''
        with h5py.File('sample_agent/data.h5', 'w') as hf:
            for t in tickers:
                print t
                try:
                    #prices = self.prices(ticker=t.strip(),type='this-month')
                    prices = self.prices(ticker=t,type='n',n=40000)
                    
                    #hf.create_dataset(t, data=prices)
                    prices.to_hdf(cwd+'/sample_agent/data2/'+str(t)+'.h5')
                    #prices.to_pickle(cwd+'/sample_agent/data/'+str(t)+'.pkl')
                except:
                    print(sys.exc_info()[0])
                    print('error for stock: '+t)
        '''
        df_list = {}
        df_list = []
        count = 0
        data = pickle.load(open('stock_data_dic','rb'))
        for t in tickers:
            print t
            try:
                #prices = self.prices(ticker=t.strip(),type='this-month')
                #prices = self.prices(ticker=t,type='n',n=40000) 
                prices = []
                if t in data:
                    prices = data[t]
                else:
                    continue

                bid_name = 'bid_'+str(t)
                ask_name = 'ask_'+str(t)
                #prices.rename(index=str, columns={'bid': bid_name, "ask": ask_name})
                prices.columns = [bid_name,ask_name]
                #del prices['last']
                #prices.drop_duplicates(inplace=True)
                prices = prices[~prices.index.duplicated(keep='first')]
                print(prices.shape)
                df_list.append(prices)
                #df_list[t] = prices
                count = count + 1
                #if count > 5:
                #    break
                #hf.create_dataset(t, data=prices)
                #prices.to_hdf(cwd+'/sample_agent/data2/'+str(t)+'.h5')
                #prices.to_pickle(cwd+'/sample_agent/data/'+str(t)+'.pkl')
            except:
                print(sys.exc_info()[0])
                print('error for stock: '+t)
        #if count > 5:
        #pickle.dump(df_list, open('stock_data_dic','wb'))
        #sys.exit()
        result = pd.concat(df_list, axis=1, join='inner')
        pickle.dump(result, open('stock_concat.pkl','wb'))
        sys.exit()
        #if still memory error, try jion=df1.index
        import gc
        df = df_list[0]
        for i,df2 in enumerate(df_list[1:]):
            df = df.join(df2, rsuffix='_'+tickers[i+1])
            gc.collect()
            #df = pd.merge(df, df2, left_index=True, 
        #df = df.join(df_list[1:])
        df.to_pickle(cwd+'/sample_agent/stock_data_join.pkl')
        sys.exit()
    def create_dataset_for_stock(self, data, stock):
        X = []
        y = []
        min_look_back = 15
        for i in range(data.shape[0] - 60 - 1):
            X.append(data[i:i+min_look_back-1].values)
            y.append(data['bid'+'_'+stock][i+60]) 
            
        return np.asarray(X), np.asarray(y)

    def create_initial_lstm_models(self):
        '''
        pull down all data and save
        what data will we pull? historic? bid? ask? or all        
        '''
        data = pickle.load(open('stock_concat.pkl','rb'))        
        tickers = self.ticker_list()
        for t in tickers:
            if 'bid_'+str(t) in data:
                l = LSTM_RNN(t)
                trainX, trainY = self.create_dataset_for_stock(data, t)
                l.train(trainX,trainY) 
                l.save('sample_agent/lstm_models/'+str(t)+'.h5') 
                #break
                   
        

    def pull_last_2_hours_data(self):
        '''
        pull down last 120 points of data
        store as stock_concat_tmp.pkl
        use to update lstm model weights
        '''
        tickers = self.ticker_list()
        df_list = []
        count = 0
        lstm_stocks = pd.read_pickle('lstm_names_full').values
        for t in tickers:
            if t not in lstm_stocks:
                continue
            print t
            try:
                print('got')
                prices = self.prices(ticker=t,type='n',n=120) 
                print(prices.shape)
                del prices['last']
                bid_name = 'bid_'+str(t)
                ask_name = 'ask_'+str(t)
                prices.columns = [bid_name,ask_name]
                prices = prices[~prices.index.duplicated(keep='first')]
                df_list.append(prices)
                count = count + 1
                #if count > 5:
                #    break
            except:
                print(sys.exc_info()[0])
                print('error for stock: '+t)
        #data = pd.concat(df_list, axis=1, join='inner')
        data = pd.concat(df_list, axis=1, join='outer')
        X = np.asarray([data.values])
        #X = np.asarray([data.values[-14:]])
        #pickle.dump(X, open('x_curr.p','wb'))
        #X = pickle.load(open('x_curr.p','rb'))
        means = np.nanmean(X, axis=1)
        mask = np.isnan(X)
        masked_arr = np.ma.masked_array(X, mask)
        X = masked_arr.filled(means)
        X = np.nan_to_num(X) 
        return X
        #return pd.concat(df_list, axis=1, join='inner')
        #return result = pd.concat(df_list, axis=1, join='inner')
        #pickle.dump(result, open('stock_concat_tmp.pkl','wb'))
 
    def update_lstm_models(self):
        '''
        use last 2 hours worth of data
        to update all existing lstm models
        '''
        data = pickle.load(open('stock_concat.pkl','rb'))
        data = data[-120:]
        print data.shape
        #data = self.pull_last_2_hours_data()
        #tickers = self.ticker_list()
        tickers = pd.read_pickle('lstm_names_full').values
        history = {}
        count = 0
        print data.columns
        for t in tickers.flatten():
            print t
            print 'bid_'+str(t) in data
            print os.path.isfile('sample_agent/lstm_models/'+str(t)+'.h5')
            if 'bid_'+str(t) in data and os.path.isfile('sample_agent/lstm_models/'+str(t)+'.h5'):            
                print 'did we even hit here???'
                l = LSTM_RNN(t, saved_file='sample_agent/lstm_models/'+str(t)+'.h5')      
                trainX, trainY = self.create_dataset_for_stock(data, t)
                hist = l.train(trainX,trainY)
                print(hist)
                history[t] = hist
                #save updated model
                l.save('sample_agent/lstm_models/'+str(t)+'.h5') 
                count = count + 1
                if count > 10:
                    break
        pickle.dump(history, open('val_history.p','wb'))

    def predict(self):
        '''to test: make sure the stocks pulled match the training stocks'''
        tickers = self.ticker_list()
        df_list = []
        count = 0
        lstm_stocks = pd.read_pickle('lstm_names_full').values
        '''
        print(lstm_stocks)
        for t in tickers:
            if t not in lstm_stocks:
                continue
            print t
            try:
                print('got')
                prices = self.prices(ticker=t,type='n',n=120) 
                print(prices.shape)
                del prices['last']
                bid_name = 'bid_'+str(t)
                ask_name = 'ask_'+str(t)
                prices.columns = [bid_name,ask_name]
                prices = prices[~prices.index.duplicated(keep='first')]
                df_list.append(prices)
                count = count + 1
                #if count > 5:
                #    break
            except:
                print(sys.exc_info()[0])
                print('error for stock: '+t)
        #data = pd.concat(df_list, axis=1, join='inner')
        data = pd.concat(df_list, axis=1, join='outer')
        X = np.asarray([data.values[-14:]])
        #pickle.dump(X, open('x_curr.p','wb'))
        #X = pickle.load(open('x_curr.p','rb'))
        means = np.nanmean(X, axis=1)
        mask = np.isnan(X)
        masked_arr = np.ma.masked_array(X, mask)
        X = masked_arr.filled(means)
        X = np.nan_to_num(X)
        print(np.isnan(X).any())
        print(X)
        #print(data.shape)
        #print(data2.shape)
        #sys.exit()
        predictions = {}
        pred_arr = []
        ####DELETE THIS - JUST FOR TEST
        #data = pickle.load(open('stock_concat.pkl','rb'))
        #X = np.asarray([data.values[0:14]])

        count = 0
        for t in tickers:
            if 'bid_'+str(t) in data and os.path.isfile('sample_agent/lstm_models/'+str(t)+'.h5'):            
                #if  os.path.isfile('sample_agent/lstm_models/'+str(t)+'.h5'):            
                l = LSTM_RNN(t, saved_file='sample_agent/lstm_models/'+str(t)+'.h5')      
                pred = l.predict(X)
                print pred
                predictions[t] = pred
                pred_arr.append(pred)
                count = count + 1
                #if count > 5:
                #    break
                #save updated model
        #return np.asarray(pred_arr)
        pred_arr = np.asarray(pred_arr)
        pickle.dump(pred_arr, open('pred_arr','wb'))
        '''
        pred_arr = pickle.load(open('pred_arr','rb'))
        print pred_arr
        agent = SampleAgent(self.config, self.url)    
        #historic = self.historic(type='n', n=100, side='ask')
        #pickle.dump(historic,open('hist.p','wb'))
        historic = pickle.load(open('hist.p','rb'))
        print historic.columns
        print ('lstm now')
        print lstm_stocks
        print historic.columns.shape
        print lstm_stocks.shape
        print np.setdiff1d(historic.columns, lstm_stocks)
        print np.setdiff1d(historic.columns, lstm_stocks).shape 
        to_del = []
        for s in historic.columns:
            if not os.path.isfile('sample_agent/lstm_models/'+str(s)+'.h5'):
                to_del.append(s)
        for s in to_del:
            print s
            del historic[s]
            print(historic.shape)
        #delete anything in pred_arr t
        #list files in same order you predicted them
        to_del = []
        reordered_cols = []
        count = 0
        for t in tickers:
            if os.path.isfile('sample_agent/lstm_models/'+str(t)+'.h5'):
                if t not in historic.columns:
                    to_del.append(count)
                else:
                    reordered_cols.append(t)
            count = count + 1

        #historic = self.historic(type='n', n=100, side='ask')
        #historic = pickle.load(open('hist.p','rb'))
        #sys.exit()

        '''
        to_del = []
        for idx, s in enumerate(lstm_stocks):
            print np.asarray(historic.columns)
            if s not in np.asarray(historic.columns):
                to_del.append(idx)
        print to_del
        '''
        print 'BEFORE'
        print pred_arr
        if len(to_del) > 0:
            to_del.reverse()
            for s in to_del:
                pred_arr = np.delete(pred_arr, s)
        #reorder historic dataframe
        historic = historic[reordered_cols]
        print 'ready to go'
        print historic.shape
        print pred_arr.shape
        print 'what is it like here???'
        print pred_arr
        return agent.calc_simplex(historic,pred_arr)
        #agent = SampleAgent(config, url)    
    
        
        #future_bid_prices

         
    def execute(self):
        """The main agent logic. Computes and executes a single trade.
        """
        #self.pull_data()
        #self.create_initial_lstm_models()
        portfolio = self.predict()
        print(portfolio)
        composition = {}
        tickers = pd.read_pickle('lstm_names_full').values.flatten()
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

