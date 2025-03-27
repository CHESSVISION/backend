import chess
from typing import List


def find_move_to_reach_fen(board, target_board_fen):
    """
    From the current 'board', find the single legal move that leads
    to 'target_board_fen' as a piece placement (i.e. board.board_fen()).

    Returns a chess.Move if found, or None if not found.
    """
    for move in board.generate_legal_moves():
        board.push(move)
        # Compare only piece placement (board.board_fen()).
        if board.board_fen() == target_board_fen:
            board.pop()
            return move
        board.pop()
    return None


def fill_full_fens(partial_fens):
    result = []
    for fen in partial_fens:
        result.append(f"{fen} w KQkq - 0 1")
    return result


def build_full_fens_from_partial_fens(partial_fens):
    """
    Given a list of partial FENs (piece placement only), find the
    sequence of moves from the initial board that lead to each position,
    and collect the full FEN for each position.
    """
    board = chess.Board()  # Start at the initial position
    full_fens = []

    # The first partial fen should match the initial piece placement:
    if board.board_fen() != partial_fens[0]:
        raise ValueError("The first partial FEN does not match the standard initial position.")

    # Record the initial position's full FEN
    full_fens.append(board.fen())

    # Go through all subsequent positions
    for i in range(1, len(partial_fens)):
        target_fen = partial_fens[i]
        move = find_move_to_reach_fen(board, target_fen)
        if move is None:
            raise ValueError(f"No single legal move transforms position {i - 1} into position {i}.")
        # Make that move
        board.push(move)
        # Now board is at the new position, so collect its full FEN
        full_fens.append(board.fen())

    return full_fens


def find_move(initial_fen, target_fen):
    # Create the board for the initial FEN
    board = chess.Board(initial_fen)

    # Iterate through all legal moves
    for move in board.legal_moves:
        board.push(move)  # Apply the move
        if board.fen() == target_fen:  # Compare the resulting FEN
            return move  # Found the move
        board.pop()  # Undo the move

    return None  # Return None if no move matches the target FEN


def fen_to_table(fen_position):
    rows = fen_position.split("/")
    table = [
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
    ]

    row_count = 0
    for row in rows:
        column_count = 0
        for c in row:
            if c.isdigit():
                column_count += int(c)
            else:
                table[row_count][column_count] = c
                column_count += 1
        row_count += 1

    return table


def coords_to_uci(row, col):
    """
    Convert table indices (0..7) to standard algebraic notation:
      row=0,col=0 => 'a8'
      row=7,col=7 => 'h1'
    """
    # File: 0->a, 1->b, ..., 7->h
    file_letter = chr(ord('a') + col)
    # Rank: 0->8, 1->7, ..., 7->1
    rank_number = str(8 - row)
    return file_letter + rank_number


def table_to_move(initial_table, target_table) -> str:
    """
    Compare two 8x8 tables and return a single UCI move (e.g. 'e2e4', 'e7e8q')
    if exactly one basic move was made, else return 'invalid move'.
    """
    diffs = []
    for r in range(8):
        for c in range(8):
            if initial_table[r][c] != target_table[r][c]:
                diffs.append((r, c))

    # In a simple move (without castling or en passant), we expect exactly 2 changed squares:
    #  - The 'from' square (occupied in initial, empty or different piece in target)
    #  - The 'to' square (empty in initial, occupied in target)
    if len(diffs) != 2:
        return "invalid move"

    (r1, c1), (r2, c2) = diffs

    # We have two squares that differ; figure out which is 'from' and which is 'to'
    #  One approach: the 'from' square is the one that had a piece initially but is empty/different now.
    #  The 'to' square is the one that had no piece or a different piece initially, but changed.

    piece1_initial = initial_table[r1][c1]
    piece1_target = target_table[r1][c1]
    piece2_initial = initial_table[r2][c2]
    piece2_target = target_table[r2][c2]

    # Identify from-square
    if piece1_initial != "" and piece1_target == "":
        # Square (r1,c1) lost a piece => from-square
        from_row, from_col = r1, c1
        to_row, to_col = r2, c2
    elif piece2_initial != "" and piece2_target == "":
        # Square (r2,c2) lost a piece => from-square
        from_row, from_col = r2, c2
        to_row, to_col = r1, c1
    else:
        # If neither changed from piece to empty, or we can't clearly identify from->to, treat as invalid
        return "invalid move"

    moved_piece = initial_table[from_row][from_col]
    new_piece = target_table[to_row][to_col]  # piece after moving (could be same or promotion)

    # Construct UCI move like "e2e4"
    from_uci = coords_to_uci(from_row, from_col)
    to_uci = coords_to_uci(to_row, to_col)

    # Check for promotion: a typical scenario is if a pawn 'P' or 'p' moves to the last rank and changes piece.
    #   White Pawn: from e7 -> e8, new_piece = 'Q' => e7e8q
    #   Black Pawn: from e2 -> e1, new_piece = 'q' => e2e1q
    # Very basic check:
    promotion_move = ""
    if moved_piece.lower() == 'p':
        # White pawn promotion if it lands on row=0, black pawn promotion if it lands on row=7
        if (moved_piece == 'P' and to_row == 0 and new_piece.upper() in ['Q', 'R', 'B', 'N']) or \
                (moved_piece == 'p' and to_row == 7 and new_piece.lower() in ['q', 'r', 'b', 'n']):
            # The letter appended is the *lowercase* of the new piece for UCI
            # e.g. White promotes to 'Q' => 'q' in UCI suffix
            promotion_move = new_piece.lower()

    uci_move = from_uci + to_uci + promotion_move
    return uci_move


def find_moves(fen_positions: List[str]) -> List[str]:
    moves = []
    for i in range(len(fen_positions) - 1):
        initial_fen = fen_positions[i]
        target_fen = fen_positions[i + 1]

        # Convert to tables
        initial_table = fen_to_table(initial_fen)
        target_table = fen_to_table(target_fen)

        # Derive the single UCI move
        move = table_to_move(initial_table, target_table)
        moves.append(move)

    return moves
