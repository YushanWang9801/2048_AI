<template>
    <div class="game-container">
        <h1>2048 Game</h1>

        <div class="game-info">
            <div class="score">Score: {{ score }}</div>
            <button @click="resetGame" class="reset-btn">New Game</button>
        </div>

        <div class="ai-controls">
            <button @click="toggleAIPlay('normal')" class="ai-btn">
                {{ isAIPlaying && aiMode === 'normal' ? 'Pause AI' : 'AI Play' }}
            </button>
            <button @click="toggleAIPlay('flash')" class="ai-btn">
                {{ isAIPlaying && aiMode === 'flash' ? 'Pause Flash' : 'AI Flash' }}
            </button>
        </div>
        <div class="game-board">
            <div v-for="(row, rowIndex) in board" :key="rowIndex" class="row">
                <div v-for="(cell, colIndex) in row" :key="colIndex" class="cell" :class="`cell-${cell || ''}`">
                    {{ cell || '' }}
                </div>
            </div>
        </div>

        <div class="game-rules">
            <p>使用键盘方向键 ↑ ↓ ← → 移动方块</p>
            <p>相同数字的方块碰撞后会合并</p>
            <p>目标是得到 2048 方块！</p>
        </div>

        <div v-if="gameOver" class="game-over">
            <h2>Game Over!</h2>
            <button @click="resetGame" class="reset-btn">Try Again</button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'GameBoard',
    data() {
        return {
            board: Array(4).fill().map(() => Array(4).fill(0)),
            score: 0,
            gameOver: false,
            isAIPlaying: false,
            aiMode: 'normal',
            aiPaused: false,
            aiInterval: null,
            aiSteps: 0
        }
    },
    mounted() {
        this.resetGame()
        window.addEventListener('keydown', this.handleKeyDown)
    },
    beforeUnmount() {
        this.stopAI()
        window.removeEventListener('keydown', this.handleKeyDown)
    },
    methods: {
        resetGame() {
            this.board = Array(4).fill().map(() => Array(4).fill(0))
            this.score = 0
            this.gameOver = false
            this.addRandomTile()
            this.addRandomTile()
        },
        addRandomTile() {
            const emptyCells = []
            for (let i = 0; i < 4; i++) {
                for (let j = 0; j < 4; j++) {
                    if (this.board[i][j] === 0) {
                        emptyCells.push({ i, j })
                    }
                }
            }

            if (emptyCells.length > 0) {
                const { i, j } = emptyCells[Math.floor(Math.random() * emptyCells.length)]
                this.board[i][j] = Math.random() < 0.9 ? 2 : 4
            }
        },
        handleKeyDown(e) {
            // 区分真实事件和AI模拟事件
            const isRealEvent = e instanceof Event;
            const key = isRealEvent ? e.key : e;

            // 仅对真实事件阻止默认行为
            if (isRealEvent && ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(key)) {
                e.preventDefault();
            }

            // 使用统一按键处理逻辑
            this.processMove(key);
        },
        processMove(direction) {
            if (this.gameOver) return;

            let moved = false;
            const oldBoard = JSON.parse(JSON.stringify(this.board));

            switch (direction) {
                case 'ArrowUp': moved = this.moveUp(); break;
                case 'ArrowDown': moved = this.moveDown(); break;
                case 'ArrowLeft': moved = this.moveLeft(); break;
                case 'ArrowRight': moved = this.moveRight(); break;
                default: return;
            }

            if (moved) {
                this.addRandomTile();
                if (this.isGameOver()) this.gameOver = true;
            }
        },
        moveUp() {
            let moved = false
            for (let j = 0; j < 4; j++) {
                const column = [this.board[0][j], this.board[1][j], this.board[2][j], this.board[3][j]]
                const { newColumn, score } = this.moveAndMerge(column)
                this.score += score
                for (let i = 0; i < 4; i++) {
                    if (this.board[i][j] !== newColumn[i]) {
                        moved = true
                        this.board[i][j] = newColumn[i]
                    }
                }
            }
            return moved
        },
        moveDown() {
            let moved = false
            for (let j = 0; j < 4; j++) {
                const column = [this.board[0][j], this.board[1][j], this.board[2][j], this.board[3][j]]
                const { newColumn, score } = this.moveAndMerge(column.reverse())
                this.score += score
                const reversedColumn = newColumn.reverse()
                for (let i = 0; i < 4; i++) {
                    if (this.board[i][j] !== reversedColumn[i]) {
                        moved = true
                        this.board[i][j] = reversedColumn[i]
                    }
                }
            }
            return moved
        },
        moveLeft() {
            let moved = false
            for (let i = 0; i < 4; i++) {
                const row = [...this.board[i]]
                const { newColumn: newRow, score } = this.moveAndMerge(row)
                this.score += score
                if (JSON.stringify(this.board[i]) !== JSON.stringify(newRow)) {
                    moved = true
                    this.board[i] = newRow
                }
            }
            return moved
        },
        moveRight() {
            let moved = false
            for (let i = 0; i < 4; i++) {
                const row = [...this.board[i]]
                const { newColumn: newRow, score } = this.moveAndMerge(row.reverse())
                this.score += score
                const reversedRow = newRow.reverse()
                if (JSON.stringify(this.board[i]) !== JSON.stringify(reversedRow)) {
                    moved = true
                    this.board[i] = reversedRow
                }
            }
            return moved
        },
        moveAndMerge(line) {
            let newLine = line.filter(cell => cell !== 0)
            let score = 0

            for (let i = 0; i < newLine.length - 1; i++) {
                if (newLine[i] === newLine[i + 1]) {
                    newLine[i] *= 2
                    score += newLine[i]
                    newLine.splice(i + 1, 1)
                }
            }

            while (newLine.length < 4) {
                newLine.push(0)
            }

            return { newColumn: newLine, score }
        },
        isGameOver() {
            // Check if there are empty cells
            for (let i = 0; i < 4; i++) {
                for (let j = 0; j < 4; j++) {
                    if (this.board[i][j] === 0) {
                        return false
                    }
                }
            }

            // Check if any possible merges
            for (let i = 0; i < 4; i++) {
                for (let j = 0; j < 4; j++) {
                    if (j < 3 && this.board[i][j] === this.board[i][j + 1]) {
                        return false
                    }
                    if (i < 3 && this.board[i][j] === this.board[i + 1][j]) {
                        return false
                    }
                }
            }

            return true
        },
        aiMove() {
            let bestScore = -Infinity;
            let bestMove = null;
            const moves = ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'];

            // 评估每个移动方向的得分
            moves.forEach(move => {
                const testBoard = JSON.parse(JSON.stringify(this.board));
                let moved = false;

                // 模拟移动
                switch (move) {
                    case 'ArrowUp': moved = this.simulateMoveUp(testBoard); break;
                    case 'ArrowDown': moved = this.simulateMoveDown(testBoard); break;
                    case 'ArrowLeft': moved = this.simulateMoveLeft(testBoard); break;
                    case 'ArrowRight': moved = this.simulateMoveRight(testBoard); break;
                }

                if (moved) {
                    const score = this.evaluateBoard(testBoard);
                    if (score > bestScore) {
                        bestScore = score;
                        bestMove = move;
                    }
                }
            });

            return bestMove;
        },
        evaluateBoard(board) {
            let score = 0;

            const flat = board.flat();
            const emptyCells = flat.filter(cell => cell === 0).length;
            const maxValue = Math.max(...flat);

            const cornerPositions = [[3, 0], [3, 3], [0, 3], [0, 0]];
            const maxInCorner = cornerPositions.some(([x, y]) => board[x][y] === maxValue);

            // 新策略组合加权
            score += emptyCells * 100; // 提高空格的权重
            score += maxInCorner ? 1000 : 0;
            score += this.evaluateSmoothness(board) * 10;
            score += this.evaluateMergingPotential(board);
            score += this.evaluateMonotonicity(board) * 5;

            return score;
        },
        evaluateMonotonicity(board) {
            let monoScore = 0;
            for (let i = 0; i < 4; i++) {
                let row = board[i];
                let inc = 0, dec = 0;
                for (let j = 0; j < 3; j++) {
                    if (row[j] > row[j + 1]) dec += row[j] - row[j + 1];
                    else inc += row[j + 1] - row[j];
                }
                monoScore += Math.max(inc, dec);
            }

            for (let j = 0; j < 4; j++) {
                let col = [board[0][j], board[1][j], board[2][j], board[3][j]];
                let inc = 0, dec = 0;
                for (let i = 0; i < 3; i++) {
                    if (col[i] > col[i + 1]) dec += col[i] - col[i + 1];
                    else inc += col[i + 1] - col[i];
                }
                monoScore += Math.max(inc, dec);
            }

            return -monoScore;
        },
        evaluateMergingPotential(board) {
            let merges = 0;
            for (let i = 0; i < 4; i++) {
                for (let j = 0; j < 3; j++) {
                    if (board[i][j] && board[i][j] === board[i][j + 1]) merges++;
                    if (board[j][i] && board[j][i] === board[j + 1][i]) merges++;
                }
            }
            return merges * 50; // 权重可调
        },
        evaluateSmoothness(board) {
            let smoothness = 0;
            for (let i = 0; i < 4; i++) {
                for (let j = 0; j < 3; j++) {
                    const current = board[i][j];
                    const right = board[i][j + 1];
                    const down = board[j][i];
                    const below = board[j + 1] ? board[j + 1][i] : 0;

                    if (current && right) {
                        smoothness -= Math.abs(Math.log2(current) - Math.log2(right));
                    }
                    if (down && below) {
                        smoothness -= Math.abs(Math.log2(down) - Math.log2(below));
                    }
                }
            }
            return smoothness;
        },
        simulateMoveUp(board) {
            let moved = false;
            for (let j = 0; j < 4; j++) {
                const column = [board[0][j], board[1][j], board[2][j], board[3][j]];
                const { newColumn } = this.moveAndMerge(column);
                for (let i = 0; i < 4; i++) {
                    if (board[i][j] !== newColumn[i]) {
                        moved = true;
                        board[i][j] = newColumn[i];
                    }
                }
            }
            return moved;
        },
        simulateMoveDown(board) {
            let moved = false;
            for (let j = 0; j < 4; j++) {
                const column = [board[0][j], board[1][j], board[2][j], board[3][j]];
                const { newColumn } = this.moveAndMerge(column.reverse());
                const reversedColumn = newColumn.reverse();
                for (let i = 0; i < 4; i++) {
                    if (board[i][j] !== reversedColumn[i]) {
                        moved = true;
                        board[i][j] = reversedColumn[i];
                    }
                }
            }
            return moved;
        },
        simulateMoveLeft(board) {
            let moved = false;
            for (let i = 0; i < 4; i++) {
                const row = [...board[i]];
                const { newColumn: newRow } = this.moveAndMerge(row);
                if (JSON.stringify(board[i]) !== JSON.stringify(newRow)) {
                    moved = true;
                    board[i] = newRow;
                }
            }
            return moved;
        },
        simulateMoveRight(board) {
            let moved = false;
            for (let i = 0; i < 4; i++) {
                const row = [...board[i]];
                const { newColumn: newRow } = this.moveAndMerge(row.reverse());
                const reversedRow = newRow.reverse();
                if (JSON.stringify(board[i]) !== JSON.stringify(reversedRow)) {
                    moved = true;
                    board[i] = reversedRow;
                }
            }
            return moved;
        },
        startAI() {
            this.aiInterval = setInterval(() => {
                if (this.aiPaused || this.gameOver) return;

                const move = this.aiMove();
                console.log(`AI选择移动方向: ${move}`);

                if (move) {
                    // 直接传递方向而非模拟事件对象
                    this.processMove(move);

                    // 检查2048目标
                    if (this.aiMode === 'flash' && Math.max(...this.board.flat()) >= 2048) {
                        this.aiPaused = true;
                    }
                } else {
                    this.stopAI();
                }
            }, this.aiMode === 'flash' ? 100 : 500);
        },
        toggleAIPlay(mode) {
            console.log(`切换AI模式: ${mode}`);
            if (this.isAIPlaying && this.aiMode === mode) {
                this.aiPaused = !this.aiPaused;
                console.log(`AI ${this.aiPaused ? '暂停' : '继续'}`);
            } else {
                this.stopAI();
                this.aiMode = mode;
                this.isAIPlaying = true;
                this.aiPaused = false;
                this.startAI();
            }
        },
        stopAI() {
            console.log('停止AI');
            clearInterval(this.aiInterval);
            this.isAIPlaying = false;
            this.aiPaused = false;
            this.aiSteps = 0;
        }
    }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Arial', sans-serif;
}

