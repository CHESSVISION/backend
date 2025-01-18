from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

import cv2

from ChessDetection_v2.machine_learning.ChessBoardDetector import chess_board_detector
from ChessDetection_v2.machine_learning.ChessPieceDetector import chess_piece_detector
from ChessDetection_v2.machine_learning.HandDetector import hand_detector


class ArtificialIntelligenceAgent:
    def video_to_fen(self, video_file_path):

        # Open the videos file
        video_capture = cv2.VideoCapture(video_file_path)

        # Check if the videos file was successfully opened
        if not video_capture.isOpened():
            exit()

        # Set up state of the videos
        # 1. initial position by frame before detected hand
        cache_frames = []
        fen_positions = []
        # Loop through each frame
        while True:
            # Read the next frame from the videos
            success, frame = video_capture.read()

            # If the frame was not read successfully, break the loop (end of videos)
            if not success:
                break

            if hand_detector.found_hand_detected(frame):
                if cache_frames:
                    voted_fen = defaultdict(int)

                    for cache_frame in cache_frames:
                        try:
                            image = chess_board_detector.get_chessboard_image(cache_frame)
                            fen_position = chess_piece_detector.get_fen_position(image)
                            voted_fen[fen_position] += 1
                        except Exception as e:
                            continue

                    if voted_fen:
                        valid_fen = max(voted_fen, key=voted_fen.get)

                        if fen_positions:
                            if fen_positions[-1] != valid_fen:
                                fen_positions.append(valid_fen)
                        else:
                            fen_positions.append(valid_fen)

                    cache_frames.clear()
                continue

            cache_frames.append(frame)

        # Release the videos capture object and close all OpenCV windows
        video_capture.release()
        return fen_positions

    def video_to_fen_chat(self, video_file_path):

        # Open the videos file
        video_capture = cv2.VideoCapture(video_file_path)
        if not video_capture.isOpened():
            return []

        cache_frames = []
        fen_positions = []

        def process_frame(frame):
            if hand_detector.found_hand_detected(frame):
                voted_fen = defaultdict(int)
                for cache_frame in cache_frames:
                    try:
                        fen_position = chess_piece_detector.get_fen_position(
                            chess_board_detector.get_chessboard_image(cache_frame)
                        )
                        voted_fen[fen_position] += 1
                    except Exception:
                        continue
                if voted_fen:
                    valid_fen = max(voted_fen, key=voted_fen.get)
                    if not fen_positions or fen_positions[-1] != valid_fen:
                        fen_positions.append(valid_fen)
                cache_frames.clear()

        with ThreadPoolExecutor(max_workers=4) as executor:
            while True:
                success, frame = video_capture.read()
                if not success:
                    break
                executor.submit(process_frame, frame)
                cache_frames.append(frame)

        video_capture.release()
        return fen_positions


artificial_intelligence_agent = ArtificialIntelligenceAgent()
