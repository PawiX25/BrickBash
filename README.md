# BrickBash

BrickBash is a classic "Breakout" style game developed using Python and the Pygame library. In this game, you control a paddle to bounce a ball and break bricks arranged in levels. The objective is to clear all the bricks without letting the ball fall below the paddle. The game features multiple difficulty levels, high score tracking, and an incrementally increasing ball speed for added challenge.

## Features

- **Multiple Difficulty Levels:** Choose from Easy, Medium, or Hard, each with varying ball speed, paddle speed, and brick layouts.
- **Level Progression:** Advance through multiple levels with increasing difficulty as you clear all the bricks.
- **High Score Tracking:** Save and display the top 5 high scores locally in `high_scores.txt`.
- **Pause and Resume:** Ability to pause and resume the game at any time using the `P` key.
- **Dynamic Ball Speed:** Ball speed increases as you score points and over time, making the game progressively more challenging.

## Controls

- **Left Arrow (`←`):** Move the paddle left.
- **Right Arrow (`→`):** Move the paddle right.
- **Enter (`⏎`):** Select difficulty on the menu.
- **P Key:** Pause/Resume the game.
- **R Key:** Restart the game after game over or victory.
- **Up Arrow (`↑`) / Down Arrow (`↓`):** Navigate the difficulty selection menu.

## Installation

### Requirements

- Python 3.x
- Pygame library

### Steps to Run

1. **Clone the repository:**
    ```bash
    git clone https://github.com/PawiX25/BrickBash.git
    cd BrickBash
    ```

2. **Install Pygame:**
    ```bash
    pip install pygame
    ```

3. **Run the game:**
    ```bash
    python game.py
    ```

## How to Play

1. **Select Difficulty:** Use the up and down arrow keys to navigate the menu and press Enter to select a difficulty level.
2. **Start the Game:** Once the difficulty is selected, the game will start automatically.
3. **Control the Paddle:** Use the left and right arrow keys to move the paddle and keep the ball in play.
4. **Break All Bricks:** Aim to break all bricks to advance to the next level.
5. **Avoid Losing Lives:** Don't let the ball fall below the paddle, or you'll lose a life.
6. **Pause/Resume:** Press `P` to pause the game and `P` again to resume.
7. **Game Over or Win:** If you lose all lives, the game ends. Press `R` to restart. If you clear all levels, you win!

## High Score Management

- High scores are automatically saved and loaded from `high_scores.txt`.
- The top 5 scores are displayed at the game over screen.

## Screenshots

Here’s a glimpse of BrickBash in action:

![BrickBash Screenshot](https://github.com/user-attachments/assets/a372607a-90c4-4535-be01-3820c028b00b)