body {
  background-color: #faf8ef;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
}

/* 主游戏容器 */
.game-container {
  width: 90%;
  max-width: 500px;
  margin: 0 auto;
  text-align: center;
}

/* 标题样式 */
h1 {
  color: #776e65;
  font-size: calc(2rem + 1.5vw);
  margin-bottom: 20px;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

/* 游戏信息栏（分数+按钮） */
.game-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  gap: 15px;
  flex-wrap: wrap;
}

.score {
  background-color: #bbada0;
  color: white;
  padding: 10px 20px;
  border-radius: 6px;
  font-size: calc(1.2rem + 0.5vw);
  font-weight: bold;
  min-width: 120px;
}

.reset-btn, .ai-btn {
  padding: 10px 20px;
  background-color: #8f7a66;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.3s;
  font-size: 1rem;
}
.reset-btn:hover, .ai-btn:hover {
  background-color: #9f8b77;
}

/* AI控制区域 */
.ai-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  margin: 20px 0;
  padding: 15px;
  background-color: rgba(185, 173, 161, 0.2);
  border-radius: 8px;
}

.stop-btn {
  background-color: #d9534f;
}
.stop-btn:hover {
  background-color: #c9302c;
}

.ai-status {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.9rem;
  color: #776e65;
}

/* 游戏棋盘 */
.game-board {
  background-color: #bbada0;
  border-radius: 6px;
  padding: 10px;
  width: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.row {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.cell {
  width: calc(25% - 10px);
  max-width: 100px;
  height: calc(25vw - 30px);
  max-height: 100px;
  flex-shrink: 0; /* 防止单元格收缩 */
  background-color: #cdc1b4;
  border-radius: 4px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: calc(1.5rem + 1.5vw);
  font-weight: bold;
  transition: transform 0.1s, background 0.3s;
}

/* 数字瓷砖颜色 */
.cell-2 { background-color: #eee4da; color: #776e65; }
.cell-4 { background-color: #ede0c8; color: #776e65; }
.cell-8 { background-color: #f2b179; color: white; }
.cell-16 { background-color: #f59563; color: white; }
.cell-32 { background-color: #f67c5f; color: white; }
.cell-64 { background-color: #f65e3b; color: white; }
.cell-128 { background-color: #edcf72; color: white; font-size: calc(1.2rem + 1.5vw); }
.cell-256 { background-color: #edcc61; color: white; font-size: calc(1.2rem + 1.5vw); }
.cell-512 { background-color: #edc850; color: white; font-size: calc(1.2rem + 1.5vw); }
.cell-1024 { background-color: #edc53f; color: white; font-size: calc(1rem + 1.5vw); }
.cell-2048 { background-color: #edc22e; color: white; font-size: calc(1rem + 1.5vw); }
.cell-4096 { background-color: #977811; color: white; font-size: calc(1rem + 1.5vw); }

/* 游戏规则说明 */
.game-rules {
  background-color: rgba(185, 173, 161, 0.2);
  padding: 15px;
  border-radius: 6px;
  font-size: 0.9rem;
  color: #776e65;
  line-height: 1.6;
  margin-bottom: 20px;
}

/* 游戏结束弹窗 */
.game-over {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(238, 228, 218, 0.85);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: 6px;
  z-index: 10;
}
.game-over h2 {
  font-size: 2.5rem;
  color: #776e65;
  margin-bottom: 20px;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .game-board {
    gap: 8px;
    padding: 8px;
  }
  .row { gap: 8px; }
  .cell { height: calc(23vw - 25px); }

  .cell {
    font-size: calc(1.2rem + 1.5vw);
  }
}

@media (max-width: 480px) {
  .game-info {
    flex-direction: column;
  }
  .ai-controls {
    flex-direction: column;
    align-items: center;
  }
  .cell {
    font-size: calc(1rem + 1.5vw);
  }
  .row { gap: 6px; }
  .cell { 
    height: calc(21vw - 20px);
    font-size: calc(1rem + 1.5vw);
  }
}
</style>