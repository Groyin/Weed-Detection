import torch

# 检查CUDA是否可用
print(f"CUDA available: {torch.cuda.is_available()}")

# 检查CUDA版本
print(f"CUDA version: {torch.version.cuda}")

# 检查PyTorch是否识别到GPU
if torch.cuda.is_available():
    print(f"GPU name: {torch.cuda.get_device_name(0)}")

