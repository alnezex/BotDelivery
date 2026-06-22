from abc import ABC, abstractmethod
import csv

class Order:
    def __init__(self, price: int, name: str):
        self.price = price
        self.name = name
    def change_name(self, new_name: str):
        self.name = new_name
    def change_price(self, new_price: int):
        self.price = new_price
    def __str__(self):
        return f'{self.name}, {self.price}'
    def __repr__(self):
        return f'{self.name}, {self.price}'
    def transform(self):
        return {'name': self.name, 'price': self.price}
