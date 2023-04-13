
from constants import ABORT_ALL_POSITION,FIND_COINTEGRATED,PLACE_TRADES,MANAGE_EXIT
from func_connections import connect_dydx
from func_private import abort_all_positions
from func_public import construct_market_prices
from func_cointegration import store_cointegration_result
from func_entry_pairs import open_positions
from func_exit_pairs import manage_trade_exits

if __name__=="__main__":
    #connect to client
    try:
        print("Sto connettendo al client...")
        client=connect_dydx()
    except Exception as e:
        print(e)
        print("Errore di connessione : ",e)    
        exit(1)
    
    
#abort all position
if ABORT_ALL_POSITION :
    try :
        print ("Sto chiudendo tutte lo posizioni aperte...")
        close_orders=abort_all_positions(client)
    except Exception as e:
        print("Errore di chiusura posizioni : ",e)    
        exit(1)   
        
#find cointegrated pairs
if FIND_COINTEGRATED : 
    #construct market pairs
    try :
        print ("Sto costruendo i prezzi di mercato...")
        df_market_prices = construct_market_prices(client)
    except Exception as e:
        print("Errore di costruzione prezzi di mercato : ",e)    
        exit(1)  
# Run as always on
while True:  
    if MANAGE_EXIT :
        try :
            print ("Sto gestendo le uscite...")
            manage_trade_exits(client)
        except Exception as e:
            print("Errore nel gestire le uscite : ",e)    
            exit(1)            
            
    #place trades for opening positions
    if PLACE_TRADES :
        try :
            print ("Sto cercando opportunità di trading...")
            open_positions(client)
        except Exception as e:
            print("Errore nel trovare pairs : ",e)    
            exit(1)      