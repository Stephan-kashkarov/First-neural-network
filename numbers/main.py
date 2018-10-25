from classes import (
	Start_Neuron,
	Hidden_Neuron,
	End_Neuron,
	Row
)
from mnist import MNIST
import random as r

mndata = MNIST('data')
images, labels = mndata.load_training()

neuron_id = 0
value_of_neuron = 0
end_row = Row(3, 10)
hidden_row_2 = Row(2, 16, end_row)
hidden_row_1 = Row(1, 16, hidden_row_2)
init_row = Row(0, 784, hidden_row_1)

network = [init_row, hidden_row_1, hidden_row_2, end_row]

print("-" * 10 + " Initializing Network " + "-" * 10)
while True:
	if neuron_id < 784:
		rowid = 0
		print("adding neuron no." + str(neuron_id) + " to inital row")
		init_row.neurons[neuron_id] = Start_Neuron(neuron_id, rowid)
	elif neuron_id < 784 + 16:
		rowid = 1
		print("adding neuron no." + str(neuron_id) + " to hidden row 1")
		hidden_row_1.neurons[neuron_id] = Hidden_Neuron(neuron_id, rowid)
	elif neuron_id < 784 + 16 + 16:
		rowid = 2
		print("adding neuron no." + str(neuron_id) + " to hidden row 2")
		hidden_row_2.neurons[neuron_id] = Hidden_Neuron(neuron_id, rowid)
	elif neuron_id < 784 + 16 + 16 + 10:
		rowid = 3
		print("adding neuron no." + str(neuron_id) + " to final row")
		end_row.neurons[neuron_id] = End_Neuron(
			neuron_id, rowid, value_of_neuron
		)
		value_of_neuron += 1
	else:
		break
	neuron_id += 1

print("-" * 10 + " Linking rows " + "-" * 10)
network[0].link()

print("-" * 10 + " Initializing Weights " + "-" * 10)
for row in network:
	if row != network[0]:
		print("randomising neuron in row" + str(row))
		for key, neuron in row.neurons.items():
			print("scrambling neuron no." + str(key))
			neuron.scramble()


print("-" * 10 + " Initializing Initial Activations " + "-" * 10)
index = r.randrange(0, len(images))
for key, neuron in init_row.neurons.items():
	neuron.activation = images[index][key]
	print(
		str(
			neuron.id
		) + " was updated with: " + str(images[index][key])
	)

print("-" * 10 + " Running network " + "-" * 10)
init_row.send()
print("The actual value is: " + str(labels[index]))


loop = input("\nWhat now? (run/scramble/quit/img/next): ")
while True:
	if loop == "run":
		init_row.send()
		print("The actual value is: " + str(labels[index]))
	elif loop == "img":
		print(mndata.display(images[index]))
	elif loop == "scramble":
		print("-" * 10 + " Initializing Weights " + "-" * 10)
		for row in network:
			if row != network[0]:
				print("randomising neuron in row" + str(row))
				for key, neuron in row.neurons.items():
					print("scrambling neuron no." + str(key))
					neuron.scramble()
	elif loop == "next":
		print("-" * 10 + " Initializing Image " + "-" * 10)
		index = r.randrange(0, len(images))
		for key, neuron in init_row.neurons.items():
			neuron.activation = images[index][key]
			print(
				str(
					neuron.id
				) + " was updated with: " + str(
					images[index][key]
				)
			)
	elif loop == "quit":
		quit()
	else:
		print("Please choose a valid option")
	loop = input("\nWhat now? (run/scramble/quit/img/next): ")
