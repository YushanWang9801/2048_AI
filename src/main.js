var board, score = 0, rows = 4, columns = 4;

window.onload = function () {
    setGame();
    if (!hasEmptyTile()) { 
        gameOver();
    }

}


function setGame() {
    board = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ];

    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < columns; c++) {
            let tile = document.createElement("div");
            tile.id = r.toString() + "-" + c.toString();
            let num = board[r][c];
            updateTile(tile, num);
            document.getElementById("board").append(tile);
        }
    }

    setTwo();
    setTwo();
}

function updateTile(tile, num) {
    tile.innerText = "";
    tile.classList.value = "";
    tile.classList.add("tile");
    if (num > 0) {
        tile.innerText = num;
        if (num > 0) {
            tile.innerText = num;
            if (num <= 4096) {
                tile.classList.add("x" + num.toString());
            } else {
                tile.classList.add("x8192");
            }
        }
    }
}

function setTwo() {
    if (!hasEmptyTile()) {
        return;
    }
    let found = false;
    while (!found) {
        //find random row and column to place a 2 in
        let r = Math.floor(Math.random() * rows);
        let c = Math.floor(Math.random() * columns);
        if (board[r][c] == 0) {
            board[r][c] = 2;
            let tile = document.getElementById(r.toString() + "-" + c.toString());
            tile.innerText = "2";
            tile.classList.add("x2");
            found = true;
        }
    }
}

function hasEmptyTile() {
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < columns; c++) {
            if (board[r][c] == 0) {
                return true;
            }
        }
    }
    return false;
}

document.addEventListener('keyup', (e) => {
    if (e.code === "ArrowLeft") {
        slideLeft();
        setTwo();
    } else if (e.code === "ArrowRight") {
        slideRight();
        setTwo();
    } else if (e.code === "ArrowUp") {
        slideUp();
        setTwo();
    } else if (e.code === "ArrowDown") {
        slideDown();
        setTwo();
    }
    document.getElementById("score").innerText = score;
});

function filterZero(row) {
    return row.filter(num => num != 0); //create new array of all nums != 0
}

function slide(row) {
    row = filterZero(row);
    for (let i = 0; i < row.length; i++) {
        if (row[i] == row[i + 1]) {
            row[i] *= 2;
            row[i + 1] = 0;
            score += row[i];
        }
    }
    while (row.length < columns) {
        row.push(0);
    }
    return row;
}

function slideLeft() {
    for (let r = 0; r < rows; r++) {
        board[r] = slide(board[r]);
        for (let c = 0; c < columns; c++) {
            let tile = document.getElementById(r.toString() + "-" + c.toString());
            let num = board[r][c];
            updateTile(tile, num);
        }
    }
}

function slideRight() {
    for (let r = 0; r < rows; r++) {
        board[r] = slide(board[r].reverse()).reverse();
        for (let c = 0; c < columns; c++) {
            let tile = document.getElementById(r.toString() + "-" + c.toString());
            let num = board[r][c];
            updateTile(tile, num);
        }
    }
}

function slideUp() {
    for (let c = 0; c < columns; c++) {
        let column = [board[0][c], board[1][c], board[2][c], board[3][c]]
        column = slide(column)
        for (let r = 0; r < rows; r++) {
            board[r][c] = column[r];
            let tile = document.getElementById(r.toString() + "-" + c.toString());
            let num = board[r][c];
            updateTile(tile, num);
        }
    }
}

function slideDown() {
    for (let c = 0; c < columns; c++) {
        let column = [board[3][c], board[2][c], board[1][c], board[0][c]]
        column = slide(column).reverse();
        for (let r = 0; r < rows; r++) {
            board[r][c] = column[r];
            let tile = document.getElementById(r.toString() + "-" + c.toString());
            let num = board[r][c];
            updateTile(tile, num);
        }
    }
}

function gameOver() {
    console.log('WHERE THE FUCK is my key')
    const gameOverElement = document.getElementById('game-over');
    gameOverElement.classList.remove('hidden');
    document.removeEventListener('keydown', handleKeyDown);

    const restartButton = document.getElementById('restart-button');
    restartButton.addEventListener('click', restartGame);
}

function restartGame() {
    board = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ];
    score = 0;

    const gameOverElement = document.getElementById('game-over');
    gameOverElement.classList.add('hidden');
    document.addEventListener('keydown', handleKeyDown);

    setGame();
}