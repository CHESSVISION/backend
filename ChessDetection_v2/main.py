from enum import Enum
from ChessBoardDetector import ChessBoardDetector
import cv2
from ChessPieceDetector import ChessPieceDetector
from HandDetector import HandDetector
from collections import defaultdict


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
# print(fen_position)

handDetector = HandDetector(image)
# print(handDetector.found_hand_detected())


# Path to your video file
video_file_path = "/Users/kuisskui/kuisskui/Github/CHESSVISION/backend/ChessDetection_v2/video/(Bonus)Long_Video_label.mp4"

# Open the video file
video_capture = cv2.VideoCapture(video_file_path)

# Check if the video file was successfully opened
if not video_capture.isOpened():
    print("Error: Cannot open video.")
    exit()

# Set up state of the video
# 1. initial position by frame before detected hand
cache_frames = []
fen_positions = []
# Loop through each frame
while True:
    # Read the next frame from the video
    success, frame = video_capture.read()

    # If the frame was not read successfully, break the loop (end of video)
    if not success:
        break

    if handDetector.found_hand_detected(frame):
        if cache_frames:
            voted_fen = defaultdict(int)

            for cache_frame in cache_frames:
                try:
                    fen_position = chessPieceDetector.get_fen_position(chessBoardDetector.get_chessboard_image(cache_frame))
                except Exception as e:
                    continue
                voted_fen[fen_position] += 1

            if voted_fen:
                valid_fen = max(voted_fen, key=voted_fen.get)

                if fen_positions:
                    if fen_positions[-1] != valid_fen:
                        fen_positions.append(valid_fen)
                        print(fen_positions)
                else:
                    fen_positions.append(valid_fen)
                    print(fen_positions)

            cache_frames.clear()
        continue

    cache_frames.append(frame)

# Release the video capture object and close all OpenCV windows
video_capture.release()
print(fen_positions)
