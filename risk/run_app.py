import os
import subprocess
import sys
import time
import signal
import platform

def signal_handler(sig, frame):
    """处理信号，优雅地退出程序"""
    print("\n正在关闭应用程序，请稍候...")
    time.sleep(1)
    sys.exit(0)

def start_streamlit_detached():
    """以分离模式启动Streamlit应用"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(current_dir, "app.py")
    
    if platform.system() == "Windows":
        # Windows系统使用start命令启动新进程
        os.system(f'start "" {sys.executable} -m streamlit run {app_path}')
        print("应用程序已在新窗口中启动，请查看浏览器。")
        print("您可以关闭此终端窗口，应用程序将继续运行。")
    else:
        # Linux/Mac系统使用nohup命令
        os.system(f'nohup {sys.executable} -m streamlit run {app_path} > streamlit.log 2>&1 &')
        print("应用程序已在后台启动，请查看浏览器。")
        print("您可以关闭此终端窗口，应用程序将继续运行。")

def main():
    """启动家康智投系统"""
    print("正在启动家康智投系统...")
    
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 检查是否安装了streamlit
    try:
        import streamlit
        print("已检测到Streamlit安装")
    except ImportError:
        print("未检测到Streamlit，正在安装...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
        print("Streamlit安装完成")
    
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(current_dir, "app.py")
    
    # 询问用户选择启动模式
    print("\n请选择启动模式:")
    print("1. 常规模式 (在当前终端运行)")
    print("2. 后台模式 (在新窗口/后台运行)")
    
    choice = input("请输入选项 (1/2，默认为1): ").strip() or "1"
    
    if choice == "2":
        # 后台模式启动
        start_streamlit_detached()
    else:
        # 常规模式启动
        try:
            cmd = [sys.executable, "-m", "streamlit", "run", app_path]
            print("\n正在启动应用程序，请稍候...")
            print("提示: 按Ctrl+C可以停止应用程序")
            subprocess.run(cmd)
        except KeyboardInterrupt:
            print("\n检测到用户中断，正在关闭应用程序...")
        except Exception as e:
            print(f"\n启动应用程序时出错: {str(e)}")
        finally:
            print("应用程序已关闭。")

if __name__ == "__main__":
    main()
