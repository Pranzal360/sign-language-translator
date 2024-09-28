import whisper
import time
import torch

# Load the Whisper model on GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("large").to(device)

# Measure execution time for transcription

start_time = time.time()
# Automatically detect the language and transcribe
result = model.transcribe("audio1.wav", language='ne')

# Measure end time
end_time = time.time()
execution_time = end_time - start_time

# Print detected language and transcription
print("Detected Language:", result['language'])
print("Transcription:", result['text'])
print(f"Execution Time: {execution_time:.2f} seconds")
