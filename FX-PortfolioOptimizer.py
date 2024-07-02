"""Using the Time Function"""
import time
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
    
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
    
    
#lf_port_alloc = [0.1,0.1,0.6,0.2]    




def simulate(allocation):
#def simulate():
    print ("In The Name of ALLAH, the Beneficent, The Merciful")
    
    
    
    dt_start = dt.datetime(2009, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)    
    #ls_symbols = ["AAPL","GOOG", "XOM", "GLD"]
    ls_symbols = ["AAPL", "GLD", "GOOG", "XOM"]
    #ls_symbols = ["AXP", "HPQ", "IBM", "HNZ"]
    #Alloc  = [0.7,0.0,0.0, 0.3]
    
    #assignment
    #ls_symbols = ["AAPL","GOOG", "IBM", "MSFT"]
    #ls_symbols = ['BRCM', 'ADBE', 'AMD', 'ADI']
    #ls_symbols = ['BRCM', 'TXN', 'AMD', 'ADI'] 
    #ls_symbols = ['BRCM', 'TXN', 'IBM', 'HNZ'] 
    #ls_symbols  = ['C', 'GS', 'IBM', 'HNZ']
    #ls_symbols  = ['AAPL', 'GOOG', 'GLD', 'XOM']
    #ls_symbols_spx  = ['SPX']
    
    #dt_start = dt.datetime(startdate)
    #dt_end = dt.datetime(enddate)    
    #ls_symbols = symbol
    Alloc  = allocation   
    
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    
    c_dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    
   # cd_data = compute_daily_return(d_data['close'])
   
    c_dataobj = da.DataAccess('Yahoo',cachestalltime=0) # clear the cache
    
    
    df_rets = d_data['close'].copy()
   # dmean  = d_data['close'].mean()
   # dstd   = d_data['close'].std()
    
   
    
   # print ldf_data
    
   # print d_data['close']
    
    
    na_price = d_data['close'].values
    
    print (df_rets.head())
    print (df_rets.values)
    df_rets = d_data['close'].copy()
    na_normalized_price = na_price / na_price[0, :]
    
    na_normalized_price1 = na_normalized_price.copy()
    na_normalized_price2 = na_normalized_price * 100
     
    na_normalized_fred = na_normalized_price 
    na_normalized_fred = na_normalized_price[:,0] * Alloc[0]  * 1000000
    na_normalized_fred1 = na_normalized_price[:,1] * Alloc[1] * 1000000
    na_normalized_fred2 = na_normalized_price[:,2] * Alloc[2] * 1000000
    na_normalized_fred3 = na_normalized_price[:,3] * Alloc[3] * 1000000
    
    na_normalized_price[:,0] = na_normalized_fred
    na_normalized_price[:,1] = na_normalized_fred1
    na_normalized_price[:,2] = na_normalized_fred2
    na_normalized_price[:,3] = na_normalized_fred3
    
    print ("Note", na_normalized_price)
    
    na_price_cumul1 = np.sum(na_normalized_price, axis=1)# fund cumulat returns
    print ("Note999999999", na_price_cumul1)
    na_price_cumulcopy = na_price_cumul1.copy() / 100
    
   # na_rets   = df_rets.values
   # tsu.returnize0(na_rets)
    
    
    
    
    na_cumul_perct = na_price_cumul1 / 10000
    
    #na_daily_rets  = np.cumprod(na_price_cumul1 +1) # daily total returns
    na_daily_rets = tsu.returnize0(na_price_cumulcopy)# daily total returns
    
    avg_daily_returns = na_daily_rets.mean()
    std_returns = na_daily_rets.std()
    sharpe = np.sqrt(252) * (avg_daily_returns / std_returns)
    
    na_cumul_rets = na_cumul_perct[-1] /100 
    
    """print na_price
    print na_normalized_price1
    print na_normalized_price2
    print na_normalized_price
    print "This is FUND INVEST"
    print na_price_cumul1
    print "This is Cummulative Fund in percentage point"
    print na_cumul_perct
    print "This is Daily Return values"
    print na_daily_rets
    print "Annual Return Percentage"
    print na_cumul_perct[-1] - 100
    print "Cumulative Return"
    print na_cumul_rets   
    print "The Average Daily Returns"
    print avg_daily_returns
    print "Standard Deviation of Daily Rets "
    print std_returns
    print "Sharpe Ratio " 
    print sharpe"""
    
    """print "Start Date :", dt_start
    print "Allah"
    print "End Date   :", dt_end
    print "Symbol     :" , ls_symbols
    print "Optimal Allocation :", Alloc
    print "Sharpe Ratio", sharpe
    print "Volatility(stdev of daily returns):",std_returns
    print "Average Daily Return:",avg_daily_returns
    print "Cumulative Return :",na_cumul_rets   
   
  
   
    plt.clf()
    plt.plot(ldt_timestamps, na_normalized_price1)
    plt.legend(ls_symbols)
    plt.ylabel('Normalized')
    plt.xlabel('Date')
    plt.savefig('adjustedclose.pdf', format='pdf')"""  


    na_rets = na_normalized_price.copy()
    tsu.returnize0(na_rets) 
    
 
    #return std_returns,avg_daily_returns,sharpe,na_cumul_rets
    return sharpe
    
def test_run():
    #vol, daily_ret,sharpe,cum_ret = simulate((2010, 1, 1),(2010, 12, 31),["AXP", "HPQ", "IBM", "HNZ"],[0.0,0.0,0.0,1.0]
    #vol, daily_ret,sharpe,cum_ret = simulate()
    #create a list of numbers from 0 to 1.0 in 0.1 increments
    l = map(lambda x:x/100., range(0,110,10))
    sharpe_list =[]
    Alloc_list = []
    number_of_valid_alloc =[]
    #iterate over all combinations and check which are valid
    for i1 in l:
        for i2 in l:
            for i3 in l:
                for i4 in l:
                    if i1+i2+i3+i4 == 1.0:
                        valid_alloc = [i1, i2, i3, i4]
                        number_of_valid_alloc.append(1) 
                        sharpe = simulate(valid_alloc)
                        sharpe_list.append(sharpe) 
                        Alloc_list.append(valid_alloc)
    # this is a valid allocation
    # check returns, sharpe, etc
    #valid_alloc1 = [0.4, 0.0, 0.2, 0.4]
    name_index = max(sharpe_list)
    name_index2 = min(sharpe_list)
    #if name_index in sharpe_list:
    print ("Min Index")
    print (sharpe_list.index(name_index2),Alloc_list[sharpe_list.index(name_index2)])
    print ("Max Index"    )
    print (sharpe_list.index(name_index),Alloc_list[sharpe_list.index(name_index)])
    print ("Max_Sharpe Ratio", )
    print ( max(sharpe_list))
    print ("Min_Sharpe Ratio",)
    print (min(sharpe_list))
    print ("Valid Alloc",)
    print (sum(number_of_valid_alloc) )   
    
    
    """print "Start Date :", startdate 
    print "End Date   :", enddate
    print "Symbol     :" , symbol
    print "Optimal Allocation :", allocation
    print "Sharpe Ratio", sharpe
    print "Volatility(stdev of daily returns):",vol
    print "Average Daily Return:",daily_ret
    print "Cumulative Return :",cum_ret"""
    
"""allocation_values = [i / 10.0 for i in range(0, 11)]

perms = [combo[i:] + combo[0:i] for i in range(len(ls_symbols)) 
for combo in itertools.combinations_with_replacement(allocation_values, len(ls_symbols)) if sum(combo) == 1.0]"""
      

if __name__=="__main__":
    test_run()
    #simulate()