#!/bin/bash

# Nombre del entorno virtual
ENV_NAME=".venv"

echo "🔧 Creando entorno virtual '$ENV_NAME'..."
python3 -m venv $ENV_NAME

echo "✅ Activando entorno..."
source $ENV_NAME/bin/activate

echo "📦 Actualizando pip..."
pip install --upgrade pip

echo "🚀 Instalando PyTorch (con soporte CUDA 11.8)..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

echo "🧰 Instalando librerías generales..."
pip install opencv-python matplotlib tqdm

echo "📥 Instalando Segment Anything (SAM)..."
pip install git+https://github.com/facebookresearch/segment-anything.git

echo "📁 Instalando dependencias de FoodSAM..."
cd FoodSAM
pip install -r requirement.txt
cd ..

echo "🧊 Guardando dependencias en 'requirements.txt'..."
pip freeze > requirements.txt

echo "📥 Descargando checkpoint SAM ViT-H..."
mkdir -p checkpoints
wget -O checkpoints/sam_vit_h.pth https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth

echo "✅ Entorno configurado con éxito."
echo "📌 Recordá correr 'source .venv/bin/activate' para activarlo cuando lo necesites."

