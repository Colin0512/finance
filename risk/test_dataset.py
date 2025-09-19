import os
import pandas as pd

# 打印当前工作目录
print(f"当前工作目录: {os.getcwd()}")

# 尝试不同的路径
paths = [
    os.path.join("Dataset", "bank.csv"),
    "Dataset/bank.csv",
    "Dataset\\bank.csv",
    "./Dataset/bank.csv",
    ".\\Dataset\\bank.csv"
]

# 检查每个路径
for path in paths:
    print(f"尝试路径: {path}")
    if os.path.exists(path):
        print(f"  文件存在!")
        try:
            # 尝试读取文件
            data = pd.read_csv(path)
            print(f"  成功读取文件，行数: {len(data)}")
            print(f"  前5行:\n{data.head()}")
            break
        except Exception as e:
            print(f"  读取文件失败: {str(e)}")
    else:
        print(f"  文件不存在")

# 如果以上路径都失败，尝试绝对路径
if not any(os.path.exists(p) for p in paths):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    abs_path = os.path.join(current_dir, "Dataset", "bank.csv")
    print(f"尝试绝对路径: {abs_path}")
    if os.path.exists(abs_path):
        print(f"  文件存在!")
        try:
            # 尝试读取文件
            data = pd.read_csv(abs_path)
            print(f"  成功读取文件，行数: {len(data)}")
            print(f"  前5行:\n{data.head()}")
        except Exception as e:
            print(f"  读取文件失败: {str(e)}")
    else:
        print(f"  文件不存在")
