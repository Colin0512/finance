import requests
import json
import os
from typing import Dict, List, Any, Optional, Union
import time

class AIAssistant:
    """
    AI助手模块，整合Deepseek API的功能
    用于提供智能投资建议和自然语言交互
    """
    
    def __init__(self, api_key: str = None):
        """初始化AI助手"""
        # 使用提供的API密钥或从环境变量获取
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("Deepseek API密钥未提供")
        
        self.base_url = "https://api.deepseek.com"
        self.model = "deepseek-chat"  # 默认模型
    
    def chat_completion(self, 
                      messages: List[Dict[str, str]], 
                      temperature: float = 0.7,
                      max_tokens: int = 1000) -> Dict[str, Any]:
        """
        获取AI聊天回复
        
        参数:
        - messages: 消息列表，格式为 [{"role": "user", "content": "你好"}]
        - temperature: 温度参数，控制随机性
        - max_tokens: 最大生成令牌数
        
        返回:
        - AI回复内容
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code != 200:
                print(f"AI聊天请求失败: {response.status_code}, {response.text}")
                return {"error": response.text, "status_code": response.status_code}
            
            return response.json()
        except Exception as e:
            print(f"AI聊天请求异常: {str(e)}")
            return {"error": str(e)}
    
    def analyze_investment_risk(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析投资风险
        
        参数:
        - user_data: 用户数据，包括年龄、收入、资产等信息
        
        返回:
        - 风险分析结果
        """
        # 构建消息
        messages = [
            {"role": "system", "content": "你是一位专业的投资顾问，擅长风险评估和投资组合分析。"},
            {"role": "user", "content": f"请分析以下用户的投资风险状况:\n{json.dumps(user_data, ensure_ascii=False, indent=2)}\n请提供风险等级评估（低、中、高）和详细的风险分析。"}
        ]
        
        # 获取AI回复
        response = self.chat_completion(messages)
        
        # 提取回复内容
        if "error" in response:
            return {"error": response["error"]}
        
        try:
            content = response["choices"][0]["message"]["content"]
            
            # 尝试提取风险等级
            risk_level = None
            if "低风险" in content or "风险等级：低" in content or "风险评级：低" in content:
                risk_level = "Low"
            elif "中风险" in content or "风险等级：中" in content or "风险评级：中" in content:
                risk_level = "Medium"
            elif "高风险" in content or "风险等级：高" in content or "风险评级：高" in content:
                risk_level = "High"
            
            return {
                "risk_level": risk_level,
                "analysis": content
            }
        except Exception as e:
            print(f"解析AI回复异常: {str(e)}")
            return {"error": str(e)}
    
    def get_investment_advice(self, 
                            risk_level: str, 
                            user_data: Dict[str, Any],
                            market_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        获取投资建议
        
        参数:
        - risk_level: 风险等级 (Low, Medium, High)
        - user_data: 用户数据
        - market_data: 市场数据（可选）
        
        返回:
        - 投资建议
        """
        # 构建消息
        system_message = "你是一位专业的投资顾问，擅长根据用户风险偏好和市场状况提供个性化投资建议。"
        
        user_message = f"请为以下风险等级和用户数据提供详细的投资建议：\n"
        user_message += f"风险等级: {risk_level}\n"
        user_message += f"用户数据: {json.dumps(user_data, ensure_ascii=False, indent=2)}\n"
        
        if market_data:
            user_message += f"市场数据: {json.dumps(market_data, ensure_ascii=False, indent=2)}\n"
        
        user_message += "\n请提供以下内容：\n"
        user_message += "1. 资产配置方案（各类资产的比例）\n"
        user_message += "2. 具体投资产品推荐\n"
        user_message += "3. 投资策略和注意事项\n"
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        
        # 获取AI回复
        response = self.chat_completion(messages, temperature=0.5, max_tokens=1500)
        
        # 提取回复内容
        if "error" in response:
            return {"error": response["error"]}
        
        try:
            content = response["choices"][0]["message"]["content"]
            return {
                "advice": content
            }
        except Exception as e:
            print(f"解析AI回复异常: {str(e)}")
            return {"error": str(e)}
    
    def analyze_portfolio(self, portfolio: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        分析投资组合
        
        参数:
        - portfolio: 投资组合，包含多个资产信息
        
        返回:
        - 投资组合分析结果
        """
        # 构建消息
        messages = [
            {"role": "system", "content": "你是一位专业的投资组合分析师，擅长评估投资组合的风险和收益特性。"},
            {"role": "user", "content": f"请分析以下投资组合:\n{json.dumps(portfolio, ensure_ascii=False, indent=2)}\n请评估组合的风险水平、多样化程度、预期收益，并提供优化建议。"}
        ]
        
        # 获取AI回复
        response = self.chat_completion(messages, temperature=0.3, max_tokens=1500)
        
        # 提取回复内容
        if "error" in response:
            return {"error": response["error"]}
        
        try:
            content = response["choices"][0]["message"]["content"]
            return {
                "analysis": content
            }
        except Exception as e:
            print(f"解析AI回复异常: {str(e)}")
            return {"error": str(e)}
    
    def decompose_query(self, query: str) -> List[str]:
        """
        将用户查询分解为子任务
        
        参数:
        - query: 用户查询
        
        返回:
        - 子任务列表
        """
        # 构建消息
        messages = [
            {"role": "system", "content": "你是一位金融分析助手，擅长将复杂的投资问题分解为简单的子任务。"},
            {"role": "user", "content": f"请将以下投资查询分解为2-3个具体的子任务：\n\"{query}\"\n请直接列出子任务，每行一个，不要有编号或其他格式。"}
        ]
        
        # 获取AI回复
        response = self.chat_completion(messages, temperature=0.3, max_tokens=500)
        
        # 提取回复内容
        if "error" in response:
            print(f"分解查询失败: {response['error']}")
            return ["分析用户需求", "提供投资建议"]
        
        try:
            content = response["choices"][0]["message"]["content"]
            # 分割内容为任务列表
            tasks = [task.strip() for task in content.split("\n") if task.strip()]
            return tasks
        except Exception as e:
            print(f"解析AI回复异常: {str(e)}")
            return ["分析用户需求", "提供投资建议"]


# 使用示例
if __name__ == "__main__":
    # 使用提供的API密钥初始化
    api_key = "sk-f41ae42c0c7f4b9bbc8fd79ada481232"
    ai_assistant = AIAssistant(api_key)
    
    # 测试聊天功能
    response = ai_assistant.chat_completion([
        {"role": "user", "content": "什么是指数基金？"}
    ])
    
    if "error" not in response:
        print(f"AI回复: {response['choices'][0]['message']['content']}")
    else:
        print(f"请求失败: {response['error']}")
