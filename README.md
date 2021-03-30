
# Minotaur Project 

- [Minotaur Project](#minotaur-project)
	- [To Play](#to-play)
	- [How to play](#how-to-play)

## To Play
Python dependencies: networkx, pymongo, matplotlib, pygame

```
pip install pygame networkx pymongo matplotlib 
```

To play: 

```
cd Minotaur-Project
python3 game.py
```

To change maze difficulty, edit line 6 in `game.py`.

```
maze_key = get_maze2(size = "small", difficulty = "easy")
```

Possible options are 

`size`
- `small`
- `medium`
- `large`
- `random`

`difficulty`
- `easy`
- `medium`
- `hard`
- `max`
- `random`

## How to play