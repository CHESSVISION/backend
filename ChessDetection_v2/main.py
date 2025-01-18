from enum import Enum
from ChessBoardDetector import ChessBoardDetector
import cv2
from ChessPieceDetector import ChessPieceDetector


# pre-requirements
# the board how to be recorded from the right side

class Type(Enum):
    FRAME = "frame"


def adjust_angle(frame) -> Type.FRAME:
    pass


def process_color(frame) -> Type.FRAME:
    pass


def adjust_board(frame) -> Type.FRAME:
    pass


def detect_pieces(frame) -> list:
    pass


def create_fen_position(output) -> str:
    pass


frames = []  # raw data
fen_positions = []

for frame in frames:
    # adjust the angle of the picture
    frame = adjust_angle(frame)
    # process the color
    frame = process_color(frame)
    # adjust the board
    frame = adjust_board(frame)
    # detect the all pieces, get the raw coordinate
    output = detect_pieces(frame)
    # change to fen_positions
    fen_position = create_fen_position(frame)
    # collect all state of the game
    fen_positions.append(fen_positions)

chessBoardDetector = ChessBoardDetector(cv2.imread("image/image.png"))

image = chessBoardDetector.get_chessboard_image()

chessPieceDetector = ChessPieceDetector(image)

fen_position = chessPieceDetector.get_fen_position()
print(fen_position)

