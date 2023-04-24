from datetime import datetime,timedelta
import time
from pprint import pprint
from func_utils import format_number
import json

#is open positions
def  is_open_positions(client,market):
    #protect API
    time.sleep(0.2)
    #get positions
    all_positions=client.private.get_positions(
        market=market,
        status="OPEN"
    )
    #determine is open
    if len(all_positions.data["positions"]) >0 :
        return True
    else :
        return False
    
#ceck orders
def check_order_status(client,order_id):
    order=client.private.get_order_by_id(order_id)
    if order.data :
        if "order" in order.data.keys():
            return order.data["order"]["status"]
    return "FAILED"

#place market order
def place_market_order (client,market,side,size,price,reduce_only):
    #get position id
    account_response=client.private.get_account()
    position_id=account_response.data["account"]["positionId"]

    #place order
    place_order=client.private.create_order(
    position_id=position_id,
    market=market,
    side=side,
    order_type="MARKET",
    post_only=False,
    size=size,
    price=price*0.9,
    limit_fee='0.015',
    expiration_epoch_seconds=time.time() + 500,
    time_in_force="FOK",
    reduce_only=reduce_only
    )
    #return order
    return place_order.data


def abort_all_positions(client):
    #cancel all orders
    client.private.cancel_all_orders()
    #protect API
    time.sleep(0.5)
    
    #get markets reference
    markets=client.public.get_markets().data
    
    #protect API
    time.sleep(0.5)
    
    #get all open position
    positions=client.private.get_positions(status="OPEN")
    all_positions=positions.data["positions"]
    #print(all_positions)
    #handle positons
    close_orders=[]
    if len(all_positions)>0:
        for position in all_positions:
            
            #determine market
            market=position["market"]
            
            #determine side
            side="BUY"
            if position["side"]=="LONG":
               side="SELL"
               
            #get price
            price = float(position["entryPrice"])
            accept_price = price*1.7 if side=="BUY" else price*0.3
            tick_size=markets["markets"][market]["tickSize"]
            accept_price=format_number(accept_price,tick_size)
            
            #place order to close
            order=place_market_order(
                client,
                market,
                side,
                position["sumOpen"],
                accept_price,
                True
                )
            
            #append the orders
            close_orders.append(order)
            
            #save API
            time.sleep(0.2)
            
        bot_agents=[]
        with open("bot_agents.json", "w") as f:
         json.dump(bot_agents, f)
        
    #return close_orders
    return close_orders    