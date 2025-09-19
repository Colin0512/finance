import os
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Union
import json

# 导入家康智投系统的核心模块
from risk_classifier import FamilyRiskClassifier
from investment_advisor import InvestmentAdvisor

# 导入新增的模块
from financial_data_provider import FinancialDataProvider
from ai_assistant import AIAssistant

class EnhancedRiskClassifier(FamilyRiskClassifier):
    """
    增强版风险分类器，整合AI能力和金融数据
    """
    
    def __init__(self, financial_api_key=None, ai_api_key=None, auto_init=True):
        """初始化增强版风险分类器"""
        # 初始化原始风险分类器
        super().__init__(auto_init=auto_init)
        
        # 初始化金融数据提供者
        self.financial_data = FinancialDataProvider(api_key=financial_api_key)
        
        # 初始化AI助手
        self.ai_assistant = AIAssistant(api_key=ai_api_key)
    
    def enhanced_risk_analysis(self, member_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        增强版风险分析，结合规则型分类、机器学习模型和AI分析
        
        参数:
        - member_data: 家庭成员数据
        
        返回:
        - 增强版风险分析结果
        """
        # 获取基础风险评估
        basic_risk = self.classify_risk_level(
            age=member_data.get('age', 35),
            balance=member_data.get('balance', 0),
            loan="yes" if member_data.get('loan', False) else "no",
            housing="yes" if member_data.get('housing', False) else "no",
            job=member_data.get('job', 'unknown'),
            marital=member_data.get('marital', 'unknown'),
            education=member_data.get('education', 'unknown')
        )
        
        # 使用AI进行深度风险分析
        ai_risk_analysis = self.ai_assistant.analyze_investment_risk(member_data)
        
        # 整合风险评估结果
        final_risk = {
            'rule_based': basic_risk['rule_based'],
            'decision_tree': basic_risk['decision_tree'],
            'random_forest': basic_risk['random_forest'],
            'ai_analysis': ai_risk_analysis.get('risk_level', basic_risk['random_forest']),
            'detailed_analysis': ai_risk_analysis.get('analysis', '')
        }
        
        # 如果提供了投资组合，进行组合分析
        if 'portfolio' in member_data and member_data['portfolio']:
            portfolio_analysis = self.analyze_portfolio(member_data['portfolio'])
            final_risk['portfolio_analysis'] = portfolio_analysis
        
        return final_risk
    
    def analyze_portfolio(self, portfolio: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        分析投资组合风险
        
        参数:
        - portfolio: 投资组合，包含多个资产信息
        
        返回:
        - 投资组合分析结果
        """
        # 获取投资组合中的股票数据
        stocks_data = []
        for item in portfolio:
            if 'ticker' in item:
                try:
                    # 获取股票价格数据
                    stock_data = self.financial_data.get_stock_prices(
                        ticker=item['ticker'],
                        start_date=item.get('start_date'),
                        end_date=item.get('end_date'),
                        interval="day",
                        interval_multiplier=1
                    )
                    
                    if 'error' not in stock_data:
                        stocks_data.append({
                            'ticker': item['ticker'],
                            'data': stock_data
                        })
                except Exception as e:
                    print(f"获取股票数据异常: {str(e)}")
        
        # 使用AI分析投资组合
        ai_portfolio_analysis = self.ai_assistant.analyze_portfolio(portfolio)
        
        # 返回分析结果
        return {
            'stocks_data': stocks_data,
            'ai_analysis': ai_portfolio_analysis.get('analysis', '')
        }


class EnhancedInvestmentAdvisor(InvestmentAdvisor):
    """
    增强版投资顾问，整合AI能力和金融数据
    """
    
    def __init__(self, financial_api_key=None, ai_api_key=None):
        """初始化增强版投资顾问"""
        # 初始化原始投资顾问
        super().__init__()
        
        # 初始化金融数据提供者
        self.financial_data = FinancialDataProvider(api_key=financial_api_key)
        
        # 初始化AI助手
        self.ai_assistant = AIAssistant(api_key=ai_api_key)
    
    def get_enhanced_recommendation(self, 
                                  risk_level: str, 
                                  age: Optional[int] = None,
                                  balance: Optional[float] = None,
                                  has_loans: bool = False,
                                  additional_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        获取增强版投资建议
        
        参数:
        - risk_level: 风险等级
        - age: 年龄
        - balance: 账户余额
        - has_loans: 是否有贷款
        - additional_data: 额外数据
        
        返回:
        - 增强版投资建议
        """
        # 获取基础投资建议
        base_recommendation = self.get_personalized_recommendation(
            risk_level=risk_level,
            age=age,
            balance=balance,
            has_loans=has_loans
        )
        
        # 获取市场数据
        market_data = self.get_market_data()
        
        # 构建用户数据
        user_data = {
            'age': age,
            'balance': balance,
            'has_loans': has_loans
        }
        
        if additional_data:
            user_data.update(additional_data)
        
        # 使用AI获取增强版投资建议
        ai_advice = self.ai_assistant.get_investment_advice(
            risk_level=risk_level,
            user_data=user_data,
            market_data=market_data
        )
        
        # 整合投资建议
        enhanced_recommendation = base_recommendation.copy()
        enhanced_recommendation['ai_advice'] = ai_advice.get('advice', '')
        enhanced_recommendation['market_data'] = market_data
        
        return enhanced_recommendation
    
    def get_market_data(self) -> Dict[str, Any]:
        """
        获取市场数据
        
        返回:
        - 市场数据
        """
        market_data = {}
        
        try:
            # 设置日期范围（过去30天）
            import datetime
            end_date = datetime.datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
            
            # 使用免费的API端点获取宏观数据
            # 获取主要指数数据
            indices = {}
            
            # 尝试获取宏观经济数据（免费）
            try:
                # 获取利率数据（免费API）
                interest_rates = self.financial_data.get_macro_data("interest_rates")
                if 'error' not in interest_rates:
                    indices['interest_rates'] = interest_rates
            except Exception as e:
                print(f"获取利率数据异常: {str(e)}")
            
            # 尝试获取GDP数据（免费API）
            try:
                gdp_data = self.financial_data.get_macro_data("gdp")
                if 'error' not in gdp_data:
                    indices['gdp'] = gdp_data
            except Exception as e:
                print(f"获取GDP数据异常: {str(e)}")
            
            # 尝试获取通胀数据（免费API）
            try:
                inflation_data = self.financial_data.get_macro_data("inflation")
                if 'error' not in inflation_data:
                    indices['inflation'] = inflation_data
            except Exception as e:
                print(f"获取通胀数据异常: {str(e)}")
            
            market_data['macro'] = indices
            
            # 获取公司概况数据（免费API）
            company_profiles = {}
            popular_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
            
            for ticker in popular_stocks:
                try:
                    profile_data = self.financial_data.get_company_profile(ticker)
                    if 'error' not in profile_data:
                        company_profiles[ticker] = profile_data
                except Exception as e:
                    print(f"获取{ticker}公司概况异常: {str(e)}")
            
            market_data['company_profiles'] = company_profiles
            
            # 获取收益数据（免费API）
            earnings_data = {}
            for ticker in popular_stocks:
                try:
                    earnings = self.financial_data.get_earnings(ticker)
                    if 'error' not in earnings:
                        earnings_data[ticker] = earnings
                except Exception as e:
                    print(f"获取{ticker}收益数据异常: {str(e)}")
            
            market_data['earnings'] = earnings_data
            
        except Exception as e:
            print(f"获取市场数据异常: {str(e)}")
        
        return market_data


class AIFinancialChatAssistant:
    """
    AI金融聊天助手，提供自然语言交互界面
    """
    
    def __init__(self, financial_api_key=None, ai_api_key=None):
        """初始化AI金融聊天助手"""
        # 初始化金融数据提供者
        self.financial_data = FinancialDataProvider(api_key=financial_api_key)
        
        # 初始化AI助手
        self.ai_assistant = AIAssistant(api_key=ai_api_key)
        
        # 初始化增强版风险分类器
        self.risk_classifier = EnhancedRiskClassifier(
            financial_api_key=financial_api_key,
            ai_api_key=ai_api_key,
            auto_init=True
        )
        
        # 初始化增强版投资顾问
        self.investment_advisor = EnhancedInvestmentAdvisor(
            financial_api_key=financial_api_key,
            ai_api_key=ai_api_key
        )
    
    def process_query(self, query: str, chat_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        处理用户查询
        
        参数:
        - query: 用户查询
        - chat_history: 聊天历史
        
        返回:
        - 处理结果
        """
        # 如果没有提供聊天历史，创建一个空列表
        if chat_history is None:
            chat_history = []
        
        # 将用户查询添加到聊天历史
        chat_history.append({"role": "user", "content": query})
        
        # 分解查询为子任务
        tasks = self.ai_assistant.decompose_query(query)
        
        # 执行任务
        task_results = []
        for task in tasks:
            result = self.execute_task(task, query)
            task_results.append({
                "task": task,
                "result": result
            })
        
        # 使用AI生成最终回复
        system_message = "你是一位专业的投资顾问，擅长解释复杂的金融概念和提供投资建议。请基于任务结果生成一个全面、专业的回复。"
        
        user_message = f"用户查询: {query}\n\n任务结果:\n"
        for i, task_result in enumerate(task_results):
            user_message += f"任务{i+1}: {task_result['task']}\n"
            user_message += f"结果: {json.dumps(task_result['result'], ensure_ascii=False)}\n\n"
        
        user_message += "请基于以上信息生成一个专业、全面的回复。"
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        
        response = self.ai_assistant.chat_completion(messages)
        
        # 提取回复内容
        if "error" in response:
            final_response = "抱歉，我无法处理您的请求。请稍后再试。"
        else:
            try:
                final_response = response["choices"][0]["message"]["content"]
            except Exception:
                final_response = "抱歉，处理您的请求时出现错误。"
        
        # 将助手回复添加到聊天历史
        chat_history.append({"role": "assistant", "content": final_response})
        
        return {
            "response": final_response,
            "tasks": tasks,
            "task_results": task_results,
            "chat_history": chat_history
        }
    
    def execute_task(self, task: str, query: str) -> Dict[str, Any]:
        """
        执行任务
        
        参数:
        - task: 任务描述
        - query: 原始查询
        
        返回:
        - 任务执行结果
        """
        # 提取可能的股票代码
        ticker = self.extract_ticker(query)
        
        # 根据任务类型执行不同的操作
        task_lower = task.lower()
        
        # 获取股票价格
        if "股价" in task_lower or "股票价格" in task_lower or "价格" in task_lower:
            if ticker:
                return self.financial_data.get_stock_prices(ticker)
            else:
                return {"error": "未找到股票代码"}
        
        # 获取财务报表
        elif "财务报表" in task_lower or "财报" in task_lower:
            if ticker:
                income = self.financial_data.get_financial_statements(ticker, statement_type="income")
                balance = self.financial_data.get_financial_statements(ticker, statement_type="balance")
                cashflow = self.financial_data.get_financial_statements(ticker, statement_type="cashflow")
                return {
                    "income_statement": income,
                    "balance_sheet": balance,
                    "cash_flow_statement": cashflow
                }
            else:
                return {"error": "未找到股票代码"}
        
        # 获取财务指标
        elif "财务指标" in task_lower or "指标" in task_lower or "比率" in task_lower:
            if ticker:
                return self.financial_data.get_financial_metrics(ticker)
            else:
                return {"error": "未找到股票代码"}
        
        # 获取市场数据
        elif "市场" in task_lower or "市场数据" in task_lower or "市场状况" in task_lower:
            return self.investment_advisor.get_market_data()
        
        # 获取投资建议
        elif "投资建议" in task_lower or "投资组合" in task_lower or "投资策略" in task_lower:
            # 提取可能的风险等级
            risk_level = self.extract_risk_level(query)
            
            return self.investment_advisor.get_enhanced_recommendation(
                risk_level=risk_level,
                additional_data={"query": query}
            )
        
        # 风险评估
        elif "风险评估" in task_lower or "风险分析" in task_lower:
            # 提取可能的用户数据
            user_data = self.extract_user_data(query)
            
            return self.risk_classifier.enhanced_risk_analysis(user_data)
        
        # 默认使用AI回答
        else:
            response = self.ai_assistant.chat_completion([
                {"role": "user", "content": f"关于'{task}'，请提供专业的分析和解答。原始查询：{query}"}
            ])
            
            if "error" in response:
                return {"error": "AI处理失败"}
            
            return {
                "ai_response": response["choices"][0]["message"]["content"]
            }
    
    def extract_ticker(self, text: str) -> Optional[str]:
        """
        从文本中提取股票代码
        
        参数:
        - text: 文本内容
        
        返回:
        - 股票代码或None
        """
        # 常见美股代码
        common_tickers = ["AAPL", "GOOGL", "MSFT", "AMZN", "META", "TSLA", "NVDA"]
        
        for ticker in common_tickers:
            if ticker in text.upper():
                return ticker
        
        # 如果没有找到常见代码，尝试使用AI提取
        response = self.ai_assistant.chat_completion([
            {"role": "system", "content": "你是一个股票代码提取器。请从用户文本中提取可能的股票代码，只返回代码本身，不要有任何其他文字。如果没有找到，返回'无'。"},
            {"role": "user", "content": text}
        ])
        
        if "error" not in response:
            extracted = response["choices"][0]["message"]["content"].strip()
            if extracted and extracted != "无":
                return extracted
        
        return None
    
    def extract_risk_level(self, text: str) -> str:
        """
        从文本中提取风险等级
        
        参数:
        - text: 文本内容
        
        返回:
        - 风险等级 (Low, Medium, High)
        """
        text_lower = text.lower()
        
        if "低风险" in text_lower or "保守" in text_lower:
            return "Low"
        elif "高风险" in text_lower or "激进" in text_lower:
            return "High"
        else:
            return "Medium"
    
    def extract_user_data(self, text: str) -> Dict[str, Any]:
        """
        从文本中提取用户数据
        
        参数:
        - text: 文本内容
        
        返回:
        - 用户数据
        """
        # 使用AI提取用户数据
        response = self.ai_assistant.chat_completion([
            {"role": "system", "content": "你是一个数据提取器。请从用户文本中提取可能的用户信息，包括年龄、职业、收入、资产等。以JSON格式返回，如：{\"age\": 30, \"job\": \"工程师\"}。如果某项信息不确定，则不要包含该字段。"},
            {"role": "user", "content": text}
        ])
        
        if "error" not in response:
            try:
                content = response["choices"][0]["message"]["content"]
                # 尝试从内容中提取JSON
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                    user_data = json.loads(json_str)
                    return user_data
            except Exception as e:
                print(f"提取用户数据异常: {str(e)}")
        
        # 如果提取失败，返回默认数据
        return {
            "age": 35,
            "balance": 10000,
            "job": "unknown"
        }


# 使用示例
if __name__ == "__main__":
    # 使用提供的API密钥初始化
    financial_api_key = "6b1d6fe9-833b-4071-8ac4-eadb1fc042c7"
    ai_api_key = "sk-f41ae42c0c7f4b9bbc8fd79ada481232"
    
    # 初始化AI金融聊天助手
    chat_assistant = AIFinancialChatAssistant(
        financial_api_key=financial_api_key,
        ai_api_key=ai_api_key
    )
    
    # 测试处理查询
    result = chat_assistant.process_query("我是一名35岁的工程师，月收入2万元，有10万存款，请推荐适合我的投资组合")
    print(f"AI回复: {result['response']}")
