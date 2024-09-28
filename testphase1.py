from flet import *
import threading
import time
import cv2
import base64
from ultralytics import YOLO  # YOLO integration

def main(page: Page):
    page.title = "Sign Language Translation"

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

    # Button to start camera
    button = ElevatedButton(text="Start", on_click=lambda e: on("on"))

    # Quit button to stop the camera
    quit_button = ElevatedButton(
        text="Quit Now",
        bgcolor="Red",
        color="Black",
        on_click=lambda e: on('off')  # Call on() with "off"
    )

    quit_button.visible = False

    # Combine UI elements
    combine = Column(
        controls=[header, middle, button],  # Include quit button in the layout
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER
    )

    container = Container(
        content=combine,
        alignment=Alignment(0, 0)
    )
    
    global cap
    b64_string = None
    image_box = Image(src_base64=b64_string, width=500, height=500)

    # Load YOLO model
    model = YOLO("last.pt")  # Assuming "last.pt" is your trained model for sign detection

    def on(var):
        global cap
        if var == "on":
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("Error: Could not open webcam.")
                return

            # Thread for reading frames and running YOLO inference
            def update_image():
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    frame = cv2.flip(frame, 1)  # Flip the frame to avoid mirrored view
                    
                    # YOLO Inference
                    results = model(frame)  # Run inference on the frame

                    # Visualize results
                    annotated_frame = results[0].plot()  # Draw bounding boxes on the frame

                    # Convert annotated frame to base64 for displaying in Flet
                    _, jpg_img = cv2.imencode(".jpg", annotated_frame)
                    b64_string = base64.b64encode(jpg_img).decode("utf-8")
                    image_box.src_base64 = b64_string
                    page.update()  # Update the page with the annotated frame
                    time.sleep(0.06)  # Limit the frame rate to about 16 FPS

            # Run the video feed with YOLO in a thread
            threading.Thread(target=update_image, daemon=True).start()
            
            # Update the UI
            header.value = "Sign Language to Text"
            middle.value = "Hold your hands up and start signing. Your signs will be transmitted into text in real time."
            button.visible = False
            quit_button.visible = True
            page.update()

        else:  # Turn off the camera
            cap.release()
            quit_webcam()

    def quit_webcam():
        button.visible = True  # Show the start button again
        quit_button.visible = False  # Hide the quit button
        image_box.src_base64 = None  # Reset the image
        header.value = "Turn the camera on to start translating"
        middle.value = "The camera is off by default. Once you turn it on, you'll see yourself and your surroundings in this area."
        page.update()

    contain = Container(
        content=image_box,
        alignment=alignment.center,
        expand=True
    )
    
    # Add UI elements to the page
    page.add(combine, contain, quit_button)

app(main)


# Works but lags + errors about imageview need to be fixed