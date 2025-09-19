Write-Host "正在启动家康智投系统..." -ForegroundColor Green
Start-Process -FilePath "python" -ArgumentList "-m", "streamlit", "run", "app.py"
Write-Host "应用程序已在新窗口中启动，请查看浏览器。" -ForegroundColor Green
Write-Host "您可以关闭此窗口，应用程序将继续运行。" -ForegroundColor Green
