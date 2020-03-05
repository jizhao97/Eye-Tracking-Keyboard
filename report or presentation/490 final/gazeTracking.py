import cv2
import numpy as np
import dlib

#cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("face_shape.dat")

def calc_gaze_ratio(points, landmarks, img, gray_img):
    eye_region = np.array([(landmarks.part(points[0]).x, landmarks.part(points[0]).y),
                           (landmarks.part(points[1]).x, landmarks.part(points[1]).y),
                           (landmarks.part(points[2]).x, landmarks.part(points[2]).y),
                           (landmarks.part(points[3]).x, landmarks.part(points[3]).y),
                           (landmarks.part(points[4]).x, landmarks.part(points[4]).y),
                           (landmarks.part(points[5]).x, landmarks.part(points[5]).y)], np.int32)

    gray_img = cv2.blur(gray_img, (3,3), 0)
    _, threshold_img = cv2.threshold(gray_img, 40, 255, cv2.THRESH_BINARY_INV)

    height, width, _ = img.shape
    mask = np.zeros((height, width), np.uint8)

    cv2.polylines(mask, [eye_region], True, 255, 1)
    cv2.fillPoly(mask, [eye_region], 255)
    masked_img = cv2.bitwise_and(threshold_img, threshold_img, mask=mask)

    min_x = np.min(eye_region[:, 0])
    max_x = np.max(eye_region[:, 0])
    min_y = np.min(eye_region[:, 1])
    max_y = np.max(eye_region[:, 1])

    threshold_eye = masked_img[min_y: max_y, min_x: max_x]
    threshold_eye = cv2.bitwise_not(threshold_eye)

    height, width = threshold_eye.shape
    left_side = threshold_eye[0: height, 0: int(width / 2)]
    left_left = threshold_eye[0: height, 0: int(width / 4)]
    right_side = threshold_eye[0: height, int(width / 2): width]
    right_right = threshold_eye[0: height, int(width * 3 / 4): width]
    bot_side = threshold_eye[0: int(height / 2), 0: width]
    bot_bot = threshold_eye[0: int(height / 4), 0: width]
    top_side = threshold_eye[int(height / 2): height, 0: width]
    top_top = threshold_eye[int(height * 3 / 4): height, 0: width]

    SCALE_FACTOR = 100

    left_white = (cv2.countNonZero(left_side) + cv2.countNonZero(left_left) * 0.5) / ((width/2)*height)
    right_white = (cv2.countNonZero(right_side) + cv2.countNonZero(right_right) * 0.5) / ((width/2)*height)
    top_white = (cv2.countNonZero(top_side) + cv2.countNonZero(top_top) * 0.5) / (width*(height/2))
    bot_white = (cv2.countNonZero(bot_side) + cv2.countNonZero(bot_bot) * 0.5) / (width*(height/2))

    threshold_eye = cv2.resize(threshold_eye, None, fx=5, fy=5)
    cv2.imshow("eye", threshold_eye)

    downLook = width/(height*3.5)

    vRat = (top_white - bot_white * downLook) * SCALE_FACTOR
    hRat = (right_white - left_white) * SCALE_FACTOR

    # blinking detection

    blink = False

    white = cv2.countNonZero(threshold_eye) / np.sum(threshold_eye >= 0)
    if white > 0.9999999999999:
        blink = True;


    return vRat, hRat, blink


def gaze_position(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    vLeft = 0
    hLeft = 0
    vRight = 0
    hRight = 0
    bLeft = False
    bRight = False


    faces = detector(gray_img)

    vGaze = 0
    hGaze = 0

    for face in faces:
        landmarks = predictor(gray_img, face)

        vLeft, hLeft, bLeft = calc_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks, img, gray_img)
        vRight, hRight, bRight = calc_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks, img, gray_img)

        for i in range(60):
            cv2.circle(img, (landmarks.part(i).x, landmarks.part(i).y), 1, (0, 0, 255), 1)

    return vLeft, hLeft, vRight, hRight, bLeft, bRight