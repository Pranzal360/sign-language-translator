from ultralytics import YOLO

model = YOLO("yolov8x.pt")

results = model(source=0, show=True)