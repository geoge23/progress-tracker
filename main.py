import cv2
import os
import paho.mqtt.client as mqtt
from pymongo import MongoClient


def take_and_send_pic():
    cap = cv2.VideoCapture(os.environ['CAM_ID'] or 0)
    frame = cap.read()
    print(frame)

take_and_send_pic()