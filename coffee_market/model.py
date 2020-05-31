from coffee_market.agents import MoneyAgent

from mesa import Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner
import pandas as pd
import time

def compute_supply(model):
    return int(model.supply)
def compute_price(model):
    return int(model.price)
def compute_stock(model):
    return int(model.stock)
def compute_burned(model):
    return int(model.burned)    

class MoneyModel(Model):
    """A model with some number of agents."""
    def __init__(self, N, width, height,init_price,init_ei,grow_ei,fixed,rnd,p_q,p_ei,min_neighbor,sub,subsell,burn, seed=None):
        self.num_agents = (width * height)
        self.grid = SingleGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.ext_inc = init_ei
        self.grow_ei = grow_ei
        self.min_neighbor = min_neighbor
        self.p_q = p_q
        self.p_ei = p_ei
        self.last_price = 0
        self.price = self.init_price = init_price
        self.tick = 0
        self.true_supply = 0
        self.stock = 0
        self.subtrue = False
        self.sub = sub
        self.subsell = subsell
        self.burn = burn
        self.burned = 0
        self.tax = 0

        print(f'{p_q}, {p_ei}, {min_neighbor}')

        # Create agents
        for i in range(self.num_agents):
            a = MoneyAgent(i, self, N, fixed, rnd)
            self.schedule.add(a)
            self.grid.place_agent(a, (0, 0))
            if i < self.num_agents - 1:
                self.grid.move_to_empty(a)
        self.supply = [k.color for k in self.schedule.agents].count('yellow')

        self.datacollector = DataCollector(
            model_reporters={"Supply": compute_supply, "Price": compute_price, "Stock": compute_stock, "Burned": compute_burned}
            #agent_reporters={"Wealth": "wealth"}
        )

        #print(f'start time: {time.time() - start_time}')

    def market(self):
        self.tick += 1
        print(self.tick)
        self.last_price = self.price
        self.ext_inc = self.ext_inc * (1 + self.grow_ei)
        self.supply = [k.color for k in self.schedule.agents].count('yellow')
        self.price = max(0,(self.init_price + (self.p_ei * self.ext_inc) - (self.p_q * self.supply)))
        
        if self.sub == True:
            if self.price < 0.9*self.last_price:
                self.true_supply = (50 * ((self.init_price) + (0.2 * self.ext_inc) - (0.9*self.last_price)))
                self.stock = (self.stock + (self.supply - self.true_supply))
                self.price = (0.9*self.last_price)
                self.subtrue = True
            if self.tick < 10:
                self.stock = 0

        if self.subsell == True:
            if self.stock > 0:
                if self.price > self.last_price:
                    if self.subtrue == True:
                        self.supprice = self.init_price + (0.2 * self.ext_inc) - (0.01 * (self.supply + self.stock))
                        if self.supprice >= self.last_price:
                            self.price = self.supprice
                            self.stock = 0
                        else:
                            self.price = self.last_price
                            self.true_supply = (50 * ((self.init_price) + (0.2 * self.ext_inc) - (0.9*self.last_price)))
                            self.stock = self.stock - (self.true_supply - self.supply)

        if self.burn == True:
            if self.stock >= 0:
                self.tax = 0.5 * (self.stock / (self.supply + 0.1))
                self.burned = (self.burned + self.stock)
                self.stock = 0
            
    def step(self):
        start_time = time.time()
        self.schedule.step()
        print(f'schedule time: {time.time() - start_time}')
        start_time = time.time()
        self.market()
        print(f'market time: {time.time() - start_time}')
        start_time = time.time()
        self.datacollector.collect(self)
        print(f'datacollector time: {time.time() - start_time}')
