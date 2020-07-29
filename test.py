# import random
# import matplotlib.pyplot as plt
# # import networkx as nx

# # I have 24 total objects, and I want to select 7 of them. 
# threshold = 7/24

# # I will randomly select items if random() is less than the threshold. If it is selected, I will count that item. So count can range from 0 to 24 total possible items. 
# # Values is a dict that contains the occurances of count after many iterations. I then plot values as a histrogram to see the distribution of items selected. 

# # Create values dictionary
# values = {}
# nums = list(range(0, 25))
# for num in nums:
# 	values[num] = 0

# # Select random items. The goal is to select 7, but there will be variance based on random(). 
# for n in range(10000):
# 	count = 0
# 	for i in range(24):
# 		# Random produces a random real number between [0, 1). 
# 		if random.random() < threshold:
# 			count += 1
# 	values[count] += 1

# # Generate the histogram. 
# keys = values.keys()
# values = values.values()

# plt.bar(keys, values)
# plt.show()

# # As you can see, it appears to be a normal distribution. I realized that the distribution is not normal, it is the type of distribution you get from counting events. So it can never go below zero. But at a sufficiently large n, like 7 in this case, it appears normal. 

# # My goal is to decrease the standard deviation to reduce the number of times I get count too low or too high. I want to have a distribution centered at 7 with a smaller standard deviation. 


###

import numpy as np
import matplotlib.pyplot as plt

plt.axis([0, 10, 0, 1])

for i in range(10):
	y = np.random.random()
	plt.scatter(i, y)
	plt.pause(0.05)
	text = input("Input: ")
	print(text)

# plt.show()