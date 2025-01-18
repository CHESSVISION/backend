from inference import get_model
import supervision as sv


class ChessPieceDetector:
    model = get_model(model_id="chess-pieces-new/19")

    def __init__(self, image):
        self.__image = image
        self.__detections = None
        self.detect()

    def set_image(self, image):
        # self.__image = cv2.imread(image_file)
        self.__image = image
        self.detect()

    def detect(self):
        results = self.model.infer(self.__image)[0]
        self.__detections = sv.Detections.from_inference(results)

    def get_detections(self):
        return self.__detections

    def get_fen_position(self):
        side = self.__image.shape[0]

        # Chessboard parameters
        width = side
        height = side
        square_size = width / 10  # Grid is 10x10 including padding

        # Initialize an 8x8 board
        board = [['' for _ in range(8)] for _ in range(8)]

        # Map piece names to FEN notation
        fen_mapping = {
            'white-king': 'K',
            'white-pawn': 'P',
            'black-king': 'k',
            'white-bishop': 'B',
            'black-pawn': 'p',
            'black-bishop': 'b'
        }

        # Process each detection
        for i, box in enumerate(self.get_detections().xyxy):
            x_center = (box[0] + box[2]) / 2
            y_base = ((box[1] + box[3]) / 2) + (max(box[1], box[3]) - ((box[1] + box[3]) / 2)) / 2

            col = int(x_center // square_size) - 1  # Adjust for padding
            row = int(y_base // square_size) - 1  # Flip row for FEN

            if 0 <= row < 8 and 0 <= col < 8:
                board[col][row] = fen_mapping[self.get_detections().data["class_name"][i]]

        # Convert board to FEN
        fen_rows = []
        for row in board:
            fen_row = ''
            empty_count = 0
            for square in row:
                if square == '':
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen_row += str(empty_count)
                        empty_count = 0
                    fen_row += square
            if empty_count > 0:
                fen_row += str(empty_count)
            fen_rows.append(fen_row)
        fen_rows.reverse()

        # Join rows with '/'
        fen = '/'.join(fen_rows)
        return fen

    def display_image(self):
        bounding_box_annotator = sv.BoxAnnotator()
        label_annotator = sv.LabelAnnotator()

        # annotate the image with our inference results
        annotated_image = bounding_box_annotator.annotate(
            scene=self.__image, detections=self.get_detections())
        annotated_image = label_annotator.annotate(
            scene=annotated_image, detections=self.get_detections())

        # display the image
        sv.plot_image(annotated_image)
