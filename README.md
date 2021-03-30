
# Minotaur Project 

- [Minotaur Project](#minotaur-project)
	- [To Play](#to-play)
	- [About The Game](#about-the-game)
		- [A Brief Overview](#a-brief-overview)
		- [Game Details](#game-details)
	- [Game Controls](#game-controls)

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

## About The Game

### A Brief Overview
[Theseus and the Minotaur](https://en.wikipedia.org/wiki/Theseus_and_the_Minotaur) is a logic maze puzzle game invented by Robert Abbott in 1990. The player controls [Theseus](https://en.wikipedia.org/wiki/Theseus), who is trying to escape a labyrinth while avoiding the [Minotaur](https://en.wikipedia.org/wiki/Minotaur). For every move that Theseus makes, the strong and powerful Minotaur is able to make two. The only way for Theseus to escape is to outwit the Minotaur by using the layout of the maze to his advantage and by predicting the Minotaur's moves. 

### Game Details
Theseus, the player, is represented by a blue circle. The Minotaur is represented by a red circle. To escape the labyrinth, you must reach the goal, represented by a green circle, before the Minotaur catches you. 

At each turn, the player can choose to move up, down, left, right, or skip their turn. However, the Minotaur gets twice as many turns as the player. While the Minotaur is faster than the player, his moves are predicable and sometimes inefficient. The Minotaur's moves are always determined by a set of rules. 

- The Minotaur will always try to move closer to the player. He will never move to a tile further away from Theseus. 
- The Minotaur will always try to move horizontally before moving vertically. If the Minotaur is unable to move horizontally, either because a wall is blocking his path, or doing so would move him further away from Theseus, then he will try to move vertically. 
- If the Minotaur is unable to move closer to Theseus following these rules, then he will skip his turn. 

By exploiting the Minotaur's movements, the player can get the Minotaur stuck against the wall, and successfully escape. 

## Game Controls 
Use the arrow keys or WASD to move. 

| Control    | Action     |
|------------|------------|
| `↑` or `W` | Move Up    |
| `↓` or `S` | Move Down  |
| `←` or `A` | Move Left  |
| `→` or `D` | Move Right |
| `Space`    | Skip Turn  |
|            |            |