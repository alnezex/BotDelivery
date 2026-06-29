from aiogram.types import BotCommand
import heapq






def get_admin_cmd():
    return BotCommand(command='admin', description='Команда главаря')





class Delivery:
    def __init__(self, delivery_repository):
        self.graph_city = {} # {A: {B: 34, C: 2, E: 8}, B: {A: 34, C: 8, G: 9}}
        
        for city in delivery_repository.get_cities():
            self.graph_city[city] = delivery_repository.get_roads(city)
        

        
        # reader = csv.DictReader(file)
        # for row in reader:
        #     if row['dest1'] not in self.graph_city:
        #         self.graph_city[row['dest1']] = {}
        #     if row['dest2'] not in self.graph_city:
        #         self.graph_city[row['dest2']] = {}
        #     self.graph_city[row['dest1']][row['dest2']] = row['time']
        #     self.graph_city[row['dest2']][row['dest1']] = row['time']

    def dijkstra(self, start, finish):
        if start == finish:
            return '20 минут'


        distances = {vertex: float('infinity') for vertex in self.graph_city}

        distances[start] = 0


        priority_queue = [(0, start)]
        while priority_queue:

            current_distance, current_vertex = heapq.heappop(priority_queue)

            if current_distance > distances[current_vertex]:
                continue
        
            for neighbor, weight in self.graph_city[current_vertex].items():
                distance = float(current_distance) + float(weight)

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))
        
        return distances[finish]
