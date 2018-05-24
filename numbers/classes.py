import math as m
import random as r


def sigmoid(x):
    return 1 / (1 + m.exp(-x))


class Row(object):
    def __init__(self, num, length, next_row=None):
        self.num = num
        self.length = length
        self.neurons = {}
        self.linklst = []
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
            max = 0
            max_val = 0
            print("-" * 10 + " Results! " + "-" * 10)
            for key, neuron in self.neurons.items():
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
        if self.next_row:
            print(
                "Linking Row " + str(
                    self.num
                ) + " to " + str(
                    self.next_row.num
                )
            )
            for key, val in self.next_row.neurons.items():
                self.linklst.append(key)
            for key, neuron in self.neurons.items():
                neuron.linkto = self.linklst
                neuron.give(self.next_row.neurons)
            self.next_row.link()

        else:
            print("All Rows Linked")


class Start_Neuron(object):
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
        for key, val in self.activations.items():
            self.weights[key] = r.randint(0, 1)

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
        self.bias = 0
        self.activations = {}
        self.weights = {}

    def scramble(self):
        for key, val in self.activations.items():
            self.weights[key] = r.randint(0, 1)

    def calculate(self):
        update = 0
        for key, value in self.activations.items():
            update += value * self.weights[key]

        self.activation = sigmoid(update - self.bias)
        return self.activation

    def give(self, objlst):
        for neuron in self.linkto:
            print(str(self.id) + " giving val to " + str(neuron))
            objlst[neuron].take(self.id, self.activation)

    def take(self, id, activity):
        if id not in self.linkfrom:
            self.linkfrom.append(id)
        self.activations[id] = activity
