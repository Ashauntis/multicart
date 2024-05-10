from fastapi import FastAPI
import scenes.quadblox.scripts.qb as qb
import random
app = FastAPI()

@app.get("/")
def read_root():
    return {"active_games": len(boards)}

@app.get("/boards/{game_id}/sit")
def seat(game_id: int):
    # check for a valid game
    if game_id >= len(boards):
        return "Invalid game id"

    # check for an open seat
    for i in range(len(boards[game_id])):
        if boards[game_id][i].dead():
            boards[game_id][i].clear()
            return {'seat': i}

@app.get("/boards")
def read_boards():
    return boards

@app.get("/boards/new")
def new_board():
    create_new_board()
    return len(boards) - 1

@app.get("/boards/{game_id}")
def read_board(game_id: int):
    board_states = []
    for board in boards[game_id]:
        board_states.append(board.export_board())
    return board_states

@app.post("/boards/update/{game_id}/{board_number}")
def update_board(game_id: int, board_number: int, board_state: str):
    # pick a random board to update
    # board = random.choice(boards[game_id])
    boards[game_id][board_number].import_board(board_state)
    

    return boards[game_id]


def create_new_board():
    new_game = []
    for _ in range(9):
        new_game.append(qb.Board())

    boards.append(new_game)

boards = []
create_new_board()
