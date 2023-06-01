import os

from ultralytics import YOLO
import cv2
import time

from app.detection.utils import get_all_detections, highlight_licence_plate, highlight_all_detections
from src.recognition.predict import ImageToWordModel


def crop_plates(plates, img):
    results = []
    for plate in plates:
        x1, y1, x2, y2, conf = plate
        # w, h = x2 - x1, y2 - y1
        img_r = img[y1:y2, x1:x2]
        cv2.imshow("Image", img_r)
        cv2.waitKey(0)
        # print(img_r.shape)
        img_r = cv2.cvtColor(img_r, cv2.COLOR_RGB2GRAY)
        results += [img_r]
    return results


def test_speed(model, image):
    start = time.time()
    path = "../../../datasets/512_all_right/512_all/test/images"
    for img in os.listdir(path):
        img = cv2.imread(os.path.join(path, img))
        img = cv2.resize(img, dsize=(512, 512))

        results = model(img, stream=True, )
        detections = get_all_detections(results)
        plates, highlighted_img = highlight_licence_plate(detections, img)

    end = time.time()
    print("The time of execution of above program is :",
          (end - start) * 10 ** 3, "ms")
    # cv2.imshow("Image", highlighted_img)
    # cv2.waitKey(0)


def modified_image_plate_recognition(source, detection_model, recognition_model, size, mode):
    img = cv2.imread(source)
    img_copy = img.copy()

    height, width, channels = img.shape
    img = cv2.resize(img, dsize=(size, size))

    highlighted_img = None

    start = time.time()
    results = detection_model(img, stream=True, task="detect", imgsz=(512, 512))
    pred = time.time()
    print("The time of detection is :",
          (pred - start) * 10 ** 3, "ms")

    detections = get_all_detections(results, height, width)

    if mode == 'all':
        highlighted_img = highlight_all_detections(detections, img)

    if mode == 'plate':
        plates, highlighted_img = highlight_licence_plate(detections, img_copy, recognition_model)

    end = time.time()
    print("The time of execution of above program is :",
          (end - start) * 10 ** 3, "ms")

    print(end - start)
    cv2.imshow("Image", highlighted_img)
    cv2.waitKey(0)


if __name__ == '__main__':
    detection = YOLO("../../src/pretrained_models/YOLOv8s_detection.pt")
    # model.to('cuda')
    recognition = ImageToWordModel(
        model_path="../../src/pretrained_models/MRNet_recognition",
    )

    modified_image_plate_recognition(source="../data/images/example.jpg",
                                     detection_model=detection,
                                     recognition_model=recognition,
                                     size=512,
                                     mode='plate')  # plate or all

    # test_speed(model=model,
    #      image="../Images/car5.jpg")
