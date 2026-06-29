from main import database
from utils import Delivery


deliv = Delivery(database)



print(deliv.dijkstra('Москва','Воронеж')) 