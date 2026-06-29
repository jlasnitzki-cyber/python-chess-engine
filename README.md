# ♟️ Python Chess Engine

A chess engine built entirely from scratch in Python featuring a custom search algorithm, move generation, evaluation function, opening book, and graphical interface.

This project began as a way to explore algorithms and has evolved into a fully playable chess engine capable of searching thousands of positions to determine the strongest move.

---

## Engineering Challenges

Some of the most challenging parts of the project included:

- Correctly implementing every special chess rule especially enpassant
- Optimising the search algorithm to increase depth without scarificing time performance
- Designing an undo system for recursive search

Building the engine provided practical experience with algorithm design, debugging complex state-based systems and performance optimisation.

## Features

### Chess Gameplay

- Complete implementation of all standard chess rules
- Legal move generation for every piece
- Castling
- En passant
- Pawn promotion
- Check, checkmate and stalemate detection
- Move history and undo functionality
- Algebraic move notation

### Chess Engine

The AI searches future positions using:

- Minimax search
- Alpha-Beta pruning
- Iterative Deepening
- Move Ordering
- Opening Book

These techniques allow the engine to search significantly deeper while reducing unnecessary calculations.

### Evaluation

The engine evaluates positions using a combination of:

- Material count
- Piece-square tables
- King safety
- Mobility
- Positional advantages

---

## GUI

- Interactive chess board
- Drag-and-drop piece movement *(or click-to-move if applicable)*
- Highlighting of legal moves
- AI vs Human gameplay
- Move animations *(if implemented)*
- Game over detection

---

## Search Optimisations

The engine includes several techniques commonly used in modern chess engines.

- Alpha-Beta Pruning
- Iterative Deepening
- Move Ordering
- Opening Book

These dramatically reduce the number of positions that need to be searched while allowing deeper searches within the same amount of time.

---

## Project Structure

```
python-chess-engine/

├── main.py          # Main game loop and input handling
├── config.py        # Constants, piece-square tables, opening book
├── state.py         # Board state, move history and undo system
├── moves.py         # Legal move generation and game rules
├── engine.py        # Evaluation, search and AI
├── notation.py      # Algebraic notation and move logging
├── ui.py            # Rendering and interface
│
├── images/
│
├── README.md
├── requirements.txt
├── LICENSE
└── .gitignore
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/YourUsername/python-chess-engine.git
```

Install the required packages

```bash
cd python-chess-engine
pip install -r requirements.txt
```

Run the program

```bash
python chess.py
```

---

## How the Engine Thinks

When it is the engine's turn to move, it follows this pipeline:

```
Current Position
        │
        ▼
Generate Legal Moves
        │
        ▼
Order Moves
        │
        ▼
Alpha-Beta Search
        │
        ▼
Evaluate Leaf Positions
        │
        ▼
Return Best Move
```

Each move is searched several moves into the future, with Alpha-Beta pruning eliminating branches that cannot improve the final result.

---

## Future Improvements

Planned features include:

- Transposition Tables
- Zobrist Hashing
- Quiescence Search
- Killer Move Heuristic
- History Heuristic
- Principal Variation Search
- UCI Support
- NNUE Evaluation
- Multiplayer
- Adjustable difficulty
- Engine analysis mode

---

## Lessons Learned

Developing this engine provided practical experience with:

- Object-Oriented Programming
- Search Algorithms
- Data Structures
- Algorithm Optimisation
- Game Programming
- Artificial Intelligence
- Software Architecture
- Debugging large Python projects

---

## Technologies Used

- Python
- Pygame
- Git
- GitHub

---

## Author

Developed by **Jake Lasnitzki**

First Year Engineering & Science Student
