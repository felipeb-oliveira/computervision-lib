import numpy as np
import cv2 as cv
import tensorflow as tf

class CameraPredict:
	# CNN input variables
	IMG_H = 128
	IMG_W = 128

	# Key assertion to ensure object is created by getInstance method
	__create_key = object()

	def __init__(self, create_key, cap):
		# Assert constructor is called by getInstance method
		assert(create_key == CameraPredict.__create_key), \
			"OnlyCreatable objects must be created using OnlyCreatable.create"

		self.cap = cap


	@classmethod
	def getInstance(cls, cameraIndex=-1):
		# Open video capture
		cap = cv.VideoCapture(cameraIndex)

		# Check if video devide is opened properly
		if not cap.isOpened():
			raise Exception("Error creating CameraPredict instance! Video device is not opened")

		return CameraPredict(cls.__create_key, cap)


	def takePicture(self):
	    # Capture frame
		ret, frame = self.cap.read()

	    # Check for errors
		if not ret:
			print("Couldn't receive frame")
			return

		# Save and return frame
		self.image = frame
		return frame


	def predict(self, img = None):
		# Get saved input or parameter input
		input_data = img
		if(input_data is None):
			input_data = self.image

		# Load the TFLite model and allocate tensors.
		interpreter = tf.lite.Interpreter(model_path="model.tflite")
		interpreter.allocate_tensors()

		# Get input and output tensors
		input_details = interpreter.get_input_details()
		output_details = interpreter.get_output_details()

		# Pre process input
		input_data = cv.resize(input_data, (self.IMG_H, self.IMG_W))
		input_data = np.array(input_data, dtype="float32") / 255.0
		input_data = np.expand_dims(input_data, axis=0)

		# Set input
		interpreter.set_tensor(input_details[0]['index'], input_data)

		# Feed model and predict
		interpreter.invoke()
		output_data = interpreter.get_tensor(output_details[0]['index'])

		# Get label:
		return output_data[0], self.getLabel(output_data)


	def predictVideo(self):
	    # Display the resulting frame
		while(True):
			# Take picture
			img = self.takePicture()

			# Check for errors
			if(img is not None):
				gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
				
				pred,label = self.predict(img)
				print(str(pred) + " - " + label)

				cv.imshow('Video', gray)
				if cv.waitKey(25) & 0xFF == ord('q'):
					return


	def showImage(self, img = None, text="image"):
		# Get parameter picture or last picture taken
		if(img is None):
			image = self.image
		else:
			image = img

		# Show image
		cv.imshow(text, image)
		cv.waitKey(0)


	def getLabel(self, output_data):
		if(output_data[0][1] > output_data[0][0]):
			label = "Dog"
		else:
			label = "Cat"
		return label

