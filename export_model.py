import torch
import torch.nn as nn
from torchvision import models
import onnx

# 1. Definir y cargar modelo (lo de siempre)
model = models.resnet18()
model.fc = nn.Sequential(
    nn.Dropout(p=0.4),
    nn.Linear(model.fc.in_features, 256),
    nn.ReLU(),
    nn.Dropout(p=0.3),
    nn.Linear(256, 5),
)
model.load_state_dict(torch.load('best_model_ResNet18.pth', map_location='cpu'))
model.eval()

# 2. Exportar temporalmente
dummy_input = torch.randn(1, 3, 128, 128)
torch.onnx.export(
    model, dummy_input, "temp.onnx", 
    export_params=True, 
    opset_version=11,
    input_names=['input'], 
    output_names=['output']
)

# 3. EL TRUCO: Cargar y volver a guardar TODO en uno
# Esto obliga a ONNX a meter los datos externos dentro del archivo principal
modelo_cargado = onnx.load("temp.onnx")
onnx.save_model(modelo_cargado, "model.onnx", save_as_external_data=False)

print("✅ ¡HECHO! Comprueba el tamaño de 'model.onnx'. Debería pesar unos 44-45 MB.")