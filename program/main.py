
from constants import ABORT_ALL_POSITION,FIND_COINTEGRATED
from func_connections import connect_dydx
from func_private import abort_all_positions
from func_public import construct_market_prices

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
        print ("Sto chiudendo tutte lo posizioni aperte")
        close_orders=abort_all_positions(client)
    except Exception as e:
        print("Errore di chiusura posizioni : ",e)    
        exit(1)   
        
#find cointegrated pairs
if FIND_COINTEGRATED : 
    try :
        print ("Sto costruendo i prezzi di mercato aspetta 3 minuti")
        df_market_prices = construct_market_prices(client)
    except Exception as e:
        print("Errore di costruzione prezzi di mercato : ",e)    
        exit(1)              