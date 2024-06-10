import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
import cv2
import base64
import asyncio
from random import randint
from time import sleep
import imutils
import numpy as np
import cv2,urllib.request
from ultralytics.solutions.parking_management import ParkingManagement



class ChatConsumer(WebsocketConsumer):
    statusing  = False
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        ChatConsumer.statusing = True

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        
        with open('chat\people.jpg', 'rb') as file:
            image_bytes = file.read()
        
			
        self.send(text_data = json.dumps({"message": message}), bytes_data=image_bytes)
        
        

class VideoCamera(object):
    
	def __init__(self):
		self.url = 'http://192.168.137.53/cam-hi.jpg'
		self.polygon_json_path = "chat/bounding_boxes.json"
		self.Model = ParkingManagement(model_path="integers/yolov8n.pt")
		self.json_data = self.Model.parking_regions_extraction(self.polygon_json_path)
	
 
	def __del__(self):
		pass

	def get_frame(self):
		img_resp = urllib.request.urlopen(self.url)
		imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
		image = cv2.imdecode(imgnp, -1)
  
		results = self.Model.model.track(image, persist=True, show=False,show_labels=False)

		if results[0].boxes.id is not None:
			boxes = results[0].boxes.xyxy.cpu().tolist()
			clss = results[0].boxes.cls.cpu().tolist()
			self.Model.process_data(self.json_data, image, boxes, clss)

		ret, jpeg = cv2.imencode('.jpg', image)
		return jpeg.tobytes()