from constants import ZSCORE_THRESH,USD_PER_TRADE,USD_MIN_COLLATERAL
from func_utils import format_number
from func_public import get_candles_recent
from func_cointegration import calculate_zscore
from func_private import is_open_positions
from func_bot_agent  import BotAgent
import pandas as pd
import json
from pprint import pprint

#open positions
def open_positions(client):
    #load cointegrated pairs
    df = pd.read_csv("cointegrated_pairs.csv")
    #get market for referencing
    markets=client.public.get_markets().data
    bot_agents = []
    # Opening JSON file
    try:
        open_positions_file = open("bot_agents.json")
        open_positions_dict = json.load(open_positions_file)
        for p in open_positions_dict:
         bot_agents.append(p)
    except:
      bot_agents = []
    #zscore triggers
    for index,row in df.iterrows():
        #get variables
        base_market = row["base_market"]
        quote_market = row["quote_market"]
        hedge_ratio = row["hedge_ratio"]
        half_life = row["half_life"]
        
        #get price
        series1=get_candles_recent(client,base_market)
        series2=get_candles_recent(client,quote_market)
        
        #get zscore
        if len(series1) > 0 and len(series1) == len(series2) :
            spread = series1 - (hedge_ratio * series2)
            zscore = calculate_zscore (spread).values.tolist()[-1]
            
            #stabilisce un trade potenziale
            if abs(zscore) >= ZSCORE_THRESH :
                #trade potenziale
                is_base_open = is_open_positions(client,base_market)
                is_quote_open = is_open_positions(client,quote_market)
                
                if not is_base_open and not is_quote_open :
                    #determina la direzione
                    base_side = "BUY" if zscore < 0 else "SELL"
                    quote_side = "BUY" if zscore > 0 else "SELL"
                    
                    #calcola un prezzo accettabile
                    base_price = series1[-1] 
                    quote_price = series2[-1]   
                    accept_base_price = float(base_price) *1.01 if zscore < 0 else float(base_price) *0.99
                    accept_quote_price = float(quote_price) *1.01 if zscore > 0 else float(quote_price) *0.99
                    failsafe_base_price = float(base_price) *0.05 if zscore < 0 else float(base_price) *1.7
                    base_tick_size=markets["markets"][base_market]["tickSize"]
                    quote_tick_size=markets["markets"][quote_market]["tickSize"]
                    
                    #format price
                    accept_base_price = format_number(accept_base_price,base_tick_size)
                    accept_quote_price = format_number(accept_quote_price,quote_tick_size)
                    accept_failsafe_base_price = format_number(failsafe_base_price,base_tick_size)
                    
                    #quantità
                    base_quantity =1 / base_price * USD_PER_TRADE
                    quote_quantity =1 / quote_price * USD_PER_TRADE
                    base_step_size = markets["markets"][base_market]["stepSize"]
                    quote_step_size = markets["markets"][quote_market]["stepSize"]
                    
                    #format size
                    base_size = format_number (base_quantity,base_step_size)
                    quote_size = format_number (quote_quantity,quote_step_size)
                    
                    #min order dydx
                    base_min_order_size = markets["markets"][base_market]["minOrderSize"]
                    quote_min_order_size = markets["markets"][quote_market]["minOrderSize"]
                    check_base = float(base_quantity) > float(base_min_order_size)
                    check_quote = float(quote_quantity) > float(quote_min_order_size)
                    
                    #if ceck pass place trade
                    if check_base and check_quote :
                        
                        #ceck account balance
                        account = client.private.get_account()
                        free_collateral=float(account.data["account"]["freeCollateral"])
                        
                        print(f"Balance : {free_collateral} and minimun at {USD_MIN_COLLATERAL}")
                        
                        if free_collateral < USD_MIN_COLLATERAL :
                            break
                        
                        #create bot agent
                        bot_agent = BotAgent(
                            client,
                            market_1=base_market,
                            market_2=quote_market,
                            base_side=base_side,
                            base_size=base_size,
                            base_price=accept_base_price,
                            quote_side=quote_side,
                            quote_size=quote_size,
                            quote_price=accept_quote_price,
                            accept_failsafe_base_price=accept_failsafe_base_price,
                            z_score=zscore,
                            half_life=half_life,
                            hedge_ratio=hedge_ratio
                        )
                        
                        #open trade
                        bot_open_dict = bot_agent.open_trades()
                        
                        # Guard: Handle failure
                        if bot_open_dict == "failed":
                           continue
                        
                        # Handle success in opening trades
                        if bot_open_dict["pair_status"] == "LIVE":
                           # Append to list of bot agents
                           bot_agents.append(bot_open_dict)
                           del(bot_open_dict)
                           # Confirm live status in print
                           print("Trade status: Live")
                           print("---")
                            
    # Save agents
    print(f"Success: Manage open trades checked")
    if len(bot_agents) > 0:
        with open("bot_agents.json", "w") as f:
         json.dump(bot_agents, f)