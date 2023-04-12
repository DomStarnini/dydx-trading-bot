from func_private import place_market_order,ceck_order_status
from datetime import datetime,timedelta
import time
from pprint import pprint

#class agent for opening and closing order

class BotAgent:
    
    #initialize
    def __init__(
        self,
        client,
        market_1,
        market_2,
        base_side,
        base_size,
        base_price,
        quote_size,
        quote_price,
        quote_side,
        accept_failsafe_base_price,
        z_score,
        half_life,
        hedge_ratio
    ) :
        #initialize class variable
        self.client=client
        self.market_1=market_1
        self.market_2=market_2
        self.base_side=base_side
        self.base_size=base_size
        self.base_price=base_price
        self.quote_size=quote_size
        self.quote_price=quote_price
        self.quote_side=quote_side
        self.accept_failsafe_base_price=accept_failsafe_base_price
        self.z_score=z_score
        self.half_life=half_life
        self.hedge_ratio=hedge_ratio
        
        #initalize output variable
        #pair status opions are FAILED, LIVE, CLOSE, ERROR
        self.order_dict = {
            
            "market_1":market_1,
            "market_2":market_2,
            "hedge_ratio":hedge_ratio,
            "half_life":half_life,
            "z_score":z_score,
            "order_id_m1":"",
            "order_m1_size":base_size,
            "order_m1_side":base_side,
            "order_time_m1":"",
            "order_id_m2":"",
            "order_m2_size":base_size,
            "order_m2_side":base_side,
            "order_time_m2":"",
            "pair_status":"",
            "comments":"",
        }
        
    #ceck order status by id
    def ceck_order_status_by_id (self,order_id) :
        
        #allow time to order
        time.sleep(2)
        
        #ceck order status
        order_status = ceck_order_status (self.client, order_id)
        
        if order_status == "CANCELED" :
            print("{self.market_1} VS {self.market_2} Ordine Cancellato...." )
            self.order_dict["pair_status"] = "FAILED"
            return "failed"
        
        if order_status != "FAILED" :
            time.sleep(15)
            order_status = ceck_order_status (self.client, order_id)
            
            if order_status == "CANCELED" :
                print("{self.market_1} VS {self.market_2} Ordine Cancellato...." )
                self.order_dict["pair_status"] = "FAILED"
                return "failed"
            
        if order_status != "FILLED":
            self.client.private.cancel_order(order_id = order_id)    
            self.order_dict["pair_status"] = "FAILED"
            return "error"
        
        return "live"    

    #open trades
    def open_trades (self):
        
        print("-------")
        print(f"{self.market_1}: apertura primo ordine...")
        print(f"Side : {self.base_side}, Size : {self.base_size}, Price : {self.base_price}")
        print("-------")
        
        #place base order
        try :
            base_order = place_market_order(
                self.client,
                market=self.market_1,
                side=self.base_side,
                size=self.base_size,
                price=self.base_price,
                reduce_only=False
            )
            #store the order
            self.order_dict["order_id_m1"] = base_order["order"]["id"]
            self.order_dict["order_time_m1"] = datetime.now().isoformat()
        except Exception as e :
            self.order_dict["status"] = "ERROR"
            self.order_dict["comments"] = f"Market 1 {self.market_1}:, {e}"
            return self.order_dict
        #ceck is order online
        order_status_m1 = self.ceck_order_status_by_id(self.order_dict["order_id_m1"])
        
        if order_status_m1 != "live":
            self.order_dict["status"] = "ERROR"
            self.order_dict["comments"] = f"{self.market_1} fallito"
            return self.order_dict
        
        print("-------")
        print(f"{self.market_2}: apertura secondo ordine...")
        print(f"Side : {self.quote_side}, Size : {self.quote_size}, Price : {self.quote_price}")
        print("-------")
        
        #place base order
        try :
            quote_order = place_market_order(
                self.client,
                market=self.market_2,
                side=self.quote_side,
                size=self.quote_size,
                price=self.quote_price,
                reduce_only=False
            )
            #store the order
            self.order_dict["order_id_m2"] = quote_order["order"]["id"]
            self.order_dict["order_time_m2"] = datetime.now().isoformat()
        except Exception as e :
            self.order_dict["status"] = "ERROR"
            self.order_dict["comments"] = f"Market 2 {self.market_1}:, {e}"
            return self.order_dict
        #ceck is order online
        order_status_m1 = self.ceck_order_status_by_id(self.order_dict["order_id_m2"])
        
        if order_status_m1 != "live":
            self.order_dict["status"] = "ERROR"
            self.order_dict["comments"] = f"{self.market_2} fallito"
            return self.order_dict
        
        
        #ceck is order online
        order_status_m2 = self.ceck_order_status_by_id(self.order_dict["order_id_m1"])
        
        if order_status_m2 != "live":
            self.order_dict["status"] = "ERROR"
            self.order_dict["comments"] = f"{self.market_2} fallito"
        
            #close order 1
            try :
                quote_order = place_market_order(
                    self.client,
                    market=self.market_1,
                    side=self.quote_side,
                    size=self.base_size,
                    price=self.accept_failsafe_base_price,
                    reduce_only=True
                )
                time.sleep(2)
                order_status_close_order= ceck_order_status(self.client,close_order["order"]["id"])
                if order_status_close_order != "FILLED":
                    print("ABORT PROGRAM")
                    print("Unexpected error")
                    print(order_status_close_order)
                    exit(1)
            except Exception as e :
                self.order_dict["status"] = "ERROR"
                self.order_dict["comments"] = f"Close Market 1 {self.market_1}:, {e}"
                print("ABORT PROGRAM")
                print("Unexpected error")
                print(order_status_close_order)
                exit(1)
        else :
              self.order_dict["pair status"]="LIVE"
              return self.order_dict