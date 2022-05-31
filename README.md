# FoldingBlocksBot
A bot for the mobile game [Folding Blocks](https://apps.apple.com/us/app/folding-blocks/id1459650728). A puzzle for mobile devices in which the player turns over pieces of different shapes to fill the entire field.

## The goal of the game
The goal of this puzzle game is to unfold the blocks, i.e. to double them in size until there are no more empty spaces on the board.

## Bot Logic
- File [tap_start_restart.py](https://github.com/Tsarevskay/FoldingBlocksBot/blob/main/tap_start_restart.py) starts the game for the first time and then switches levels to continue the game using text recognition from the screen.
- File [finding_coordinates_and_colors.py](https://github.com/Tsarevskay/FoldingBlocksBot/blob/main/finding_coordinates_and_colors.py) uses CV to find the coordinates and color of each square in the screenshot and interprets this level as a matrix.
- File [solution_algorithm.py](https://github.com/Tsarevskay/FoldingBlocksBot/blob/main/solution_algorithm.py) finds the sequence of directions of the figures to win.
- File [swipe.py](https://github.com/Tsarevskay/FoldingBlocksBot/blob/main/swipe.py) implements a shape swipe in a given direction.
- File [consts.py](https://github.com/Tsarevskay/FoldingBlocksBot/blob/main/consts.py) contains color and direction constants.

## Getting Started
1. [Download](https://www.bluestacks.com/ru/index.html) a free emulator to run mobile applications on your computer.
2. Launch the emulator and download the **Folding Blocks** game from the **Play Store**, turn off the Internet (to play without ads), then launch the game. *Complete the first 2 training levels on your own and go to the main menu of the game.*
3. Clone the repository or download and unzip the zip file for this repository.
4. Open the terminal in the folder where the project is saved and enter the command: `$ pip install -r requirements.txt`.
5. Run the file [main.py](https://github.com/Tsarevskay/FoldingBlocksBot/blob/main/main.py) and open the emulator with the game, if you want to stop code execution, press q on the keyboard.
