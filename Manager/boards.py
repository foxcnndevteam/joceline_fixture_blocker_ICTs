import sys
import json
import logger
import peewee
import Utils.lang as lang
import Db.Models as Models
import Manager.config as config

boards: dict[str, Models.Local.Boards] = {}

def loadBoardsInfo():
    global boards
    
    try:
        boards_messages = {
            "repeated_ids": lang.messages["boards"]["repeated_ids"]
        }
    except KeyError as e:
        logger.error(f'Corrupted lang file: Missing key "{e.args[0]}" in lang file')
        sys.exit(0)
    
    boards_ids = getBoardsList()

    if len(boards_ids) != len(set(boards_ids)):
        logger.error(boards_messages["repeated_ids"])
        sys.exit(0)
    
    for board in boards_ids:
        try:
            boards[str(board)] = Models.Local.Boards(
                board_id = board,
                board_failed = False,
                should_board_retest = False
            )
            
            boards[str(board)].save()
        except peewee.IntegrityError:
            boards[str(board)] = Models.Local.Boards().select().where(Models.Local.Boards.board_id == board).get()
                
        
# --- Getters --- #

def isOnlyOneBoard() -> bool:
    return (len(getBoardsList()) == 1)

def getBoardsMap():
    return json.loads(config.getBoardsOnFixtureMap())

def getBoardsList():
    return [board for row in getBoardsMap() for board in row]

def getBoardFailed(board_id: str):
    global boards
    
    return boards[board_id].board_failed

def getBoardsToRetest():
    boards_to_retest = []
    try:
        raw_boards = Models.Local.Boards().select().where(Models.Local.Boards.should_board_retest == True)
        for board in raw_boards:
            if board.should_board_retest:
                boards_to_retest.append(board.board_id)
                board.should_board_retest = False
                board.save()
        return boards_to_retest
    except:
        return boards_to_retest
    
def someBoardFailed():
    board: Models.Local.Boards
    boards = Models.Local.Boards().select()
    some_board_faied = False
    
    for board in boards:
        if board.board_failed:
            some_board_faied = True
            board.board_failed = False
            board.save()
    
    return some_board_faied
    
    
# --- Setters --- #

def setBoardFailed(board_id: str, board_failed: bool):
    global boards
    
    boards[board_id].board_failed = board_failed
    boards[board_id].save()

def saveBoardShouldRetest(board_id: str, should_board_retest: bool):
    global boards
    
    boards[board_id].should_board_retest = should_board_retest
    boards[board_id].save()

def restartBoardsValues():
    global boards
    
    for board_model in boards.values():
        board_model.should_board_retest = False
        board_model.save()