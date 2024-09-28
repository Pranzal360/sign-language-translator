from flet import *
import threading
import time
import cv2
import base64
import torch
from ultralytics import YOLO
import threading
from speechR import audio_file
import whisper

model = YOLO("last2.pt")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def load_wishper():
    global wish_model
    print("loading whisper")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    wish_model = whisper.load_model("base").to(device)
    print("load complete")

threading.Thread(target=load_wishper,daemon=True).start()



def main(page: Page):
    PATH = "audio.wav"
    page.title = "Sign Language Translation"

    recording = False
    
    recn_label = Text("",size=18)

    def transcribe_np():
        if 'wish_model' in globals():
            try:
                result = wish_model.transcribe(PATH, language='ne')
                print("Transcription result:", result['text'])
                recn_label.value = result['text']
                # Update your recognized label with the result here
            except RuntimeError as e:
                print(f"Runtime error during transcription: {e}")
        else:
            print("Whisper model not loaded yet.")

    def handle_state_change(e) :
        print("state changed : {e.data}")
    
    audio = AudioRecorder(
        audio_encoder=AudioEncoder.WAV,
        on_state_changed=handle_state_change
    )
       

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
        on_click=lambda e: handle()
    )
    btn_container = Row (
        controls=[quit_button,speak_btn],
        alignment=MainAxisAlignment.SPACE_AROUND
    )
    

    text_above_btn = Column(
        controls=[recognized_text,btn_container,recn_label],
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER
    )
    quit_button.visible = False
    speak_btn.visible = False

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
    image_box = Image(src_base64=b64_string, width=2000, height=500)
    image_box.visible = False


    def handle():
        print("here in the handle")
        nonlocal recording 
        recording = not recording
        
        if recording:
            print("THE TEXT IS STARTING TO RECORD")
            speak_btn.icon = icons.STOP_CIRCLE
            audio.start_recording(PATH)
        else: 
            print("THE TEXT IS STOPPING TO WORK")
            speak_btn.icon = icons.MIC
            audio.stop_recording()
            
            try:
                # Use a thread for transcription
                transcription_thread = threading.Thread(target=transcribe_np, daemon=True)
                transcription_thread.start()
            except Exception as e:
                print(f"Error during transcription: {e}")
            
        page.update() 
        print("Recording:", recording)


    def start_camera():


        global cap
        cap = cv2.VideoCapture(0)  
        time.sleep(1)

        threading.Thread(target=capture_frames, daemon=True).start()

    def capture_frames():
        global cap
        if cap.isOpened():
            image_box.visible = True  
            page.update()  

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    continue  

                frame = cv2.flip(frame, 1)  
                
                
                results = model(frame, device=device, show=False) 
                
            
                recognized_texts = []
                for result in results:
                   
                    if result.boxes is not None:  
                        for box in result.boxes:
                            class_id = int(box.cls)  
                            confidence = box.conf  

                            if confidence > 0.7:  
                                label = model.names[class_id]  
                                recognized_texts.append(label)  

                    frame = result.plot()  
                
                jpg_img = cv2.imencode(".jpg", frame)[1]
                b64_string = base64.b64encode(jpg_img).decode("utf-8")
                image_box.src_base64 = b64_string
                
                header.value = "Sign Language to Text"
                middle.value = "Hold your hands up and start signing. Your signs will be transmitted into text in real-time."
                recognized_text.value = ', '.join(recognized_texts)  # Update the displayed text
                button.visible = False
                quit_button.visible = True
                speak_btn.visible = True
                recn_label.visible = True
                page.update()  
                
                time.sleep(0.03)  


    
    def stop_camera():
        global cap
        if cap is not None:
            cap.release()  

        button.visible = True  
        quit_button.visible = False  
        speak_btn.visible = False
        image_box.visible = False
        recn_label.visible = False  
        header.value = "Turn the camera on to start translating"
        middle.value = "The camera is off by default. Once you turn it on, you'll see yourself and your surroundings in this area."
        recognized_text.value = ""  
        page.update()

    contain = Container(
        image_box,
        alignment=alignment.center,
        expand=True
    )
    page.overlay.append(audio)
    page.add(container, contain, text_above_btn)

threading.Thread(target=app(main),daemon=True).start()




