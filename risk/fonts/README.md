# 字体文件说明

此目录包含应用程序使用的字体文件，主要用于确保matplotlib图表中能够正确显示中文字符。

## 包含的字体

- `SimHei.ttf` - 黑体，用于显示中文字符
- `SimSun.ttf` - 宋体，作为备选中文字体

## 使用方法

在代码中，可以通过以下方式使用这些字体：

```python
import os
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 获取字体文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(current_dir, 'fonts', 'SimHei.ttf')

# 创建字体属性对象
font_prop = FontProperties(fname=font_path)

# 在绘图时使用字体
plt.title('中文标题', fontproperties=font_prop)
```

## 注意事项

- 请确保在部署应用程序时，包含这些字体文件
- 如果字体文件无法加载，可能需要检查文件路径和权限
