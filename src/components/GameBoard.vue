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
            <button v-if="isAIPlaying" @click="stopAI" class="ai-btn stop-btn">
                Stop
            </button>
            <div v-if="isAIPlaying" class="ai-status">
                AI: {{ aiPaused ? 'Paused' : 'Running' }}
                <button @click="aiPaused = !aiPaused" class="ai-btn">
                    {{ aiPaused ? 'Resume' : 'Pause' }}
                </button>
            </div>
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

            // 1. 空格数量（权重：10）
            const emptyCells = board.flat().filter(cell => cell === 0).length;
            score += emptyCells * 10;

            // 2. 最大数值位置（权重：1000）
            const maxValue = Math.max(...board.flat());
            const cornerPositions = [[3, 0], [3, 3], [0, 3], [0, 0]]; // 优先角落位置
            if (cornerPositions.some(([x, y]) => board[x][y] === maxValue)) {
                score += 1000;
            }

            // 3. 单调性评估（权重：5）
            for (let i = 0; i < 4; i++) {
                for (let j = 0; j < 3; j++) {
                    // 横向单调性
                    if (board[i][j] >= board[i][j + 1]) score += 5;
                    // 纵向单调性
                    if (board[j][i] >= board[j + 1][i]) score += 5;
                }
            }

            return score;
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
.game-container {
    max-width: 500px;
    margin: 0 auto;
    text-align: center;
    font-family: Arial, sans-serif;
    color: black;
}

.game-info {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
}

.score {
    font-size: 1.5em;
    font-weight: bold;
}

h1 {
    color: black;
}

.reset-btn {
    padding: 8px 16px;
    background-color: #8f7a66;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1em;
}

.reset-btn:hover {
    background-color: #9f8b77;
}

.game-board {
    background-color: #bbada0;
    border-radius: 6px;
    padding: 15px;
    position: relative;
    width: 445px;
    /* 固定宽度 */
    height: 445px;
    /* 固定高度，与宽度相同 */
    margin: 0 auto;
    /* 居中 */
}

.cell {
    width: 100px;
    height: 100px;
    margin-right: 15px;
    margin-bottom: 15px;
    background-color: #cdc1b4;
    border-radius: 4px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 2em;
    font-weight: bold;
    color: #776e65;
    float: left;
    /* 让单元格浮动排列 */
}

.row {
    display: block;
    /* 改为block布局 */
    clear: both;
    /* 清除浮动 */
    margin-bottom: 0;
    /* 移除底部间距 */
}

.row:last-child {
    margin-bottom: 0;
}

.cell:last-child {
    margin-right: 0;
}

.cell-2 {
    background-color: #eee4da;
}

.cell-4 {
    background-color: #ede0c8;
}

.cell-8 {
    background-color: #f2b179;
    color: white;
}

.cell-16 {
    background-color: #f59563;
    color: white;
}

.cell-32 {
    background-color: #f67c5f;
    color: white;
}

.cell-64 {
    background-color: #f65e3b;
    color: white;
}

.cell-128 {
    background-color: #edcf72;
    color: white;
    font-size: 1.8em;
}

.cell-256 {
    background-color: #edcc61;
    color: white;
    font-size: 1.8em;
}

.cell-512 {
    background-color: #edc850;
    color: white;
    font-size: 1.8em;
}

.cell-1024 {
    background-color: #edc53f;
    color: white;
    font-size: 1.5em;
}

.cell-2048 {
    background-color: #edc22e;
    color: white;
    font-size: 1.5em;
}

.cell-4096 {
    background-color: #977811;
    color: white;
    font-size: 1.5em;
}

.cell-8192 {
    background-color: #503e03;
    color: white;
    font-size: 1.5em;
}

.cell-16384 {
    background-color: #c3761e;
    color: white;
    font-size: 1.5em;
}

.game-over {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(238, 228, 218, 0.73);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-radius: 6px;
}

.game-over h2 {
    font-size: 2em;
    color: #776e65;
    margin-bottom: 20px;
}

.game-rules {
    background-color: #faf8ef;
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 15px;
    font-size: 0.9em;
    color: #776e65;
}

.scores {
    display: flex;
    gap: 15px;
}

.score,
.high-score {
    background-color: #bbada0;
    color: white;
    padding: 5px 10px;
    border-radius: 3px;
    font-weight: bold;
}

.ai-controls {
    margin: 15px 0;
    padding: 10px;
    background-color: #faf8ef;
    border-radius: 6px;
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
}

.ai-btn {
    padding: 8px 15px;
    background-color: #8f7a66;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9em;
    transition: background-color 0.3s;
}

.ai-btn:hover {
    background-color: #9f8b77;
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
    font-size: 0.9em;
    color: #776e65;
}
</style>