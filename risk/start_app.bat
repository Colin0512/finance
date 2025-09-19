@echo off
echo 正在启动家康智投系统...
start "家康智投系统" python -m streamlit run app.py
echo 应用程序已在新窗口中启动，请查看浏览器。
echo 您可以关闭此窗口，应用程序将继续运行。
