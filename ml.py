from model.user import User

import pandas as pd
import numpy as np
import cv2
import tensorflow as tf
from google.cloud import firestore, storage
from io import StringIO

storege_client = storage.Client()

#model読み込み
blob = storege_client.get_bucket("manerun-mlengine").blob("test.h5")
model = tf.keras.models.load_model(blob.download_as_string())

def Score_generate(csv_str):
    #CSVの読み込み
    csv_data = StringIO(csv_str.decode("utf-8"))
    df_Data=pd.read_csv(csv_data)
    
    width = 24
    height = len(df_Data)
    
    # uint8で0埋めの配列を作る。
    # zeros(shape, type) shapeは配列の大きさ
    # 配列の（行数、列数）になっている
    # 画像はwidth,heightの慣習があるが、ココは逆なので気をつけること
    imageArray = np.zeros((height, width, 3), np.uint8)
    
    for h in range(0, height):
        for w in range(0, width):
            R=float(df_Data.iat[h,4+w*3])
            R=R/2+127.5
            G=float(df_Data.iat[h,5+w*3])
            G=G/2+127.5
            B=float(df_Data.iat[h,6+w*3])
            B=B/2+127.5
            imageArray[h, w] = [B,G,R]
    
    #画像のリサイズと保存
    imageArray=cv2.resize(imageArray, dsize=(400, 400))
    cv2.imwrite('motion.png', imageArray)
    
    #おまじない
    image = tf.io.read_file('motion.png')
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, [400, 400])
    image /= 255.0
    image=image[None, ...]
    score=model.predict(image)[0,0]
    
    return score#点数


"""
    entry point.
"""
def delegate_ML(user):
    csv_str = storege_client.get_bucket("manerun-motions").blob(user.csv_id).download_as_string()
    score = Score_generate(csv_str)
    firestore.Client().collection("users").document(user.id).update({"score":score})
