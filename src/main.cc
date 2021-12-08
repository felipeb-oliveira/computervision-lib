#include <iostream>
#include <string.h>
#include <memory>
#include <float.h>

using namespace std;
using namespace cv;

typedef int Mat;

bool takePicture(Mat* pic, int cameraIndex = 0);

bool takePicture(Mat* pic, int cameraIndex){
    VideoCapture vc(cameraIndex);

    // Error check
    if(!isOpened()){
        return false;
    }

    // Take picture
    vc.read(*pic);

    // Return picture
    return true;
}


float* predict(Mat img, std::unique_ptr<tflite::FlatBufferModel> model){
    // Build the interpreter
    tflite::ops::builtin::BuiltinOpResolver resolver;
    std::unique_ptr<tflite::Interpreter> interpreter;
    tflite::InterpreterBuilder(model, resolver)(&interpreter);

    // Resize input tensors, if desired.
    interpreter->AllocateTensors();

    float* input = interpreter->typed_input_tensor<float>(0);
    *input = img;

    interpreter->Invoke();

    float* output = interpreter->typed_output_tensor<float>(0);
    return output;
}


float* predictCamera(int cameraIndex){
    Mat *picture;

    // Take picture
    if(!takePicture(picture)){
        // Error handle
    }

    // Predict
    

    // Return

}

// Camera - Dog/Cat (98%)

void predictAndShow(){
    // Create variables
    float* prediction;
    VideoCapture cap(0);
    Mat frame;
    int maxIndex;
    int maxValue;

    // Window string variables
    string predictString[] = {"Cat", "Dog"};
    string title = "Camera - ";

    // Open model
    std::unique_ptr<tflite::FlatBufferModel> model = tflite::FlatBufferModel::BuildFromFile('src/mode.tflite');

    while(true){
        // Get frame
        cap.read(frame);

        // Predict frame
        prediction = predict(frame, *model);

        // Get highest index
        if(prediction[0] > prediction[1]){
            maxIndex = 0;
            maxValue = 0;
        } else {
            maxIndex = 1;
            maxValue = 1;
        }

        // Show image and prediction
        imshow(title + predictString[maxIndex] + "(" + to_string(maxValue) + ")", frame);

        // Check for exit
        if(waitKey(1000 / 30) >= 0){
            break;
        }
    }
}


int main(){

    float values[2];
    values = predict();


    predictAndShow();
    return 0;
}


