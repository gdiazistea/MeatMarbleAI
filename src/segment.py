import cv2
import numpy as np
from PIL import Image
from segment_anything import sam_model_registry, SamPredictor
import torch

# --------- CONFIGURACIÓN ---------
image_path = "imgs/img1.jpg"
model_type = "vit_h"
sam_checkpoint = "sam_vit_h_4b8939.pth"
device = "cuda" if torch.cuda.is_available() else "cpu"

# --------- CARGAR MODELO SAM ---------
sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device)
predictor = SamPredictor(sam)

# --------- CARGAR IMAGEN ---------
image_bgr = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
predictor.set_image(image_rgb)
clone = image_bgr.copy()

# --------- VARIABLES GLOBALES ---------
clicked_points = []  # (x, y, clase)
class_names = {1: "Carne", 2: "Grasa"}
mask_combined = np.zeros(image_rgb.shape[:2], dtype=np.uint8)

# --------- CALLBACK DE MOUSE ---------
def click_event(event, x, y, flags, param):
    global clicked_points, mask_combined
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Seleccioná clase: 1 para carne, 2 para grasa")
        selected_class = int(input("Clase: "))
        if selected_class not in class_names:
            print("Clase inválida. Debe ser 1 o 2.")
            return
        print(f"Click en ({x},{y}) - Clase: {class_names[selected_class]}")
        clicked_points.append((x, y, selected_class))

        # Obtener máscara desde SAM
        input_point = np.array([[x, y]])
        input_label = np.array([1])  # 1 = foreground
        masks, scores, _ = predictor.predict(point_coords=input_point,
                                             point_labels=input_label,
                                             multimask_output=True)

        best_mask = masks[np.argmax(scores)]  # elegimos la mejor máscara
        best_mask = best_mask.astype(np.uint8)

        # Asignar valor de clase (1 o 2) a los píxeles donde hay 1 en la máscara
        mask_combined[best_mask == 1] = selected_class

        # Dibujar punto y texto en la imagen
        color = (0, 255, 0) if selected_class == 1 else (0, 0, 255)
        cv2.circle(image_bgr, (x, y), 5, color, -1)
        cv2.putText(image_bgr, class_names[selected_class], (x + 10, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)

# --------- EJECUTAR INTERFAZ ---------
cv2.namedWindow("Seleccioná puntos (ESC para salir)")
cv2.setMouseCallback("Seleccioná puntos (ESC para salir)", click_event)

while True:
    cv2.imshow("Seleccioná puntos (ESC para salir)", image_bgr)
    key = cv2.waitKey(1)
    if key == 27:  # ESC para salir
        break

cv2.destroyAllWindows()

# --------- GUARDAR MÁSCARA FINAL ---------
output_path = "masks/img1_mask_multiclase.png"
Image.fromarray(mask_combined).save(output_path)
print(f"Mascara multiclase guardada en: {output_path}")
