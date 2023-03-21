import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta, date
from getData import getCallData, getPutData

# Define the start and end dates for the backtest
startDate = date(2018, 1, 2)
endDate = date(2023, 1, 1)

ticker = "SPY"

underlyingData = yf.download(ticker, start=startDate, end=endDate)

def getUnderlyingData(dateGiven, df=underlyingData):
    dateGiven = dateGiven.strftime("%Y-%m-%d")
    try:
        return underlyingData.loc[dateGiven]['Close']

    except:
        return None

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

# track contracts and shares
# put contracts = [data_bought, premium, dte, expiration_date, premium, strike price, underlying price, delta]
# call contracts = [data_bought, premium, dte, expiration_date, premium, strike price, underlying price, delta]
# shares = [data_bought, amt, price_bought]
putContracts = []
callContracts = []
shares = []

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

# loop through each trading day from start to end date
for single_date in pd.date_range(startDate, endDate):
    year = single_date.strftime("%Y")
    month = single_date.strftime("%m")

    # start of bullish neutral strategy
    if len(shares) == 0 and len(putContracts) == 0 and len(callContracts == 0) : # need to edit this
        # get required info for put contracts
        result = getPutData(single_date)

        # if there is a suitable contract
        if result:
            premium, dte, expdate, strike, underlying_price, delta = result

            # sell 10 put contracts (100 shares each) and save details needed during expiry in list
            putContracts = [single_date, premium, dte, expdate, strike, underlying_price, delta] 

            # premium
            cash += premium * 1000
            print("Put contract sold on " + single_date.strftime("%Y-%m-%d") + " for " + str(premium *1000))

        else:
            print("No suitable put contract found on " + single_date.strftime("%Y-%m-%d"))
        

    # check if there are contracts expiring today
    if putContracts[0] == single_date:
        # get price of underlying asset today 
        # !!!!!
        underlying_price = getUnderlyingData(single_date, df=underlyingData)
    
        # check if put contract is exercised
        returns = sell_put(value[4], underlying_price)

        putContracts = []

        if returns < 0:
            # put contract is exercised
            # update numShares
            # shares = [data_bought, amt, price_bought]
            shares = [single_date, 1000, value[4]]


    # start of bearish neutral strategy
    if len(shares) > 0 and len(callContracts == 0):
        # get required info for call contracts
        result = getCallData(single_date)

        # if there is a suitable contract
        if result:
            premium, dte, expdate, strike, underlying_price, delta = result

            # sell 10 call contracts and save details needed during expiry in dictionary strike_price, expiration_date
            callContracts[single_date] = [strike, single_date + timedelta(days=dte)] 

            # premium * 10
            cash += 12.50 * 10

    # check if there are call contracts expiring today
    for key, value in callContracts:
        if value[2] == date:
            # get price of underlying asset today
            underlying_price = 100
        
            # check if put contract is exercised
            returns = sell_call(value[0], underlying_price)

            del callContracts[key]

            if returns < 0:
                # call contract is exercised
                original_price = shares.values()[0]
                difference = original_price - underlying_price

                # update cash - could be either profit or loss
                cash += difference * 1000

                # update numShares
                del shares[original_price]

# end of strategy

if len(shares) > 0:
    # sell all shares
    # get current share price
    current_price = 100

    for key, value in shares:
        cash += current_price * value

print(cash)
