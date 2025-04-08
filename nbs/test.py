import cv2
import numpy as np
import torch
from segment_anything import sam_model_registry, SamPredictor

# Cargar imagen
image_path = '../imgs/marbling.jpg'  # <- Cambiá esto por la ruta real
image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Cargar modelo SAM
sam_checkpoint = "../checkpoints/sam_vit_h_4b8939.pth"  # <- Asegurate de tener este archivo
model_type = "vit_h"
device = "cuda" if torch.cuda.is_available() else "cpu"

sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device)
predictor = SamPredictor(sam)
predictor.set_image(image_rgb)

clicked_points = []

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_points.append((x, y))
        print(f"Click registrado en: ({x}, {y})")

cv2.imshow("Seleccionar carne y grasa", image)
cv2.setMouseCallback("Seleccionar carne y grasa", click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()

if len(clicked_points) < 2:
    raise ValueError("Necesitás al menos 2 clics: uno en carne, otro en grasa.")

input_points = np.array(clicked_points[:2])  # Primer clic = carne, segundo = grasa
input_labels = np.array([1, 1])  # 1 = foreground

masks, scores, logits = predictor.predict(
    point_coords=input_points,
    point_labels=input_labels,
    multimask_output=True
)

# Elegimos las dos mejores máscaras (una por cada clic)
mask_carne = masks[0]
mask_grasa = masks[1]

# Asegurar que no se superpongan
mask_grasa = np.logical_and(mask_grasa, np.logical_not(mask_carne))

mask_multiclass = np.zeros_like(mask_carne, dtype=np.uint8)
mask_multiclass[mask_carne] = 1
mask_multiclass[mask_grasa] = 2

import matplotlib.pyplot as plt

colors = {
    0: [0, 0, 0],       # fondo
    1: [0, 255, 0],     # carne
    2: [0, 255, 255]    # grasa
}

mask_rgb = np.zeros((*mask_multiclass.shape, 3), dtype=np.uint8)
for label, color in colors.items():
    mask_rgb[mask_multiclass == label] = color

plt.figure(figsize=(8, 8))
plt.imshow(mask_rgb)
plt.title("Máscara multicategoría")
plt.axis("off")
plt.show()
