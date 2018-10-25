"""
OOP Neural Network Prototype

Written by Stephan Kashkarov finished: 22/05/2018

This is a collection of classes that can be put together
to make a neural network. An example of complete network
is provided in neuralNetworkExample.py

I feel like i could refactor this if i get the time

This network cannot be trained as I have a weak understanding
of backpropogation

TODO:
	- Add training system,
	- Refactor neuron classes with inheritance

Classes:
	-> Neurons
		-> Start_Neuron (first row neuron)
		-> Hidden_Neuron (center row neuron)
		-> End_Neuron (end row neurons)
	-> Row (a collection of neurons)

Functions:
	-> sigmoid

"""
import math as m
import random as r


def sigmoid(x):
	"""Does the mathematical operation sigmoid of param x"""
	return 1 / (1 + m.exp(-x))


class Row(object):
	"""Row object
		A collection of neurons in a row

		params:
			-> num ~ the number of the row (ordered)
			-> lenght ~ the size of the row
			-> next_row ~ links to the next row
	"""
	def __init__(self, num, length, next_row=None):
		self.num = num
		self.length = length
		self.neurons = {}
		self.linklst = []
		self.next_row = next_row

	def calc(self):
		"""Calculate funtion
		Calculates activation for each neuron in the row
		"""
		for neuron in self.neurons.items():
			neuron.calculate()

	def send(self):
		""" Send funtiion
		Sends activations to the next row
		"""
		if self.next_row:
			for neuron in self.neurons.items():
				neuron.give(self.next_row.neurons)
			print("-" * 10 + " Completed Row " + "-" * 10)
			self.next_row.calc()
			self.next_row.send()
		# Prints results
		if not self.next_row:
			max = 0
			max_val = 0
			print("-" * 10 + " Results! " + "-" * 10)
			for neuron in self.neurons.items():
				print(
					'activation of neuron ' + str(
						neuron.value
					) + " was " + str(
						neuron.activation
					)
				) 
				if neuron.activation > max_val:
					max = neuron.value
					max_val = neuron.activation
			print("the computer thinks this is: " + str(max))

	def link(self):
		"""Link Function
		Links all internal neurons to the next row's
		internal neurons
		"""
		if self.next_row:
			print(
				"Linking Row " + str(
					self.num
				) + " to " + str(
					self.next_row.num
				)
			)
			for key in self.next_row.neurons.keys():
				self.linklst.append(key)
			for key, neuron in self.neurons.items():
				neuron.linkto = self.linklst
				neuron.give(self.next_row.neurons)
			self.next_row.link()

		else:
			print("All Rows Linked")


class Start_Neuron(object):
	"""Start Neuron Object
	This is a neural network start point
	the value of this neuron is set with activation
	directly form source data.

	This is then sent to the next row of neurons

	params:
		-> id ~ numerical identifier
		-> row ~ row object
	"""
	def __init__(self, id, row):
		self.id = id
		self.row = row
		self.linkto = []
		self.activation = 0

	def give(self, objlst):
		for neuron in self.linkto:
			print(str(self.id) + " giving val to " + str(neuron))
			objlst[neuron].take(self.id, self.activation)


class End_Neuron(object):
	""" End Neuron Object
	This is the end neuron of an nueral network.
	Each neuron in the final row has its own value 
	the neuron with the highest activation is the one
	that will be selected as the answer

	params:
		-> id ~ numerical identifier
		-> row ~ row object
		-> value ~ value of neuron as answer
	"""
	def __init__(self, id, row, value):
		self.id = id
		self.value = value
		self.row = row
		self.linkfrom = []
		self.activation = 0
		self.bias = 0
		self.activations = {}
		self.weights = {}

	def scramble(self):
		"""Scrable method
		scrambles the neuron with a random value for
		each weight in weights object
		"""
		for key in self.activations.keys():
			self.weights[key] = r.randint(0, 1)

	def take(self, id, activity):
		"""Take method
		recieves id of neuron and adds activation
		to neuron's id in the self.activation dict

		params:
			-> id ~ id of neuron going in
			-> activation of neuron going in
		"""
		if id not in self.linkfrom:
			self.linkfrom.append(id)
		self.activations[id] = activity

	def calculate(self):
		'''Calculate method
		Calculates activation of neuron from the weights
		currently in self.weights

		returns:
			-> activation
		'''
		update = 0
		for key, value in self.activations.items():
			update += value * self.weights[key]
		self.activation = sigmoid(update - self.bias)
		return self.activation


class Hidden_Neuron(object):
	"""Hidden Neuron object
	This neuron is the majority of the neurons in most networks
	they populate all the rows between the first and the last
	they take inputs calculate their activation and then sends
	it over to the next row.

	params:
		-> id ~ numerical identifier
		-> row ~ row object
	"""
	def __init__(self, id, row):
		self.id = id
		self.row = row
		self.linkto = []
		self.linkfrom = []
		self.activation = 0
		self.bias = 0
		self.activations = {}
		self.weights = {}

	def scramble(self):
		"""Scrable method
		scrambles the neuron with a random value for
		each weight in weights object
		"""
		for key in self.activations.keys():
			self.weights[key] = r.randint(0, 1)

	def calculate(self):
		'''Calculate method
		Calculates activation of neuron from the weights
		currently in self.weights

		returns:
			-> activation
		'''
		update = 0
		for key, value in self.activations.items():
			update += value * self.weights[key]

		self.activation = sigmoid(update - self.bias)
		return self.activation

	def give(self, objlst):
		"""Give method
		this method calls the take method in every neuron
		that self is connected to. 

		params:
			-> objlst ~ a list of neuron objects
		"""
		for neuron in self.linkto:
			print(str(self.id) + " giving val to " + str(neuron))
			objlst[neuron].take(self.id, self.activation)

	def take(self, id, activity):
		"""Take method
		recieves id of neuron and adds activation
		to neuron's id in the self.activation dict

		params:
			-> id ~ id of neuron going in
			-> activation of neuron going in
		"""
		if id not in self.linkfrom:
			self.linkfrom.append(id)
		self.activations[id] = activity
