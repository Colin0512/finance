import streamlit as st

def setup_streamlit_config():
    """
    设置Streamlit配置，优化中文显示
    """
    # 设置页面配置
    st.set_page_config(
        page_title="家庭成员风险评估系统",
        page_icon="🏠",
        layout="wide"
    )
    
    # 自定义CSS，优化中文字体显示，添加Google Fonts中文字体
    st.markdown("""
    <style>
    /* 导入Google Noto Sans SC中文字体 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap');
    
    /* 设置全局字体 */
    html, body, [class*="css"] {
        font-family: 'Noto Sans SC', "Microsoft YaHei", "SimHei", "Arial Unicode MS", sans-serif !important;
    }
    
    /* 优化标题字体 */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Noto Sans SC', "Microsoft YaHei", "SimHei", "Arial Unicode MS", sans-serif !important;
        font-weight: bold;
    }
    
    /* 优化表格字体 */
    .dataframe {
        font-family: 'Noto Sans SC', "Microsoft YaHei", "SimHei", "Arial Unicode MS", sans-serif !important;
    }
    
    /* 优化按钮字体 */
    .stButton>button {
        font-family: 'Noto Sans SC', "Microsoft YaHei", "SimHei", "Arial Unicode MS", sans-serif !important;
    }
    
    /* 优化侧边栏字体 */
    .css-1d391kg, .css-1lcbmhc {
        font-family: 'Noto Sans SC', "Microsoft YaHei", "SimHei", "Arial Unicode MS", sans-serif !important;
    }
    
    /* 强制使用Noto Sans SC字体渲染SVG文本 */
    svg text {
        font-family: 'Noto Sans SC', sans-serif !important;
    }
    
    /* 确保matplotlib图表中的中文显示正常 */
    .matplotlib-figure text {
        font-family: 'Noto Sans SC', sans-serif !important;
    }
    </style>
    
    <!-- 预加载Noto Sans SC字体 -->
    <link rel="preload" href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC&display=swap"></noscript>
    """, unsafe_allow_html=True)
    
    return True