
# Chess Engine (Minimax + Alpha-Beta Pruning)

A chess engine written in Python from scratch — full board representation, legal move generation (including check detection), and move selection via the minimax algorithm with alpha-beta pruning. The board is rendered directly in the terminal using ANSI escape codes for colored squares and Unicode chess piece symbols, with no external chess or GUI library used.

Currently runs in **engine-vs-engine mode** and **player-vs-engine mode**: both sides are played by the search algorithm, so you can watch two versions of the same engine play a full game against each other move by move in the terminal or go against the engine by playing as white.

## Features

- Full board representation using a flat 64-square array (`0`–`63`, `a1` = index `0`)
- Custom legal move generation for every piece type (pawn, knight, bishop, rook, queen, king), including two-square pawn advances and diagonal captures
- Check detection (`isKingChecked`) and legality filtering (`isMoveLegal`) so illegal "move into check" options are excluded
- Game-end detection for checkmate and stalemate (`CheckGameStatus`)
- Minimax search with alpha-beta pruning (`Maximizing`) for efficient move evaluation
- Custom material-based evaluation function (`EvaluatePoints`)
- Tie-breaking among equally-scored best moves via random selection, so the engine doesn't play identically every game
- Colored terminal board rendering with Unicode piece glyphs (♜ ♞ ♝ ♛ ♚ ♟, etc.) via ANSI escape codes — no GUI dependencies

## How It Works

### Board representation
The board is a single flat list of 64 integers rather than an 8x8 grid. Each square holds a signed integer: positive values are white pieces, negative are black, and `0` is empty (`1`=Rook, `2`=Knight, `3`=Bishop, `4`=Queen, `5`=King, `6`=Pawn). Index `i` maps to rank `i // 8` and file `i % 8`.

### Move generation and legality
Each piece type has its own move-validation function (`isValidPawnMove`, `isValidKnightMove`, etc.), dispatched through `FunctionMapId`. `GenerateAllMoves` produces every pseudo-legal move for a color; `GetLegalMoves` then filters out any move that would leave that side's own king in check, using a make-move / check-detect / unmake-move pattern (`isMoveLegal`).

### Search: minimax with alpha-beta pruning
`Maximizing` recursively searches the game tree to a fixed depth, alternating between maximizing White's score and minimizing Black's score. **Alpha-beta pruning** cuts off branches that can't influence the final decision, meaning the engine explores far fewer positions than plain minimax would while still arriving at the same result. `FindBestMove` drives the top-level search, and where multiple moves tie for the best score, one is chosen at random from among them (`best_moves`) so games don't play out identically every time.

### Evaluation function
At the search's depth limit, `EvaluatePoints` scores the position purely by material, using custom weights defined in `Price_Values` (Rook = 10, Knight = 8, Bishop = 6, Queen = 20, King = 999, Pawn = 2) — summed for White and subtracted for Black. This is a fixed, hand-crafted heuristic rather than a learned one — see "Future Improvements" below.

## Demo
<img width="291" height="585" alt="TerminalExecution1" src="https://github.com/user-attachments/assets/b018e9bd-e66e-4e16-8a91-18033840012d" />
<img width="296" height="610" alt="TerminalExecution3" src="https://github.com/user-attachments/assets/8caef72d-90db-459a-8d85-1c192051b956" />
<img width="296" height="594" alt="TerminalExecution2" src="https://github.com/user-attachments/assets/e3eb1724-00fb-4aff-8d00-536268bb13b2" />

<!-- Add a screenshot or short terminal recording (e.g. a GIF via terminalizer/asciinema) of the colored board mid-game here — this is the single highest-impact addition for a terminal-only project, since it's the first thing a visitor sees. -->

## Getting Started

### Prerequisites
- Python 3.x (no external dependencies — uses only the standard library: `time`, `random`)

### Installation and Running

```bash
git clone https://github.com/nightmaretethered/chess-engine-minimax.git
cd chess-engine-minimax
python main.py
```

The engine will immediately begin playing itself, printing the board and each side's move in the terminal, with a short delay (`time.sleep(1)`) between moves so the game is watchable in real time. It stops automatically on checkmate or stalemate.

### Game modes
On startup, choose:
- **1** — AI vs AI (watch the engine play itself)
- **2** — Player vs AI (play against the engine yourself)

## Project Structure

```
chess-engine-minimax/
└── main.py    # Board representation, move generation/legality, minimax + alpha-beta search, evaluation, terminal rendering, and game loop
```

## Future Improvements

- Re-enable and polish the player-input mode for interactive play against the engine
- Replace the fixed material evaluation weights with a learned evaluation — e.g. training on self-play game outcomes to adjust piece values or move-scoring, moving from a hand-crafted heuristic toward a genuinely learned one
- Add move ordering (e.g. MVV-LVA, killer moves) to improve alpha-beta pruning efficiency at higher search depths
- Add remaining special moves: castling, en passant, and pawn promotion
- Add positional evaluation terms (piece-square tables) alongside material, since the current evaluation only considers material count
- Build a simple web interface (React frontend + API backend) as an alternative to the terminal UI

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Author
nightmaretethered
[nightmaretethered](https://github.com/nightmaretethered)
