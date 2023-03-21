import pandas as pd
from datetime import date, datetime
import yfinance as yf # For downloading historical price data of the ETF

# function to get the data for a particular date (with processing)
def getCallData(givenDate):
    year = givenDate.strftime("%Y")
    month = givenDate.strftime("%m")
    day = givenDate.strftime("%d")
    df = pd.read_csv('data/spy_eod_' + year + '/spy_eod_' + year + month + '.txt')

    givenDate = " " + givenDate.strftime("%Y-%m-%d")
    try: 
    # filter out the relevant rows
        df = df.loc[df[' [QUOTE_DATE]'] == givenDate]

        # filter out relevant rows with DTE 35 < x < 45
        df = df.loc[df[' [DTE]'] > 35]
        df = df.loc[df[' [DTE]'] < 45]
        
        # filter out relevant rows with C_DELTA nearest to 0.35
        df = df.loc[df[' [C_DELTA]'] > 0.3]
        df = df.loc[df[' [C_DELTA]'] < 0.4]

        # return row that has delta closest to 0.35
        df = df.iloc[(df[' [C_DELTA]']-0.35).abs().argsort()][:1].reset_index(drop=True)

        expiry = df.loc[0][' [EXPIRE_DATE]'][1:]
        
        expiry = datetime.strptime(expiry, '%Y-%m-%d').date()
        # return price, dte, expdate, strike, underlying price, delta
        return df.loc[0][' [C_LAST]'], df.loc[0][' [DTE]'], expiry, df.loc[0][' [STRIKE]'], df.loc[0][' [UNDERLYING_LAST]'], df.loc[0][' [C_DELTA]'], 

    except:
        return None
    # return individual values
# print(getCallData(date(2018, 1, 10)))


# function to get the data for a particular date (with processing)
def getPutData(givenDate):
    year = givenDate.strftime("%Y")
    month = givenDate.strftime("%m")
    day = givenDate.strftime("%d")
    df = pd.read_csv('data/spy_eod_' + year + '/spy_eod_' + year + month + '.txt')

    givenDate = " " + givenDate.strftime("%Y-%m-%d")

    try:
        # filter out the relevant rows
        df = df.loc[df[' [QUOTE_DATE]'] == givenDate]

        # filter out relevant rows with DTE 35 < x < 45
        df = df.loc[df[' [DTE]'] > 35]
        df = df.loc[df[' [DTE]'] < 45]
        
        # filter out relevant rows with C_DELTA nearest to 0.35
        df = df.loc[df[' [P_DELTA]'] > -0.4]
        df = df.loc[df[' [P_DELTA]'] < -0.3]

        # return row that has delta closest to 0.35
        df = df.iloc[(df[' [P_DELTA]']- (-0.35)).abs().argsort()][:1].reset_index(drop=True)

        expiry = df.loc[0][' [EXPIRE_DATE]'][1:]
        
        expiry = datetime.strptime(expiry, '%Y-%m-%d').date()
        # return price, dte, expdate, strike, underlying price, delta
        return df.loc[0][' [P_LAST]'], df.loc[0][' [DTE]'], expiry, df.loc[0][' [STRIKE]'], df.loc[0][' [UNDERLYING_LAST]'], df.loc[0][' [P_DELTA]'], 

    except:
        return None
    # return individual values
# print(getPutData(date(2018, 1, 10)))

# Define the start and end dates for the backtest
startDate = date(2018, 1, 2)
endDate = date(2023, 1, 1)
ticker = "SPY"

# function to get data from yfinance
def getStockData(ticker, start_date, end_date, givenDate):
    # symbol = "SPY"
    data = yf.download(ticker, start=start_date, end=end_date)
    givenDate = givenDate.strftime("%Y-%m-%d")
    try:
        print(data.loc[givenDate]['Close'])
    # return data
    except:
        print("no data")
        return None
getStockData(ticker, startDate, endDate, date(2018, 1, 10))




