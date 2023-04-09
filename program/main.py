
from constants import ABORT_ALL_POSITION,FIND_COINTEGRATED
from func_connections import connect_dydx
from func_private import abort_all_positions
from func_public import construct_market_prices
from func_cointegration import store_cointegration_result

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
        
    #store cointegrated pairs    
    try :
        print ("Sto salvando le coppie di coin...")
        store_result = store_cointegration_result(df_market_prices)
        if store_result != "saved" :
            print ("Errore nel salvere le coppie di valute")
            exit(1)
    except Exception as e:
        print("Errore nel salvere le coppie di valute : ",e)    
        exit(1)      