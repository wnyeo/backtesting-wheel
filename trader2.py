import yfinance as yf
import pandas as pd
from datetime import timedelta, date
from getData import getCallData, getPutData, underlyingFromOptions

# Define the start and end dates for the backtest
startDate = date(2018, 1, 2)
endDate = date(2022, 12, 30)

ticker = "SPY"

underlyingData = yf.download(ticker, start=startDate, end=endDate)

def getUnderlyingData(dateGiven, df=underlyingData):
    dateGivenStr = dateGiven.strftime("%Y-%m-%d")
    try:
        return underlyingData.loc[dateGivenStr]['Close']

    except:
        return underlyingFromOptions(dateGiven)

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
cash = 500000

# track contracts, shares and details of each cycle
# put contracts = [data_bought, premium, dte, expiration_date, premium, strike price, underlying price, delta]
# call contracts = [data_bought, premium, dte, expiration_date, premium, strike price, underlying price, delta]
# shares = [data_bought, amt, price_bought]
# cycle = [total premium earned, buy_price, sell_price, starting_bal, ending_bal]
# pnl = [] # at the end of each cycle
putContracts = []
callContracts = []
shares = [None, 0, None]
cycle = [0, 0, 0, cash, 0, ]
pnl = []
dailyPnL = []
dates = []
costBasis = 0
costArr = []

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

# loop through each trading day from start to end date
for single_date in pd.date_range(startDate, endDate):

    # start of bullish neutral strategy
    if shares[1] == 0  and len(putContracts) == 0 and len(callContracts) == 0: 
        # get required info for put contracts
        result = getPutData(single_date)

        # if there is a suitable contract
        if result:
            premium, dte, expdate, strike, underlying_price, delta = result

            # sell 10 put contracts (100 shares each) and save details needed during expiry in list
            putContracts = [single_date, premium, dte, expdate, strike, underlying_price, delta] 

            # premium x number of contracts x number of shares per contract
            cash += premium * 10 * 100
            cycle[0] += premium * 10 * 100
            
            print("Put contract sold on " + single_date.strftime("%Y-%m-%d") + " for " + str(premium *100 *10))
            print(f"Details of put contract: Underlying Price: {underlying_price}, Strike Price: {strike}, DTE: {dte}, Delta: {delta}, Premium: {premium}, Expiration Date: {expdate}")
            print(f"Cash: {cash}")

        else:
            print("No suitable put contract found on " + single_date.strftime("%Y-%m-%d"))
        
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
                # change to 100x10
                shares = [single_date, 1000, putContracts[4]]
                print("Shares bought on " + single_date.strftime("%Y-%m-%d") + " for " + str(putContracts[4] * 1000))
                cash -= putContracts[4] * 1000
                costBasis = putContracts[4] * 1000
                print(f"Cash: {cash}")
                
                cycle[1] = putContracts[4]

            else:
                print("Put contract not exercised")

            putContracts = []

    # start of bearish neutral strategy
    if shares[1] > 0 and len(putContracts) == 0 and len(callContracts) == 0:
        # get required info for call contracts
        result = getCallData(single_date)

        # if there is a suitable contract
        if result:
            premium, dte, expdate, strike, underlying_price, delta = result

            # sell 10 call contracts (100 shares each) and save details needed during expiry in list
            callContracts = [single_date, premium, dte, expdate, strike, underlying_price, delta] 

            # premium x number of contracts x number of shares per contract
            cash += premium * 10 * 100
            cycle[0] += premium * 10 * 100

            print("Call contract sold on " + single_date.strftime("%Y-%m-%d") + " for " + str(premium *100 *10))
            print(f"Details of call contract: Underlying Price: {underlying_price}, Strike Price: {strike}, DTE: {dte}, Delta: {delta}, Premium: {premium}, Expiration Date: {expdate}")
            print(f"Cash: {cash}")

        else:
            print("No suitable call contract found on " + single_date.strftime("%Y-%m-%d"))
        
    # check if there are call contracts expiring today
    if len(callContracts) > 0:
        if callContracts[3].strftime("%Y-%m-%d") == single_date.strftime("%Y-%m-%d"):
            # get price of underlying asset today
            underlying_price = getUnderlyingData(single_date, df=underlyingData)

            # check if put contract is exercised
            returns = sell_call(callContracts[4], underlying_price)

            if returns != False:
                # call contract is exercised

                # update cash - could be either profit or loss
                # strike price x number of shares
                cash += callContracts[4] * 1000

                # update numShares
                shares = [None, 0, None]
                print("Shares sold on " + single_date.strftime("%Y-%m-%d") + " for " + str(callContracts[4] * 1000))
                print(f"Cash: {cash} \n")

                cycle[4] = cash
                cycle[2] = callContracts[4]

                # add cycle to pnl
                # cycle = [total premium earned, buy_price, sell_price, profit_From_Underlying, starting_bal, ending_bal]
                # print(cycle)
                profitFromUnderlying = (cycle[2] - cycle[1]) * 1000
                print("Profit from underlying: " + str(profitFromUnderlying))

                print("Profits from selling options: " + str(cycle[0]))

                profits = cycle[0] + profitFromUnderlying
                print("Profits from this cycle: " + str(profits) + "\n")

                pnl.append(profits)
    
                cycle = [0, 0, 0, cash, 0]
                costBasis = 0
            else:
                print("Call contract not exercised")

            callContracts = []
    

    # get price of underlying asset today
    underlying_price = getUnderlyingData(single_date, df=underlyingData)

    # calculate the NAV
    nav = cash
    if shares[1] > 0:
        underlying_price = getUnderlyingData(single_date, df=underlyingData)
        if underlying_price != None:
            nav = cash + (underlying_price * shares[1])
            dailyPnL.append(nav-500000)
        else:
            dailyPnL.append(dailyPnL[-1])
            
    else:
        dailyPnL.append(nav-500000)

    dates.append(single_date)
    costArr.append(costBasis)

# end of strategy
print(pnl)
print(cash)
# check for any shares left
# print(dailyPnL)
df = pd.DataFrame(dailyPnL)
df.index = dates
df['costBase'] = costArr
df.to_csv("trader2pnl.csv")
