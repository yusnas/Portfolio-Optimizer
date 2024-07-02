import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd

def simulate(start_date, 
	     end_date, 
             ls_stock, 
             allocation):
	"""Return std, average daily return,sharpe ration and 
           cummulative return of the portfolio.
  
           Example Input:
           ([2010,1,1],[2010,12,31],['AXP','HPQ','IBM', 'HNZ'],/
           [0, 0, 0, 1])"""
	
	#Define start_date, end_date as 3 array of integer
	ls_symbols = ls_stock
	allo_matrix = np.transpose(np.matrix(allocation))
	dt_start = dt.datetime(start_date[0], start_date[1], start_date[2])
	dt_end = dt.datetime(end_date[0], end_date[1], end_date[2])
	# Data read at 16:00pm each day
	dt_timeofday = dt.timedelta(hours = 16)
	# Count the NYSE days
	ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)	
	
	# Read data
	c_dataobj = da.DataAccess('Yahoo') # Use Yahoo data
	ls_keys = ['open', 
                   'high', 
                   'low', 
                   'close', 
                   'volume', 
                   'actual_close',
		  ]
	
	# Get data object, 6 blocks
	# Define dict so that each element ls_keys corresponds to one block	
	ldf_data = c_dataobj.get_data(ldt_timestamps,ls_symbols, ls_keys)	
	d_data = dict(zip(ls_keys, ldf_data))

	# Normalize the data
	# Close price is the adjusted price here
	# .value only retain the values	
	# Normalize the price for each stock
	na_price = d_data['close'].values 
	normalized_price = na_price / na_price[0,:]  
	# Calulate the asset of the portfolio, x_A*P_A(t) + x_B*P_B(t)
	# np.matrix(string), so allocation must be string
	asset_price = np.dot(normalized_price,allo_matrix)
	
	# Calculate the daily_return of the portfolio
	# In python, it's passed by reference so we need copy it
	na_rets = asset_price.copy()	
	tsu.returnize0(na_rets)	

	# Calculate the mean and std of portfolio daily_return	
	av_day_ret = na_rets.mean()
	vol = np.std(na_rets)
	cum_ret = np.dot(normalized_price[normalized_price.shape[0]-1,:],\
		   	allo_matrix)
	sharpe = np.sqrt(252)*av_day_ret / vol
#	print "dailyreturn",av_day_ret,\
#	      "\nvolatility", vol, \
#	      "\ncumulative return:", cum_ret[0,0],\
 #             "\nsharpe ratio", sharpe
	return (av_day_ret, vol,sharpe, cum_ret[0,0])


# test  
#print simulate([2010,1,1],[2010,12,31],['AXP','HPQ','IBM', 'HNZ'],[0, 0, 0, 1])
# agree!


def optim_allocation(start_date,
		     end_date,
		     ls_stock):
	num_stock = len(ls_stock)
	# Generate num_stock - 1 random number between 0 and 1
	allo = [0,0,0,1]
	sharpe = 0
	while allo[0] <= 1:
		while allo[1] <= 1 - allo[0]:
			while allo[2] <= 1 - allo[0] - allo[1]:
				allo[3] = 1 - allo[0] - allo[1] - allo[2]
				day_ret, vol, sharp_out, cum_ret = simulate(start_date, end_date, ls_stock, allo) 
				if sharp_out > sharpe:
					sharpe = sharp_out
					allo_optima = list(allo) #[allo[0],allo[1],allo[2],allo[3]]
					day_opt = day_ret
					vol_opt = vol
					cum_opt = cum_ret
				allo[2] += 0.1
			allo[2] = 0
			allo[1] += 0.1
		allo[1] = 0
		allo[0] += 0.1
	return (sharpe, allo_optima, day_opt, vol_opt, cum_opt)		
		
#test optim_allocation
sharpe, allo, day, vol, cum = optim_allocation([2010,1,1],[2010,12,31],['AAPL','GOOG','IBM', 'MSFT'])
print "The Optimal allocation is", allo,"with", "\nsharpe ration", sharpe,\
      "\naverage day return", day, "\nvolatility",vol,"\ncumulative return", cum
