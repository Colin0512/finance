import os

# 确保模型目录存在
models_dir = os.path.join(os.path.dirname(__file__), 'models')
if not os.path.exists(models_dir):
    os.makedirs(models_dir)
