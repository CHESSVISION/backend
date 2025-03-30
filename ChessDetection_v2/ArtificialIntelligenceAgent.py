from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import cv2
import supervision as sv
from datetime import datetime

from ChessDetection_v2.machine_learning.ChessBoardDetector import chess_board_detector
from ChessDetection_v2.machine_learning.ChessPieceDetector import chess_piece_detector
from ChessDetection_v2.machine_learning.HandDetector import hand_detector


class ArtificialIntelligenceAgent:

    def image_to_fen(self, file_path):
        try:
            image = chess_board_detector.get_chessboard_image(cv2.imread(file_path))
            fen_position = chess_piece_detector.get_fen_position(image)
        except Exception as e:
            return ["8/8/8/8/8/8/8/8"]
        return [fen_position]

    def video_to_fen(self, video_file_path):
        print("ArtificialIntelligenceAgent: video_to_fen")
        print("video file path: ", video_file_path)

        video_capture = cv2.VideoCapture(video_file_path)

        if not video_capture.isOpened():
            print("video open failed")
            exit()

        cache_frames = []
        fen_positions = []

        while True:
            success, frame = video_capture.read()

            if not success and not cache_frames:
                print("End: capture failed")
                break

            if frame is not None:
                if not hand_detector.found_hand_detected(frame):
                    cache_frames.append(frame)
                    continue

            voted_fen = defaultdict(int)

            for cache_frame in cache_frames:
                try:
                    image = chess_board_detector.get_chessboard_image(cache_frame)
                    fen_position = chess_piece_detector.get_fen_position(image)
                    voted_fen[fen_position] += 1
                except Exception as e:
                    continue

            cache_frames.clear()

            total_frames = sum(voted_fen.values())

            if total_frames <= 6:
                print(f"Discard: too few {total_frames}")
                continue

            selected_fen, selected_fen_frames = max(voted_fen.items(), key=lambda item: item[1])

            if selected_fen_frames < total_frames / 3:
                print(f"Discard: lower than 0.5 ratio {selected_fen_frames} : {total_frames}")
                continue

            if fen_positions:
                if fen_positions[-1] != selected_fen:
                    fen_positions.append(selected_fen)
            else:
                fen_positions.append(selected_fen)

            print(f"Add fen: selected fen {fen_positions[-1]}")

        video_capture.release()
        return fen_positions

    def video_to_fen_chat(self, video_file_path):
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

    @staticmethod
    def shorten_label(label):
        mapping = {
            "white-king": "K", "white-queen": "Q", "white-rook": "R",
            "white-bishop": "B", "white-knight": "N", "white-pawn": "P",
            "black-king": "k", "black-queen": "q", "black-rook": "r",
            "black-bishop": "b", "black-knight": "n", "black-pawn": "p",
            "hand": "H", "chessboard": "B"
        }
        return mapping.get(label, label[:1])

    def generate_annotated_video(self, video_file_path, output_path=None):
        print("🎥 Generating annotated video...")

        video_capture = cv2.VideoCapture(video_file_path)
        if not video_capture.isOpened():
            print("❌ Failed to open video.")
            return None

        width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = video_capture.get(cv2.CAP_PROP_FPS)

        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"annotated_{timestamp}.mp4"

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        box_annotator = sv.BoxAnnotator(thickness=1, color=sv.Color.from_hex('#CCCCCC'))
        label_annotator = sv.LabelAnnotator(text_thickness=1, text_scale=0.4, text_padding=2)

        frame_idx = 0
        while True:
            success, frame = video_capture.read()
            if not success:
                break

            frame_idx += 1
            print(f"Processing frame {frame_idx}", end='\r')

            for detector in [chess_board_detector, chess_piece_detector, hand_detector]:
                detector.set_image(frame)
                detections = detector.get_detections()
                if detections and len(detections.xyxy) > 0:
                    short_labels = [self.shorten_label(cls) for cls in detections.data["class_name"]]
                    detections.data["class_name"] = short_labels
                    frame = box_annotator.annotate(scene=frame, detections=detections)
                    frame = label_annotator.annotate(scene=frame, detections=detections)

            video_writer.write(frame)

        video_capture.release()
        video_writer.release()
        print(f"\n✅ Annotated video saved at: {output_path}")
        return output_path


artificial_intelligence_agent = ArtificialIntelligenceAgent()

# CLI
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate annotated chess video with bounding boxes.")
    parser.add_argument("input", help="Path to the input video file")
    parser.add_argument("-o", "--output", help="Path to save the annotated video (optional)")

    args = parser.parse_args()

    agent = ArtificialIntelligenceAgent()
    agent.generate_annotated_video(video_file_path=args.input, output_path=args.output)
