# 2048 Game with Smart AI (Vue 3)

This is a web-based implementation of the classic **2048** puzzle game, built using **Vue 3** and enhanced with a powerful **Smart AI**. The AI uses an Expectimax-based strategy and several heuristics to evaluate and play the game automatically.

![screenshot](./public/screenshot.png)

---

## 🚀 Features

- ✅ Classic 2048 gameplay with arrow key controls
- 🤖 **AI Play**: Smart AI chooses the optimal move based on board evaluation
- ⚡ **AI Flash**: Fast-paced AI mode for quickly reaching higher tiles
- 🎯 AI heuristics include:
  - Empty cell count
  - Highest tile position (favoring corners)
  - Smoothness (difference between neighboring tiles)
  - Merge potential
  - Monotonicity (increasing/decreasing sequences)

---

## 🛠 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourname/vue-2048-ai.git
cd vue-2048-ai
````

### 2. Install dependencies

```bash
npm install
```

### 3. Run the development server

```bash
npm run dev
```

Then open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 🎮 Gameplay Instructions

* Use the **arrow keys (↑ ↓ ← →)** to move the tiles.
* When two tiles with the same number touch, they merge into one.
* Try to create the `2048` tile to win!
* Click **"New Game"** to start over.
* AI Controls:

  * **AI Play**: Starts the AI in normal speed mode.
  * **AI Flash**: Runs the AI at a high speed (100ms interval).
  * **Pause/Resume**: Temporarily halt or resume the AI.
  * **Stop**: Completely stops AI and returns control to the player.

---

## 🤖 Smart AI Integration

### AI Files

The AI logic is separated into the following files:

```
src/
├── ai/
│   ├── SmartAI.js        # Expectimax-based AI with heuristic evaluation
│   ├── GridWrapper.js    # Converts Vue board state to an AI-friendly format
│   └── GameWrapper.js    # Handles movement and tile merging logic for the AI
```

### Integration Point

In `GameBoard.vue`, AI moves are selected with:

```js
const move = this.smartAiMove();
this.processMove(move);
```

The AI evaluates all four directions and chooses the one with the highest estimated score.

---

## 📁 Project Structure

```
src/
├── ai/                   # AI logic and wrappers
├── assets/               # Static assets (e.g., styles, images)
├── components/
│   └── GameBoard.vue     # Main game logic and UI
├── App.vue               # Vue root component
└── main.js               # App entry point
```

---

## 🧪 Build for Production

```bash
npm run build
```

The build output will be located in the `dist/` directory and can be deployed to any static hosting provider (e.g., Vercel, Netlify, GitHub Pages).

---

## 🧠 Future Improvements

* [ ] Add deep expectimax with adjustable depth
* [ ] Implement persistent high score saving
* [ ] Mobile gesture support
* [ ] Visual debugging overlay for AI decisions

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).
