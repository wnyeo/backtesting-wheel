import pandas as pd
from datetime import date, datetime
import yfinance as yf # For downloading historical price data of the ETF

# function to get the data for a particular date (with processing)
def getCallData(givenDate):
    year = givenDate.strftime("%Y")
    month = givenDate.strftime("%m")
    day = givenDate.strftime("%d")
    df = pd.read_csv('data/spy_eod_' + year + '/spy_eod_' + year + month + '.txt', low_memory=False)

    givenDate = " " + givenDate.strftime("%Y-%m-%d")
    try: 
    # filter out the relevant rows
        df = df.loc[df[' [QUOTE_DATE]'] == givenDate]

        # filter out relevant rows with DTE 35 < x < 45
        df = df.loc[df[' [DTE]'] > 35]
        df = df.loc[df[' [DTE]'] < 45]
        
        # filter out relevant rows with C_DELTA nearest to 0.30
        df = df.loc[df[' [C_DELTA]'] > 0.2]
        df = df.loc[df[' [C_DELTA]'] < 0.3]

        # return row that has delta closest to 0.30
        df = df.sort_values(by=' [C_DELTA]', ascending=False).reset_index(drop=True)

        expiry = df.loc[0][' [EXPIRE_DATE]'][1:]
        expiry = datetime.strptime(expiry, '%Y-%m-%d').date()
        price = float(df.loc[0][' [C_LAST]'])
        dte = int(df.loc[0][' [DTE]'])
        strike = float(df.loc[0][' [STRIKE]'])
        underlying = float(df.loc[0][' [UNDERLYING_LAST]'])
        delta = float(df.loc[0][' [C_DELTA]'])

        # return price, dte, expdate, strike, underlying price, delta
        if price > 0:
            return price, dte, expiry, strike, underlying, delta

        return None
    
    except:
        return None

# print(getCallData(date(2018, 1, 2)))


# function to get the data for a particular date (with processing)
def getPutData(givenDate):
    year = givenDate.strftime("%Y")
    month = givenDate.strftime("%m")
    day = givenDate.strftime("%d")
    df = pd.read_csv('data/spy_eod_' + year + '/spy_eod_' + year + month + '.txt', low_memory=False)

    givenDate = " " + givenDate.strftime("%Y-%m-%d")

    try:
        # filter out the relevant rows
        df = df.loc[df[' [QUOTE_DATE]'] == givenDate]

        # filter out relevant rows with DTE 35 < x < 45
        df = df.loc[df[' [DTE]'] > 35]
        df = df.loc[df[' [DTE]'] < 45]
        
        # filter out relevant rows with P_DELTA nearest to 0.30
        df = df.loc[df[' [P_DELTA]'] > -0.3]
        df = df.loc[df[' [P_DELTA]'] < -0.2]

        # return row that has delta closest to -0.30
        df = df.sort_values(by=' [P_DELTA]', ascending=True).reset_index(drop=True)

        expiry = df.loc[0][' [EXPIRE_DATE]'][1:]
        expiry = datetime.strptime(expiry, '%Y-%m-%d').date()
        price = float(df.loc[0][' [P_LAST]'])
        dte = int(df.loc[0][' [DTE]'])
        strike = float(df.loc[0][' [STRIKE]'])
        underlying = float(df.loc[0][' [UNDERLYING_LAST]'])
        delta = float(df.loc[0][' [P_DELTA]'])

        # print(type(price), type(dte), type(expiry), type(strike), type(underlying), type(delta))
    
        # return price, dte, expdate, strike, underlying price, delta
        if price > 0:
            return price, dte, expiry, strike, underlying, delta

        return None

    except:
        return None

# print(getPutData(date(2018, 1, 10)))

def underlyingFromOptions(givenDate):
    year = givenDate.strftime("%Y")
    month = givenDate.strftime("%m")
    day = givenDate.strftime("%d")
    df = pd.read_csv('data/spy_eod_' + year + '/spy_eod_' + year + month + '.txt', low_memory=False)

    givenDate = " " + givenDate.strftime("%Y-%m-%d")

    try:
        # filter out the relevant rows
        df = df.loc[df[' [QUOTE_DATE]'] == givenDate].reset_index(drop=True)
        underlying = float(df.loc[0][' [UNDERLYING_LAST]'])
        return underlying
    
    except:
        return None