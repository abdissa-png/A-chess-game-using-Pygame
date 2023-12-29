from Board import Board
from Move import Move


def minimax(board: Board,maxDepth: int,currentDepth: int,alpha: float,beta: float,isMaximizing:bool=True) -> (float, Move):
    # Check if we’re done recursing.
    if board.isGameOver() or currentDepth == maxDepth:
        return board.evaluate(), None
    # Otherwise bubble up values from below.
    bestMove: Move = None
    if isMaximizing:
        bestScore: float = -9999
    else:
        bestScore: float = 9999
    # Go through each move.
    for move in board.legalMoves:
        newBoard: Board = board.builder(move)
        # Recurse.
        currentScore, currentMove = minimax(newBoard,maxDepth, currentDepth+1,alpha,beta,not isMaximizing)
        # Update the best score.
        if isMaximizing:
            if currentScore > bestScore:
                bestScore = currentScore
                bestMove = move
            alpha=max(alpha,bestScore)
            if alpha>=beta:
                return alpha,bestMove
        else:
            if currentScore < bestScore:
                bestScore = currentScore
                bestMove = move
            beta=min(beta,bestScore)
            if beta<=alpha:
                return beta,bestMove
    return bestScore, bestMove