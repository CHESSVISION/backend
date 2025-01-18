from ChessDetection_v2.machine_learning.MachineLearning import MachineLearning


class ChessPieceDetector(MachineLearning):
    def __init__(self, image=None, model_id="chess-pieces-new/19"):
        super().__init__(image, model_id)

    def get_fen_position(self, image=None):
        if image is not None:
            self.set_image(image)

        side = self.get_image().shape[0]

        # Chessboard parameters
        width = side
        height = side
        square_size = width / 10  # Grid is 10x10 including padding

        # Initialize an 8x8 board
        board = [['' for _ in range(8)] for _ in range(8)]

        # Map piece names to FEN notation
        fen_mapping = {
            'white-king': 'K',
            'white-queen': 'Q',
            'white-rook': 'R',
            'white-bishop': 'B',
            'white-knight': 'N',
            'white-pawn': 'P',
            'black-king': 'k',
            'black-queen': 'q',
            'black-rook': 'r',
            'black-bishop': 'b',
            'black-knight': 'n',
            'black-pawn': 'p'
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
