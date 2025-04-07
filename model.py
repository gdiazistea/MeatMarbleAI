import cv2
import numpy as np

# Cargar la imagen
image_path = 'imgs/marbling.jpg'
image = cv2.imread(image_path)

# Convertir la imagen a escala de grises
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Aplicar desenfoque para reducir el ruido
blurred_image = cv2.blur(gray_image, (3, 3))

# Detectar bordes usando Canny
canny_output = cv2.Canny(blurred_image, 100, 200)

# Encontrar contornos
contours, _ = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Calcular la envolvente convexa para cada contorno
hulls = [cv2.convexHull(contour) for contour in contours]

# Crear una imagen para dibujar los resultados
drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)

# Dibujar contornos y envolventes convexas
for i in range(len(contours)):
    color = (255, 0, 0)  # Color azul para los contornos
    cv2.drawContours(drawing, contours, i, color)
    color = (0, 255, 0)  # Color verde para las envolventes convexas
    cv2.drawContours(drawing, hulls, i, color)

# Mostrar la imagen resultante
cv2.imshow('Hull demo', drawing)
cv2.waitKey(0)
cv2.destroyAllWindows()