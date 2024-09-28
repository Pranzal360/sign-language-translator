from ultralytics import YOLO

model = YOLO("last.pt")

image_path = "image.png"

results = model(source=0, show=True, save=True)

print(results)