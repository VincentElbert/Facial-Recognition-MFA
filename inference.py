import pickle
import os
import numpy as np
import face_recognition
import face_to_encoding
from PIL import Image

def infer(img_buffer):
    img = Image.open(img_buffer)
    img_arr = np.array(img)
    if not face_to_encoding.checkFace(img_arr):
        return None
    else:
        face_enc = face_recognition.face_encodings(img_arr)[0]
        
        with open('face_classifier.pkl', 'rb') as fid:
            clf = pickle.load(fid)
            p = clf.predict_proba(face_enc.reshape(1, -1))
            max_prob_index = np.argmax(p, axis=1)
            max_prob = p[0][max_prob_index]

            if max_prob >= 0.9:
                return clf.classes_[max_prob_index]
            else:
                return "No Match"

def loginInfer(imgdir, label):
    matching_count = 0
    pix = os.listdir(imgdir)
    for img in pix:
        if infer(imgdir + '/' + img) == label:
            matching_count += 1
    return matching_count >= 9

