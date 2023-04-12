
from func_utils import get_ISO_times
from pprint import pprint
from constants import RESOLUTION
import pandas as pd
import numpy as np
import time

#get relevant period for iso from and to
ISO_TIMES=get_ISO_times() 

#get candles recent
def get_candles_recent(client,market):
    #output
    close_prices=[]
    #protect api
    time.sleep(0.2)
    #get candles
    candles = client.public.get_candles(
        market=market,
        resolution=RESOLUTION,
        limit=100
    ) 
    #structure data
    for candle in candles.data["candles"]:
        close_prices.append(candle["close"])
    #return close
    close_prices.reverse()  
    price_result=np.array(close_prices).astype(np.float)  
    return price_result
#get historical candles
def get_candles_historical(client, market):
    
    #define output
    close_price = []
    
    #extract historical price from ISO_TIMES
    for timeframe in ISO_TIMES.keys():
        tf_obj = ISO_TIMES[timeframe]
        from_iso = tf_obj["from_iso"]
        to_iso = tf_obj["to_iso"]
        
        #protect API
        time.sleep(0.2)
    
    #get data
    candles = client.public.get_candles(
        
        market=market,
        resolution=RESOLUTION,
        from_iso = from_iso,
        to_iso = to_iso,
        limit = 100
    ) 
    
    #structure data
    for candle in candles.data["candles"]:
        close_price.append({"datetime": candle["startedAt"], market : candle["close"]})   
        
    #construct and reverse dataframe
    close_price.reverse()
    return close_price   
    

#construct market prices
def construct_market_prices(client):
    
    #declare variables
    tradeable_markets = []
    markets = client.public.get_markets()
    
    #find tradeable pairs
    for market in markets.data["markets"].keys():
        market_info = markets.data["markets"][market]
        if market_info["status"] == "ONLINE" and market_info["type"] == "PERPETUAL" :
            tradeable_markets.append(market)
    
    #set initial dataframe
    close_prices = get_candles_historical (client , tradeable_markets[0])
    df = pd.DataFrame(close_prices)
    df.set_index("datetime", inplace=True)
    
    for market in tradeable_markets [1:]:#in produzione
        close_prices_add = get_candles_historical (client , market)
        df_add = pd.DataFrame(close_prices_add)
        df_add.set_index("datetime", inplace=True)
        df = pd.merge(df, df_add, how="outer", on="datetime", copy=False)
        del df_add
        
        nans = df.columns [df.isna().any()].tolist()
        if len(nans) > 0 :
            print ("Dropping columns : ")
            print (nans)
            df.drop(columns=nans, inplace=True)
    
   
    return df
    
    
    
    
    
    
    
    
    
    
    