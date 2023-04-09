
from func_utils import get_ISO_times
from pprint import pprint
from constants import RESOLUTION
import pandas as pd
import numpy as np
import time

#get relevant period for iso from and to
ISO_TIMES=get_ISO_times() 

pprint(ISO_TIMES)

#construct market prices
def construct_market_prices(client):
    pass