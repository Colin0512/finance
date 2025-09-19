import requests
import json
import sys

def test_deepseek_api():
    """测试Deepseek API连接"""
    api_key = "sk-f41ae42c0c7f4b9bbc8fd79ada481232"
    base_url = "https://api.deepseek.com"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": "你好"}],
        "temperature": 0.7,
        "max_tokens": 100
    }
    
    try:
        print("正在测试Deepseek API连接...")
        response = requests.post(
            f"{base_url}/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=10
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            print("API连接成功!")
        else:
            print(f"API连接失败: {response.status_code}")
            
    except Exception as e:
        print(f"请求异常: {str(e)}")

def test_financial_api():
    """测试Financial Datasets API连接"""
    api_key = "6b1d6fe9-833b-4071-8ac4-eadb1fc042c7"
    base_url = "https://api.financialdatasets.ai"
    
    headers = {
        "X-API-Key": api_key
    }
    
    try:
        print("\n正在测试Financial Datasets API连接...")
        response = requests.get(
            f"{base_url}/prices/snapshot",
            params={"ticker": "AAPL"},
            headers=headers,
            timeout=10
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text[:200]}...")  # 只显示前200个字符
        
        if response.status_code == 200:
            print("API连接成功!")
        else:
            print(f"API连接失败: {response.status_code}")
            
    except Exception as e:
        print(f"请求异常: {str(e)}")

if __name__ == "__main__":
    print("API连接测试工具")
    print("=" * 50)
    
    test_deepseek_api()
    test_financial_api()
