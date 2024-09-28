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

    button = ElevatedButton(text="Start", on_click=lambda e: start_camera())
    quit_button = ElevatedButton(
        text="Quit Now",
        bgcolor="Red",
        color="Black",
        on_click=lambda e: stop_camera()
    )

    quit_button.visible = False

    combine = Column(
        controls=[header, middle, button],
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

    # Function to start the camera
    def start_camera():
        global cap
        cap = cv2.VideoCapture(0)  # Open webcam
        time.sleep(1)  # Allow time for camera initialization

        threading.Thread(target=capture_frames, daemon=True).start()

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
                
                # Draw bounding boxes on the frame (if results exist)
                for result in results:
                    frame = result.plot()
                    # print(f"result = {result)}")

                # Convert the frame to JPEG and then Base64 for Flet
                jpg_img = cv2.imencode(".jpg", frame)[1]
                b64_string = base64.b64encode(jpg_img).decode("utf-8")
                image_box.src_base64 = b64_string
                
                header.value = "Sign Language to Text"
                middle.value = "Hold your hands up and start signing. Your signs will be transmitted into text in real-time."
                button.visible = False
                quit_button.visible = True
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
        page.update()

    contain = Container(
        image_box,
        alignment=alignment.center,
        expand=True
    )
    
    # Add the image box container to the page
    page.add(container, quit_button, contain)

app(main)
