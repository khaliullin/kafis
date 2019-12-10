# -*- coding: utf-8 -*-
import cv2
import openface
from joblib import load
from PIL import Image

from estimate.core.cert import cert


def warn(*args, **kwargs):
    pass


import warnings
import random
import traceback
import urllib.parse

warnings.warn = warn

# dlibFacePredictor = 'shape_predictor_68_face_landmarks.dat'
dlibFacePredictor = '/home/ubuntu/project/kafis/backend/process/shape_predictor_68_face_landmarks.dat'
networkModel = '/home/ubuntu/project/kafis/backend/process/nn4.small2.v1.t7'
align = openface.AlignDlib(dlibFacePredictor)
net = openface.TorchNeuralNet(networkModel, 96)
models_path = '/home/ubuntu/project/kafis/backend/kafis/estimate/core/model.joblib'


def preprocess(imgPath, gender='F', name=None):
    if name is None:
        name = str(random.randint(1, 999999))
    bgrImg = cv2.imread(urllib.parse.unquote(imgPath))

    rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)

    bb = align.getAllFaceBoundingBoxes(rgbImg)

    class_names = ('красивый', 'обычный', 'некрасивый')

    if len(bb) > 1:
        raise Exception('Найдено больше одного лица!')
    elif len(bb) == 0:
        raise Exception('Не найдено ни одного лица!')
    else:
        bb = align.getAllFaceBoundingBoxes(rgbImg)[0]
        try:
            alignedFace = align.align(96, rgbImg, bb,
                                      landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
            #rep = net.forward(alignedFace).reshape(1, -1)

            left = max(int(bb.left() - bb.width() * 0.5), 0)
            right = min(int(bb.right() + bb.width() * 0.5), int(rgbImg.shape[1]))
            top = max(int(bb.top() - bb.height() * 0.5), 0)
            bottom = min(int(bb.bottom() + bb.height() * 0.5), int(rgbImg.shape[0]))

            models = load(models_path)[0]

            cls_name = 'красивый'#class_names[models[gender].predict(rep)[0]]
            print(cls_name)
            face = Image.fromarray(rgbImg[top:bottom, left:right])
            img_path = cert(face, name, cls_name)
            return img_path, cls_name
        except Exception as e:
            traceback.print_exc()
            raise Exception('Не удаётся извлечь признаки, выберите другую фотографию!' + '\n' + str(e)) 
            

# img1 = '/home/ivan/faces/Kristina_Фомина_75814093_M_4.jpg'
# img2 = '/home/ivan/faces/img/yandex2.jpg'
# img3 = '/home/ivan/faces/img/grim.jpg'
# img4 = '/home/ivan/faces/img/kravez.jpg'
# # try:
# #     preprocess(img1, gender='F')
# # except Exception as e:
# #     print(str(e))
#
# preprocess(img1, gender='F', name='Кристина Фомина')
