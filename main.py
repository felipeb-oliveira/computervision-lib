from cameraLib import CameraPredict

def main():
	# Get instance by custom constructor
	try:
		# Try to get instance
		camPred = CameraPredict.getInstance()
	except Exception as e:
		# Handle error properly
		print(e)
		return

	# Print options
	while(True):
		print("Choose an option:")
		print("\t1. Take picture")
		print("\t2. Take picture and predict")
		print("\t3. Predict video")
		print("\t0. Exit")

		# Switch user input
		txt = input()
		if(txt == "1"):
			camPred.takePicture()
			camPred.showImage()

		elif(txt == "2"):
			camPred.takePicture()
			out,label = camPred.predict()
			txt = label + " - " + str(out)
			print(txt)
			camPred.showImage(text=txt)

		elif(txt == "3"):
			camPred.predictVideo()

		elif(txt == "0"):
			return

		else:
			print("Invalid Option")



if __name__ == "__main__":
	main()