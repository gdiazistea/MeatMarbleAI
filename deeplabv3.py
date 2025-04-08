import os
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from torchvision.models.segmentation import deeplabv3_resnet50
from PIL import Image
import matplotlib.pyplot as plt
import torch.nn.functional as F

# ---------------- CONFIGURACION ----------------
data_dir = "./dataset"
img_dir = os.path.join(data_dir, "imgs")
mask_dir = os.path.join(data_dir, "masks")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ---------------- DATASET PERSONALIZADO ----------------
class MeatSegmentationDataset(Dataset):
    def __init__(self, img_dir, mask_dir, transform=None):
        self.img_dir = img_dir
        self.mask_dir = mask_dir
        self.transform = transform
        self.img_names = sorted(os.listdir(img_dir))

    def __len__(self):
        return len(self.img_names)

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.img_names[idx])
        mask_path = os.path.join(self.mask_dir, self.img_names[idx].replace(".jpg", "_mask.png"))

        image = Image.open(img_path).convert("RGB")
        mask = Image.open(mask_path)

        image = image.resize((512, 512))
        mask = mask.resize((512, 512), resample=Image.NEAREST)

        image = transforms.ToTensor()(image)
        image = transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])(image)

        mask = np.array(mask).astype(np.int64)

        return image, torch.from_numpy(mask)

# ---------------- CARGA DE DATOS ----------------
train_dataset = MeatSegmentationDataset(img_dir, mask_dir)
train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True, num_workers=2)

# ---------------- MODELO ----------------
model = deeplabv3_resnet50(num_classes=3, pretrained=False)
model.to(device)

optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
criterion = torch.nn.CrossEntropyLoss()

# ---------------- ENTRENAMIENTO ----------------
epochs = 20
for epoch in range(epochs):
    model.train()
    total_loss = 0
    for images, masks in train_loader:
        images, masks = images.to(device), masks.to(device)

        outputs = model(images)['out']
        loss = criterion(outputs, masks)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(train_loader):.4f}")

# ---------------- VISUALIZACION ----------------
def decode_mask(mask):
    palette = np.array([[0, 0, 0], [255, 0, 0], [255, 255, 255]])
    color_mask = palette[mask]
    return color_mask

model.eval()
with torch.no_grad():
    for images, masks in train_loader:
        images = images.to(device)
        outputs = model(images)['out']
        preds = torch.argmax(outputs, dim=1).cpu().numpy()
        masks = masks.numpy()

        for i in range(min(2, len(images))):
            img = images[i].permute(1, 2, 0).cpu().numpy()
            img = (img * np.array([0.229, 0.224, 0.225])) + np.array([0.485, 0.456, 0.406])
            img = np.clip(img, 0, 1)

            plt.figure(figsize=(12, 4))
            plt.subplot(1, 3, 1)
            plt.imshow(img)
            plt.title("Imagen")
            plt.axis("off")

            plt.subplot(1, 3, 2)
            plt.imshow(decode_mask(masks[i]))
            plt.title("Máscara Real")
            plt.axis("off")

            plt.subplot(1, 3, 3)
            plt.imshow(decode_mask(preds[i]))
            plt.title("Predicción")
            plt.axis("off")

            plt.tight_layout()
            plt.show()
        break
