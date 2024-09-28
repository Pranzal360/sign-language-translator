**Sign Language Translation - README**

Welcome to the Sign Language Translation project! This application allows real-time translation of sign language into text using computer vision and AI models, along with speech recognition for additional interactivity.

**Table of Contents**

    Overview
    Features
    Installation
    Usage
    Project Structure
    Technologies Used
    Acknowledgments

Overview

This project provides a seamless interface to translate sign language gestures into readable text and also includes a speech recognition system using Whisper AI for Nepali language transcription. It was built with accessibility in mind and designed to help bridge the communication gap between those who use sign language and others.

The application works by:

    Capturing real-time video through your camera.
    Detecting sign language gestures using a pre-trained YOLO model.
    Converting recognized gestures into text.
    Supporting speech-to-text using Whisper AI for additional transcription functionality.

Features

    Real-time Sign Language Recognition: The app captures video frames and recognizes gestures using YOLO model inference.
    Speech-to-Text Recognition: Record and transcribe audio in Nepali using the Whisper AI large model.
    Responsive UI: A dynamic user interface built with Flet library for smooth user interactions.
    Camera Control: Turn the camera on/off and view recognition results directly in the app.
    Interactive Speech Button: Start/stop audio recording for speech transcription.

Installation

    Clone the repository:

    bash

`git clone https://github.com/your-repo/sign-language-translation.git`
cd sign-language-translation

Install the required Python libraries:

bash

`pip install -r requirements.txt`

Download YOLO model weights:

> Make sure to place the last.pt model in the root directory or provide a path to your pre-trained YOLO model.

Install Whisper for Speech Recognition:

bash

`pip install git+https://github.com/openai/whisper.git`

Install OpenCV:

bash

    pip install opencv-python

Usage

    Run the Application: To start the application, run:

    bash

    python app.py

    Using the Interface:
        Turn on the Camera: Press the Start button to begin capturing video.
        Sign Language Recognition: Once the camera is on, perform gestures in front of the camera to see real-time translations into text.
        Speech Recognition: Click the microphone button to record Nepali audio. Click again to stop recording and view the transcription.

Project Structure

graphql

.
├── app.py                   # Main Python script to run the application
├── requirements.txt          # Python dependencies
├── last.pt                   # Pre-trained YOLO model weights (place here)
├── audio.wav                 # Temporary audio file for speech recognition
├── speechR.py                # Module for handling audio recording
└── README.md                 # Project documentation

Technologies Used

    Flet: For creating interactive and dynamic user interfaces.
    YOLO (You Only Look Once): A real-time object detection system used for recognizing sign language gestures.
    OpenAI Whisper: A state-of-the-art speech recognition model used for transcribing Nepali language speech.
    OpenCV: For capturing and processing real-time video frames from the camera.
    Threading: To ensure smooth processing and avoid UI blocking by running tasks concurrently.

Acknowledgments

    YOLO: Thanks to the ultralytics team for providing the pre-trained model used in this project.
    Whisper by OpenAI: For their open-source and versatile speech recognition model.
    Hackathon Team: For the inspiration and drive to complete this project.

License

This project is open-source and available under the MIT License.

Contributors:

    Pranzal Khatiwada  @Pranzal360
    Shuam Rai 
    Rohan Adhikari
