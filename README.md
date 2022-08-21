# HandsMultiMedia
Hands detection application using Python language, Framework powered by TensorFlow Artificial Intelligence.


## Architecture:
1. Numpy
2. Mediapipe
3. cv2
4. playsound
5. Pygame

## Function
1. File selection function: A file chooser window powered by tkinter for selecting from a computer
movie file.
2. Lens input: Use the default webcam as the input stream for hand motion processing.
3. Video input: Hand motion processing with video file as input stream.
4. Hands-on Alphabet Sound Output: Get the video stream input containing the hand object, process the number of fingers, and then
Back to the alphanumeric displayed on the panel, perform the sound and then stack the letters on the string array.
5. 5-note piano: Get a video stream containing fingers, then play the piano keys according to the number of fingers
The key is displayed in the panel. Key settings: - 1 finger: C - 2 finger: D - 3 finger: E - 4 finger: F - 5 finger: G.
6. Snake game: Snake game using hand fingers.
Key settings: - 1 finger: left - 2 finger: up - 3 finger: down - 4 finger: right.

## Installation prerequisites
1. Make sure you have the sound folder with the main python
program in the same directory and make sure that folder
no nested folders
2. Add the mediapipe library to the python environment,
make sure to set the protobuf version to 4.20.X
5. Add the playsound library to the python environment,
make sure to set the version to 1.2.2
7. If these points have been completed and there are still problems,
Please try running it on pycharm because
spyder can sometimes generate undefined errors


## Installation and run
1. Import the py file from the IDE
2. Make sure to do the installation prerequisites
3. Run the program from the IDE (sometimes loading is a bit slow, and
does not mean the program crashes)
4. A GUI menu will appear, select the input mode and
output mode, then press run
5. The desired selected mode will be active
6. To terminate the active program, press End on the GUI menu
end 
7. To terminate the entire program, press X in the GUI window
icon


© 2022 Nicolas Louis, Multi Media Final Project
