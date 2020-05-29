## rever o momento em que o cara fica verde; tem que ter um marcador e ele ficar verde só no início da rodada seguinte;

from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from .model import MoneyModel

class SupplyElement(TextElement):
    '''
    Display a text count of how many happy agents there are.
    '''

    def __init__(self):
        pass

    def render(self, model):
        return "A oferta é igual a " + str(model.supply) + " e o preço a " + str(round(model.price,2))

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 1,
                 #"w": 1,
                 #"h": 1,
                 "Layer": 0,
                 "Color": agent.color}

    return portrayal

model_params = {"init_people": UserSettableParameter("slider", "Densidade (%)", 20, 1, 100,
                                                    description="Densidade de produtores"),
                "init_price": UserSettableParameter("number","Preço Inicial",100,0,200,
                                                    description="Custo Variável"),
                "init_ei": UserSettableParameter("number","Init-ei",100,0,200,
                                                    description="Custo Variável"),
                "grow_ei": UserSettableParameter("number","Grow-ei",0.015,0,0.2,step=0.01,
                                                    description="Custo Variável"),
                "fixed": UserSettableParameter("number","Custo Fixo",100,0,100,
                                                    description="Custo fixo"),
                "rnd": UserSettableParameter("number","Custo Variável",30,0,100,
                                                    description="Custo Variável"),
                "p_q": UserSettableParameter("number","del p/del q",0.02,0,0.2,
                                                    description="del p/del q"),
                "p_ei": UserSettableParameter("number","del p/del ei",0.2,0,1,
                                                    description="del p/del ei"),
                "min_neighbor": UserSettableParameter("number","Mín. Vizinho",1,0,9,
                                                    description="Min Vizinho"),                                                                                                                                                            
                "sub": UserSettableParameter("checkbox","Subsídio",False),
                "subsell": UserSettableParameter("checkbox","Subsídio e venda",False),
                "burn": UserSettableParameter("checkbox","Queima",False)
}

supply_element = SupplyElement()
grid = CanvasGrid(agent_portrayal, 100, 100, 500, 500)

chart = ChartModule([
    {
        "Label": "Supply",
        "Color": "Yellow"
    },{
        "Label":"Price",
        "Color":"Green"
    },{
        "Label":"Stock",
        "Color":"Blue"
    },{
        "Label":"Burned",
        "Color":"Red"                          
    }
    ],
    data_collector_name='datacollector')

server = ModularServer(MoneyModel,
                       [
                           grid, 
                           supply_element,
                           chart,
                       ],
                       "Money Model",
                       {"N":model_params['init_people'], 
                       "width":100, 
                       "height":100,
                        "init_price":model_params['init_price'],
                        "init_ei":model_params['init_ei'],
                        "grow_ei":model_params['grow_ei'],
                        "fixed":model_params['fixed'],
                        "rnd":model_params['rnd'],
                        "p_q":model_params['p_q'],
                        "p_ei":model_params['p_ei'],
                        "min_neighbor":model_params['min_neighbor'],
                        "sub":model_params['sub'],
                        "subsell":model_params['subsell'],
                        "burn":model_params['burn'],
                        "seed":0})
server.port=8521