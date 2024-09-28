from flet import *

PATH = "audio.wav"

from speechR import audio_file

def main(page: Page):
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.vertical_alignment = MainAxisAlignment.CENTER


    def handle_state_change(e) :
        print("state changed : {e.data}")


    # Initial state
    recording = False

    audio = AudioRecorder(
        audio_encoder=AudioEncoder.WAV,
        on_state_changed=handle_state_change
    )


    btn = ElevatedButton(
        icon="mic",
        text="start recording",
        on_click=lambda e: handle()
    )

    def handle():
        nonlocal recording  # Use nonlocal to modify the outer variable
        recording = not recording  # Toggle the recording state
        
        if recording:
            btn.icon = "stop_circular"
            btn.text = "stop recording"
            audio.start_recording(PATH)

        else: 
            btn.icon = "mic"
            btn.text = "start recording"
            audio.stop_recording()
            result = audio_file(PATH)
            print(result)
        page.update()  # Update the page to reflect changes
        print("Recording:", recording)
    
    page.overlay.append(audio)

    page.add(btn)

app(main)
