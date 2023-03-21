import yfinance as yf
import pandas as pd
from datetime import timedelta, date
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
        return False

# per option - 100 shares
def sell_call(strike_price, underlying_price):
    # call is exercised
    if underlying_price > strike_price:
        return (underlying_price - strike_price) * 100 
    else:
        return False

# initialize the variables
cash = 300000

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
    if len(shares) == 0 and len(putContracts) == 0 and len(callContracts) == 0: # need to edit this
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
            print(f"Cash: {cash}")

        else:
            print("No suitable put contract found on " + single_date.strftime("%Y-%m-%d"))
        pass

    # check if there are contracts expiring today
    if len(putContracts) > 0:
        if putContracts[3].strftime("%Y-%m-%d") == single_date.strftime("%Y-%m-%d"):
            # get price of underlying asset today 
            underlying_price = getUnderlyingData(single_date, df=underlyingData)

            # check if put contract is exercised
            returns = sell_put(putContracts[4], underlying_price)

            if returns != False:
                # put contract is exercised
                # update numShares
                # shares = [data_bought, amt, price_bought]
                shares = [single_date, 1000, putContracts[4]]
                print("Shares bought on " + single_date.strftime("%Y-%m-%d") + " for " + str(putContracts[4] * 1000))
                cash -= putContracts[4] * 1000
                print(f"Cash: {cash}")

            else:
                print("Put contract not exercised")

            putContracts = []

    # start of bearish neutral strategy
    if len(shares) > 0 and len(putContracts) == 0 and len(callContracts) == 0:
        # get required info for call contracts
        result = getCallData(single_date)

        # if there is a suitable contract
        if result:
            premium, dte, expdate, strike, underlying_price, delta = result

            # sell 10 call contracts (100 shares each) and save details needed during expiry in list
            callContracts = [single_date, premium, dte, expdate, strike, underlying_price, delta] 

            # premium
            cash += premium * 1000
            print("Call contract sold on " + single_date.strftime("%Y-%m-%d") + " for " + str(premium *1000))
            print(f"Cash: {cash}")

        else:
            print("No suitable call contract found on " + single_date.strftime("%Y-%m-%d"))
        pass

    # check if there are call contracts expiring today
    if len(callContracts) > 0:
        if callContracts[3].strftime("%Y-%m-%d") == single_date.strftime("%Y-%m-%d"):
            # get price of underlying asset today
            underlying_price = getUnderlyingData(single_date, df=underlyingData)

            # check if put contract is exercised
            returns = sell_call(callContracts[4], underlying_price)

            if returns != False:
                # call contract is exercised
                # original_price = shares[2]
                # difference = original_price - callContracts[4]

                # update cash - could be either profit or loss
                cash += callContracts[4] * 1000

                # update numShares
                shares = []
                print("Shares sold on " + single_date.strftime("%Y-%m-%d") + " for " + str(callContracts[4] * 1000))
                print(f"Cash: {cash}")
            else:
                print("Call contract not exercised")

            callContracts = []
# end of strategy

print(shares)
print(cash)
