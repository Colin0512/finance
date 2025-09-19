import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import sys
import numpy as np

def setup_chinese_fonts():
    """
    设置matplotlib中文字体支持
    """
    # 设置通用备用字体（适用于云环境）
    plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'Noto Sans CJK JP', 
                                      'SimHei', 'Microsoft YaHei', 'SimSun', 
                                      'DejaVu Sans', 'Arial Unicode MS', 
                                      'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    
    # 检查系统中文字体
    font_paths = []
    
    # Windows系统字体路径
    if sys.platform.startswith('win'):
        font_paths.append(os.path.join(os.environ['WINDIR'], 'Fonts'))
        chinese_fonts = ['SimHei', 'Microsoft YaHei', 'SimSun', 'FangSong', 'KaiTi', 'NSimSun', 
                         'Microsoft JhengHei', 'DengXian', 'DFKai-SB']
    
    # Linux系统字体路径
    elif sys.platform.startswith('linux'):
        font_paths.extend(['/usr/share/fonts', '/usr/local/share/fonts', os.path.expanduser('~/.fonts')])
        chinese_fonts = ['WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'AR PL UMing CN', 
                         'Noto Sans CJK SC', 'Noto Sans CJK TC', 'Noto Sans CJK JP']
    
    # macOS系统字体路径
    elif sys.platform == 'darwin':
        font_paths.append('/Library/Fonts')
        font_paths.append('/System/Library/Fonts')
        font_paths.append(os.path.expanduser('~/Library/Fonts'))
        chinese_fonts = ['PingFang SC', 'Heiti SC', 'STHeiti', 'STSong', 'Hiragino Sans GB', 
                         'Apple LiGothic', 'Apple LiSung']
    
    # 查找可用的中文字体
    available_fonts = []
    for font_path in font_paths:
        if os.path.exists(font_path):
            for font in fm.findSystemFonts(font_path):
                try:
                    font_name = fm.FontProperties(fname=font).get_name()
                    if any(chinese_font in font_name for chinese_font in chinese_fonts):
                        available_fonts.append(font)
                except:
                    continue
    
    # 设置找到的第一个中文字体
    if available_fonts:
        # 优先选择黑体或雅黑字体
        preferred_fonts = [f for f in available_fonts if 'SimHei' in fm.FontProperties(fname=f).get_name() 
                          or 'YaHei' in fm.FontProperties(fname=f).get_name()]
        
        if preferred_fonts:
            selected_font = preferred_fonts[0]
        else:
            selected_font = available_fonts[0]
            
        # 设置matplotlib字体
        plt.rcParams['font.family'] = fm.FontProperties(fname=selected_font).get_name()
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        
        # 设置seaborn字体
        try:
            import seaborn as sns
            sns.set(font=fm.FontProperties(fname=selected_font).get_name())
        except:
            pass
            
        print(f"已设置中文字体: {fm.FontProperties(fname=selected_font).get_name()}")
        return True
    else:
        print("未找到本地中文字体，使用备用字体")
        return True

if __name__ == "__main__":
    setup_chinese_fonts()