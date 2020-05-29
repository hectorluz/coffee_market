from mesa import Agent

class MoneyAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, N, fixed, rnd):
        super().__init__(unique_id, model)
        self.wealth = 0
        self.color = 'black'
        self.coffee_age = 0
        self.cost = fixed + self.random.randint(0,rnd)
        self.green_marker = 0
        self.grow = 0
        if self.random.randint(0,100) < N:
            if self.random.randint(0,100) < 50:
                self.color = 'green'
            else:
                self.color = 'yellow'        


    def move(self):
        if self.color == "black":
            if self.model.price > self.cost:
                self.grow = 8 - [neighbor.color for neighbor in self.model.grid.neighbor_iter(self.pos)].count('black')
                if self.grow > self.model.min_neighbor:
                    self.color = 'green'
                    self.grow = 0
        if self.color == "yellow":
            self.wealth = self.wealth + (self.model.price - self.cost)
            if self.wealth < 0:
                self.color = "black"
                self.coffee_age = 0
        if self.color == "green":
            if self.coffee_age >= 4:
                self.color = "yellow"
            self.coffee_age += 1
        if self.model.burn == True:
            self.cost = (1+self.model.tax)*self.cost


    def step(self):
        self.move()
