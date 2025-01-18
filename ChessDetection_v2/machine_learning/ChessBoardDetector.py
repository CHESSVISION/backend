import math
import numpy as np
import cv2 as cv
from ChessDetection_v2.machine_learning.MachineLearning import MachineLearning


class ChessBoardDetector(MachineLearning):

    def __init__(self, image=None, model_id="chessboard-detection-yqcnu/3"):
        super().__init__(image, model_id)

    def get_conor(self):
        points = []

        for box in self.get_detections().xyxy:
            x = (box[0] + box[2]) / 2
            y = (box[1] + box[3]) / 2
            points.append([x, y])

        points = sorted(points, key=lambda point: (point[1], point[0]))

        # Top two points are the top-left and top-right
        top_left, top_right = sorted(points[:2], key=lambda point: point[0])

        # Bottom two points are the bottom-left and bottom-right
        bottom_left, bottom_right = sorted(points[2:], key=lambda point: point[0])

        return [top_left, top_right, bottom_left, bottom_right]

    def get_chessboard_image(self, image=None):
        if image is not None:
            self.set_image(image)

        top_left, top_right, bottom_left, bottom_right = self.get_conor()

        points_on_board = np.float32([top_left, top_right, bottom_left, bottom_right])

        width = math.sqrt((top_right[0] - top_left[0]) ** 2 + (top_right[1] - top_left[1]) ** 2)

        height = math.sqrt((bottom_left[0] - top_left[0]) ** 2 + (bottom_left[1] - top_left[1]) ** 2)

        side = (width + height)/2

        padding = side/8

        points_on_image = np.float32([[padding, padding], [side + padding, padding], [padding, side+padding], [side + padding, side + padding]])

        matrix = cv.getPerspectiveTransform(points_on_board, points_on_image)

        dimension_image = (int(side + 2*padding), int(side + 2*padding))

        dst = cv.warpPerspective(self.get_image(), matrix, dimension_image)
        return dst
