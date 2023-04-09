from datetime import datetime,timedelta

#Format number
def format_number(curr_number,match_number):
    curr_number_string=f"{curr_number}"
    match_number_string=f"{match_number}"
    
    if "." in match_number_string:
        match_decimal = len(match_number_string.split(".")[1])
        curr_number_string = f"{curr_number:.{match_decimal}f}"
        curr_number_string = curr_number_string[:]
        return curr_number_string
    else :
        return f"{int(curr_number)}"

#format time
def format_time(timestamp):
    return timestamp.replace(microsecond=0).isoformat()    
    
#get ISO times
def  get_ISO_times(): 
    
    #get timestamps
    date_start_0=datetime.now()
    date_start_1=date_start_0-timedelta(hours=100)
    date_start_2=date_start_1-timedelta(hours=100)
    date_start_3=date_start_2-timedelta(hours=100)
    date_start_4=date_start_3-timedelta(hours=100)
      
    #format datetimes
    times_dict = {
        "range_1":{
        "from_iso":format_time(date_start_1),
        "to_iso"  :format_time(date_start_0),
        },
        "range_2":{
        "from_iso":format_time(date_start_2),
        "to_iso"  :format_time(date_start_1),
        },
        "range_3":{
        "from_iso":format_time(date_start_3),
        "to_iso"  :format_time(date_start_2),
        },
        "range_4":{
        "from_iso":format_time(date_start_4),
        "to_iso"  :format_time(date_start_3),
        },  
    }  
    
    return times_dict