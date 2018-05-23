import math as m
import random as r


def sigmoid(x):
    return 1 / (1 + m.exp(-x))


class Row(object):
    def __init__(self, num, length, next_row=None):
        self.num = num
        self.length = length
        self.neurons = {}
        self.next_row = next_row

    def calc(self):
        for key, neuron in self.neurons.items():
            neuron.calculate()

    def send(self):
        if self.next_row:
            for key, neuron in self.neurons.items():
                neuron.give(self.next_row.neurons)
            print("-" * 10 + " Completed Row " + "-" * 10)
            self.next_row.calc()
            self.next_row.send()
        if not self.next_row:
            print("-" * 10 + " Results! " + "-" * 10)
            for key, neuron in self.neurons.items():
                print(
                    'activation of neuron ' + str(
                        neuron.value
                    ) + " was " + str(
                        neuron.activation
                    )
                )


class Start_Neuron(object):
    def __init__(self, id, row):
        self.id = id
        self.row = row
        self.linkto = []
        self.activation = 0

    def give(self, objlst):
        for neuron in self.linkto:
            objlst[neuron].take(self.id, self.activation)


class End_Neuron(object):
    def __init__(self, id, row, value):
        self.id = id
        self.value = value
        self.row = row
        self.linkfrom = []
        self.activation = 0
        self.bias = -1
        self.activations = {}
        self.weights = {}

    def scramble(self):
        for key in self.activations.items():
            self.weights[key] = r.randint(-1, 1)

    def take(self, id, activity):
        if id not in self.linkfrom:
            self.linkfrom.append(id)
        self.activations[id] = activity

    def calculate(self):
        update = 0
        for key, value in self.activations.items():
            update += value * self.weights[key]
        self.activation = sigmoid(update - self.bias)
        return self.activation


class Hidden_Neuron(object):
    def __init__(self, id, row):
        self.id = id
        self.row = row
        self.linkto = []
        self.linkfrom = []
        self.activation = 0
        self.bias = -1
        self.activations = {}
        self.weights = {}

    def scramble(self):
        for key in self.activations.items():
            self.weights[key] = r.randint(-1, 1)

    def calculate(self):
        update = 0
        for key, value in self.activations.items():
            update += value * self.weights[key]
        self.activation = sigmoid(update - self.bias)
        return self.activation

    def give(self, nxt_row):
        for neuron in self.linkto:
            objlst[neuron].take(self.id, self.activation)

    def take(self, id, activity):
        if id not in self.linkfrom:
            self.linkfrom.append(id)
        self.activations[id] = activity
