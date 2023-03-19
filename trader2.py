import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


# Define the underlying asset and option symbol
stock_symbol = 'SPY'
option_symbol = 'SPY220617C00450000'  # Replace with a valid option symbol for SPY

# Define the start and end dates for the backtest
start_date = '1/1/2015'
end_date = '12/31/2019'


# per option - 100 shares
def sell_put(strike_price, underlying_price):
    # put is exercised
    if underlying_price < strike_price:
        return (strike_price - underlying_price) * 100
    else:
        return None

# per option - 100 shares
def sell_call(strike_price, underlying_price):
    # call is exercised
    if underlying_price > strike_price:
        return (underlying_price - strike_price) * 100 
    else:
        return None

# initialize the variables
cash = 10000

# dictionary to track status of contracts and shares and their prices
# format
# put contracts = {"data_bought": [strike_price, premium, expiration_date]}
# call contracts = {"data_bought": [strike_price, premium, expiration_date, underlying_price]}
# shares = {price: amt}
putContracts = {}
callContracts = {}
shares = {}

# loop through each trading day from start to end date
for date in pd.date_range(start_date, end_date):
    # start of bullish neutral strategy
    if len(shares) == 0 and len(putContracts) == 0 and len(callContracts == 0) : # need to edit this
        # get required info for put contracts
        # sieve out info for put contracts and choose

        # sell 10 put contracts and save details needed during expiry in dictionary strike_price, expiration_date
        putContracts[date] = [100, date + timedelta(days=45)] 

        # premium * 10
        cash += 12.50 * 10

    # check if there are contracts expiring today
    for key, value in putContracts:
        if value[2] == date:
            # get price of underlying asset tod
            underlying_price = 100
        
            # check if put contract is exercised
            returns = sell_put(value[0], underlying_price)

            del putContracts[key]

            if returns < 0:
                # put contract is exercised

                # update numShares
                if underlying_price in shares:
                    shares[underlying_price] += 1000
                else:
                    shares[underlying_price] = 1000

                # update cash
                cash -= underlying_price * 1000
                pass

    # start of bearish neutral strategy
    if len(shares) > 0 and len(callContracts == 0):
        # get required info for call contracts
        # sieve out info for call contracts and choose

        # sell 10 call contracts and save details needed during expiry in dictionary strike_price, expiration_date
        callContracts[date] = [100, date + timedelta(days=45)] 

        # premium * 10
        cash += 12.50 * 10

    # check if there are call contracts expiring today
    for key, value in callContracts:
        if value[2] == date:
            # get price of underlying asset today
            underlying_price = 100
        
            # check if put contract is exercised
            returns = sell_call(value[0], underlying_price)

            del putContracts[key]

            if returns < 0:
                # call contract is exercised
                difference = value[3] - underlying_price

                # update cash - could be either profit or loss
                cash += difference * 1000

                # update numShares
                del shares[value[3]]

# end of strat

if len(shares) > 0:
    # sell all shares
    # get current share price
    current_price = 100

    for key, value in shares:
        cash += current_price * value

print(cash)
                
                

            

