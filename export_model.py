import torch
import torch.nn as nn
from torchvision import models

# 1. Definir arquitectura idéntica
model = models.resnet18()
model.fc = nn.Sequential(
    nn.Dropout(p=0.4),
    nn.Linear(model.fc.in_features, 256),
    nn.ReLU(),
    nn.Dropout(p=0.3),
    nn.Linear(256, 5),
)

# 2. Cargar tus pesos
model.load_state_dict(torch.load('best_model_ResNet18.pth', map_location='cpu'))
model.eval()

# 3. Exportar
dummy_input = torch.randn(1, 3, 128, 128)
torch.onnx.export(model, dummy_input, "model.onnx", 
                  input_names=['input'], 
                  output_names=['output'],
                  dynamic_axes={'input': {0: 'batch_size'}})
print("¡Éxito! model.onnx generado.")