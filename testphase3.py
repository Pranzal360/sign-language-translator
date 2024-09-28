from flet import *
import threading
import time
import cv2
import base64
import torch
from ultralytics import YOLO

# Load the YOLO model and ensure it's on the GPU
model = YOLO("last.pt")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def main(page: Page):
    page.title = "Sign Language Translation with YOLO and CUDA"

    header = Text(
        "Turn the camera on to start translating",
        size=25,
        font_family="Inter",
        weight=FontWeight.BOLD
    )

    middle = Text(
        "The camera is off by default. Once you turn it on, you'll see yourself and your surroundings in this area.",
        size=15
    )

    recognized_text = Text("", size=20, weight=FontWeight.BOLD)

    button = ElevatedButton(text="Start", on_click=lambda e: start_camera())
    quit_button = ElevatedButton(
        text="Close camera",
        bgcolor="Red",
        color="Black",
        on_click=lambda e: stop_camera()
    )
    speak_btn = IconButton (
        icon=icons.MIC,
        bgcolor='blue',
        visible=False,
        on_click=lambda e: start_recording_audio()
    )
    btn_container = Row (
        controls=[quit_button,speak_btn]
    )
    text_above_btn = Column(
        controls=[recognized_text,btn_container],
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER
    )
    quit_button.visible = False

    combine = Column(
        controls=[header, middle,button],
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER
    )

    container = Container(
        content=combine,
        alignment=Alignment(0, 0)
    )

    b64_string = None
    global cap
    image_box = Image(src_base64=b64_string, width=500, height=500)
    image_box.visible = False  # Initially hidden

    def start_recording_audio():
        import speech_recognition as sr
        import pyttsx3

        r = sr.Recognizer()

        engine = pyttsx3.init()
        try: 
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
            
            #listens for the user's input 
            audio2 = r.listen(source2)
            
            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()

            print(MyText)
        
        except sr.RequestError as e:
            print("Could not request results")
        
        except sr.UnknownValueError:
            print("unknown error occurred")
    # Function to start the camera
    def start_camera():
        global cap
        cap = cv2.VideoCapture(0)  # Open webcam
        time.sleep(1)  # Allow time for camera initialization

        threading.Thread(target=capture_frames, daemon=True).start()

    # Function to capture frames
    # Function to capture frames
    def capture_frames():
        global cap
        if cap.isOpened():
            image_box.visible = True  # Show the image box when starting to capture
            page.update()  # Update the page to show the image box

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    continue  # Skip the iteration if no frame is captured

                frame = cv2.flip(frame, 1)  # Flip the frame for better UX
                
                # Run the frame through the YOLO model
                results = model(frame, device=device, show=False)  # Use GPU for inference
                
                # Extract recognized classes and their labels
                recognized_texts = []
                for result in results:
                    # Access the predicted classes directly
                    if result.boxes is not None:  # Ensure there are boxes detected
                        for box in result.boxes:
                            class_id = int(box.cls)  # Get class index
                            confidence = box.conf  # Get confidence score

                            if confidence > 0.5:  # Threshold to consider the detection
                                label = model.names[class_id]  # Get class label
                                recognized_texts.append(label)  # Add label to list

                    frame = result.plot()  # Draw bounding boxes on the frame

                # Update recognized text display
                
                # Convert the frame to JPEG and then Base64 for Flet
                jpg_img = cv2.imencode(".jpg", frame)[1]
                b64_string = base64.b64encode(jpg_img).decode("utf-8")
                image_box.src_base64 = b64_string
                
                header.value = "Sign Language to Text"
                middle.value = "Hold your hands up and start signing. Your signs will be transmitted into text in real-time."
                recognized_text.value = ', '.join(recognized_texts)  # Update the displayed text
                button.visible = False
                quit_button.visible = True
                speak_btn.visible = True
                page.update()  # Update the page to reflect changes
                
                time.sleep(0.03)  # Control frame rate


    # Function to stop the camera
    def stop_camera():
        global cap
        if cap is not None:
            cap.release()  # Release the camera

        button.visible = True  # Show the start button again
        quit_button.visible = False  # Hide the quit button
        image_box.visible = False  # Hide the image box
        header.value = "Turn the camera on to start translating"
        middle.value = "The camera is off by default. Once you turn it on, you'll see yourself and your surroundings in this area."
        recognized_text.value = ""  # Clear the recognized text
        speak_btn.visible = False
        page.update()

    contain = Container(
        image_box,
        alignment=alignment.center,
        expand=True
    )
    
    # Add the image box container to the page
    page.add(container, contain, text_above_btn)

app(main)



# make the UI clean as we wrote above, the text should be below us, add the buttons to speak the text 
