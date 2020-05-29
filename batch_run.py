from coffee_market.model import MoneyModel
import pandas as pd

m = MoneyModel(30,50,50,50,100,0.01,70,30,False,False,False)

import time
start_time = time.time()
for i in range(0,100):
    m.step()
print(f'{time.time()-start_time}')


