import os
from django.conf import settings
import dlib
import cv2 as cv
import numpy as np
import pandas as pd


# 두점 사이 거리 구하는 함수
def dist(list, index1, index2):
    return ((list[index1][0]-list[index2][0])**2+((list[index1][1]-list[index2][1])**2))**(1/2)


# 광대크기 구하는 함수
def cheek_size(array):
    cheek_height1 = dist(array, 0, 2)
    cheek_area1 = abs(np.cross(array[0]-array[1], array[2]-array[1]))
    cheek_height2 = dist(array, 1, 3)
    cheek_area2 = abs(np.cross(array[1]-array[2], array[3]-array[2]))
    cheek_height3 = dist(array, 14, 16)
    cheek_area3 = abs(np.cross(array[14]-array[15], array[16]-array[15]))
    cheek_height4 = dist(array, 13, 15)
    cheek_area4 = abs(np.cross(array[13]-array[14], array[15]-array[14]))
    cheek_size1 = 100*cheek_area1/cheek_height1**2
    cheek_size2 = 100*cheek_area2/cheek_height2**2
    cheek_size3 = 100*cheek_area3/cheek_height3**2
    cheek_size4 = 100*cheek_area4/cheek_height4**2
    cheek_size = max(cheek_size1, cheek_size2, cheek_size3, cheek_size4)
    return cheek_size


# 턱크기 구하는 함수
def jaw_size(array):
    jaw_height1 = dist(array, 2, 4)
    jaw_area1 = abs(np.cross(array[2]-array[3], array[4]-array[3]))
    jaw_height2 = dist(array, 3, 5)
    jaw_area2 = abs(np.cross(array[3]-array[4], array[5]-array[4]))
    jaw_height3 = dist(array, 12, 14)
    jaw_area3 = abs(np.cross(array[12]-array[13], array[14]-array[13]))
    jaw_height4 = dist(array, 11, 13)
    jaw_area4 = abs(np.cross(array[11]-array[12], array[13]-array[12]))
    jaw_size1 = 100*jaw_area1/jaw_height1**2
    jaw_size2 = 100*jaw_area2/jaw_height2**2
    jaw_size3 = 100*jaw_area3/jaw_height3**2
    jaw_size4 = 100*jaw_area4/jaw_height4**2
    jaw_size = max(jaw_size1, jaw_size2, jaw_size3, jaw_size4)
    return jaw_size


# 가로 세로 비율 구하기 함수
def face_hor_ver_ratio(array):
    horizontal_dist = array[0][0]-array[16][0]
    eyebrow_middle = (array[21]+array[22])/2
    vertical_dist = eyebrow_middle[1]
    face_hor_ver_ratio = vertical_dist/horizontal_dist
    return face_hor_ver_ratio


class Face:

    def __init__(self):
        self.face_det = dlib.get_frontal_face_detector()
        self.landmark_model = dlib.shape_predictor(
            settings.BASE_DIR+"/static/shape_predictor_68_face_landmarks.dat")

    def calculate(self, imgLink):
        # 사진 넣었을 때 각 부위별 특징 도출
        src = cv.imread(settings.BASE_DIR+imgLink)  # 넣을사진

        if src is not None:
            grey = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

            # 얼굴검출
            face = self.face_det(grey)

            if (len(face) != 0):
                # 랜드마크 검출
                lm = self.landmark_model(src, face[0])

                lm_point = []
                for p in lm.parts():
                    lm_point.append([p.x, p.y])
                lm_point = np.array(lm_point)

                # 점들 정규화 시키기

                # 평행이동
                lm_point = lm_point-lm_point[8]

                # 기울어진 각도 구하기
                chin_to_bridge = dist(lm_point, 27, 8)
                chin_to_bridge_height = (lm_point[27][1]-lm_point[8][1])
                chin_to_bridge_width = (lm_point[27][0]-lm_point[8][0])
                cos_tilt = chin_to_bridge_height/chin_to_bridge
                sin_tilt = chin_to_bridge_width/chin_to_bridge

                # 배열 회전시키
                rotation_matrix = np.array(
                    [[cos_tilt, -sin_tilt], [sin_tilt, cos_tilt]])
                for idx, val in enumerate(lm_point):
                    rotate_array = rotation_matrix@np.array(
                        [[val[0]], [val[1]]])
                    lm_point[idx][0] = rotate_array[0][0]
                    lm_point[idx][1] = rotate_array[1][0]

                # 키워드 담을 배열
                keywords = []

                # 광대크기 구하기
                keywords.append(cheek_size(lm_point))

                # 옆턱크기 구하기
                keywords.append(jaw_size(lm_point))

                # 가로세로비율 구하기
                keywords.append(face_hor_ver_ratio(lm_point))

                return keywords
