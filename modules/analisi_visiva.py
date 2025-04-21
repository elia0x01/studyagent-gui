import cv2
import os
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def estrai_e_descrivi_frame(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    intervallo = int(fps * 4)
    count, saved = 0, 0
    os.makedirs("frames", exist_ok=True)
    descrizioni = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if count % intervallo == 0:
            file_path = f"frames/frame_{saved:03}.jpg"
            cv2.imwrite(file_path, frame)
            image = Image.open(file_path).convert("RGB")
            inputs = processor(image, return_tensors="pt")
            out = model.generate(**inputs)
            caption = processor.decode(out[0], skip_special_tokens=True)
            descrizioni.append(f"Frame {saved:03}: {caption}")
            saved += 1
        count += 1
    cap.release()
    return "\n".join(descrizioni)
