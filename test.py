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


# # ###

# # import numpy as np
# # import matplotlib.pyplot as plt

# # plt.axis([0, 10, 0, 1])

# # for i in range(10):
# # 	y = np.random.random()
# # 	plt.scatter(i, y)
# # 	plt.pause(0.05)
# # 	text = input("Input: ")
# # 	print(text)

# # # # plt.show()
# import time
# for i in range(1000):
# 	time.sleep(0.01)
# 	print("Time is {}".format(i), end='\r')

# import file_io

# d = file_io.read_dict_from_file("mazes/test_set.txt")
# new_dict = {}

# for kv_pair in sorted(d.items(), reverse = True):
# 	key = kv_pair[0]
# 	value = kv_pair[1]
# 	if key >= 30:
# 		new_dict[key] = value

# file_io.write_dict_to_file(new_dict, "mazes/new_test_set.txt")

import sys, pygame
pygame.init()

size = width, height = 320, 240
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("intro_ball.gif")
ballrect = ball.get_rect()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()