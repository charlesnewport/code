import random
import json
import os

def loadJson(name):
	with open('data/' + name, 'r') as file:
		data = json.load(file)
	return data

def names():
	return [f for f in os.listdir(os.getcwd() + '/data') if f.find('json') != -1]

class Disease:
	def __init__(self):
		d = loadJson(random.choice(names()))
		self.name = d['name']
		self.multG = d['multG']
		self.distG = d['distG']
		self.hLimit = 1000

	def effects(self, bee):
		vals = bee.__dict__.keys()
		for v in vals:
			if v in self.__dict__:
				bee.__dict__[v] = self.__dict__[v]