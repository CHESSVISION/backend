from inference import get_model
import supervision as sv
import math
import numpy as np
import cv2 as cv


class ChessBoardDetector:
    model = get_model(model_id="chessboard-detection-yqcnu/3")

    def __init__(self, image):
        self.__image = image
        self.__detections = None
        self.detect()

    def set_image(self, image):
        self.__image = image
        self.detect()

    def detect(self):
        results = self.model.infer(self.__image)[0]
        self.__detections = sv.Detections.from_inference(results)

    def get_detections(self):
        return self.__detections

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

    def get_chessboard_image(self):
        top_left, top_right, bottom_left, bottom_right = self.get_conor()

        points_on_board = np.float32([top_left, top_right, bottom_left, bottom_right])

        width = math.sqrt((top_right[0] - top_left[0]) ** 2 + (top_right[1] - top_left[1]) ** 2)

        height = math.sqrt((bottom_left[0] - top_left[0]) ** 2 + (bottom_left[1] - top_left[1]) ** 2)

        side = (width + height)/2

        padding = side/8

        points_on_image = np.float32([[padding, padding], [side + padding, padding], [padding, side+padding], [side + padding, side + padding]])

        matrix = cv.getPerspectiveTransform(points_on_board, points_on_image)

        dimension_image = (int(side + 2*padding), int(side + 2*padding))

        dst = cv.warpPerspective(self.__image, matrix, dimension_image)
        return dst

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

