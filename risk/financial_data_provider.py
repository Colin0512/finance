import requests
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any
import os

class FinancialDataProvider:
    """
    金融数据提供者，整合Financial Datasets API的功能
    用于获取股票价格、财务报表和市场数据
    """
    
    def __init__(self, api_key: str = None):
        """初始化金融数据提供者"""
        # 使用提供的API密钥或从环境变量获取
        self.api_key = api_key or os.environ.get("FINANCIAL_DATASETS_API_KEY")
        if not self.api_key:
            raise ValueError("Financial Datasets API密钥未提供")
        
        self.base_url = "https://api.financialdatasets.ai"
    
    def get_stock_prices(self, ticker: str, 
                        start_date: Optional[str] = None, 
                        end_date: Optional[str] = None,
                        interval: str = "day",
                        interval_multiplier: int = 1) -> Dict[str, Any]:
        """
        获取股票价格数据
        
        参数:
        - ticker: 股票代码
        - start_date: 开始日期 (YYYY-MM-DD)
        - end_date: 结束日期 (YYYY-MM-DD)
        - interval: 时间间隔 (second, minute, day, week, month, year)
        - interval_multiplier: 时间间隔乘数 (例如：1表示每天，5表示每5天)
        
        返回:
        - 包含股票价格数据的字典
        """
        # 构建请求参数
        params = {
            "ticker": ticker, 
            "interval": interval,
            "interval_multiplier": interval_multiplier
        }
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
            
        # 发送请求
        response = requests.get(
            f"{self.base_url}/prices/", 
            params=params,
            headers={"X-API-Key": self.api_key}
        )
        
        # 检查响应
        if response.status_code != 200:
            print(f"获取股票价格失败: {response.status_code}, {response.text}")
            return {"error": response.text, "status_code": response.status_code}
        
        # 返回数据
        return response.json()
    
    def get_stock_snapshot(self, ticker: str) -> Dict[str, Any]:
        """
        获取股票当前快照数据
        
        参数:
        - ticker: 股票代码
        
        返回:
        - 包含股票当前数据的字典
        """
        response = requests.get(
            f"{self.base_url}/prices/snapshot", 
            params={"ticker": ticker},
            headers={"X-API-Key": self.api_key}
        )
        
        if response.status_code != 200:
            print(f"获取股票快照失败: {response.status_code}, {response.text}")
            return {"error": response.text, "status_code": response.status_code}
        
        return response.json()
    
    def get_financial_statements(self, 
                               ticker: str, 
                               statement_type: str = "income", 
                               period: str = "annual",
                               limit: int = 5) -> Dict[str, Any]:
        """
        获取财务报表数据
        
        参数:
        - ticker: 股票代码
        - statement_type: 报表类型 (income, balance, cashflow)
        - period: 期间 (quarterly, annual, ttm)
        - limit: 返回的报表数量
        
        返回:
        - 包含财务报表数据的字典
        """
        # 映射报表类型到API端点
        endpoint_map = {
            "income": "income-statements",
            "balance": "balance-sheets",
            "cashflow": "cash-flow-statements"
        }
        
        endpoint = endpoint_map.get(statement_type)
        if not endpoint:
            return {"error": f"不支持的报表类型: {statement_type}"}
        
        # 构建请求参数
        params = {"ticker": ticker, "period": period, "limit": limit}
        
        # 发送请求
        response = requests.get(
            f"{self.base_url}/financials/{endpoint}/",
            params=params,
            headers={"X-API-Key": self.api_key}
        )
        
        # 检查响应
        if response.status_code != 200:
            print(f"获取财务报表失败: {response.status_code}, {response.text}")
            return {"error": response.text, "status_code": response.status_code}
        
        # 返回数据
        return response.json()
    
    def get_financial_metrics(self, 
                            ticker: str, 
                            period: str = "ttm",
                            limit: int = 5) -> Dict[str, Any]:
        """
        获取财务指标数据
        
        参数:
        - ticker: 股票代码
        - period: 期间 (quarterly, annual, ttm)
        - limit: 返回的指标数量
        
        返回:
        - 包含财务指标数据的字典
        """
        params = {"ticker": ticker, "period": period, "limit": limit}
        
        response = requests.get(
            f"{self.base_url}/financial-metrics/",
            params=params,
            headers={"X-API-Key": self.api_key}
        )
        
        if response.status_code != 200:
            print(f"获取财务指标失败: {response.status_code}, {response.text}")
            return {"error": response.text, "status_code": response.status_code}
        
        return response.json()
    
    def search_stocks(self, 
                     filters: List[Dict[str, Union[str, float]]],
                     period: str = "ttm",
                     limit: int = 10) -> Dict[str, Any]:
        """
        根据财务指标筛选股票
        
        参数:
        - filters: 筛选条件列表，如 [{"field": "revenue", "operator": "gt", "value": 1000000000}]
        - period: 期间 (quarterly, annual, ttm)
        - limit: 返回的股票数量
        
        返回:
        - 包含符合条件股票的字典
        """
        # 构建请求体
        body = {
            "filters": filters,
            "period": period,
            "limit": limit
        }
        
        # 发送请求
        response = requests.post(
            f"{self.base_url}/financials/search/",
            json=body,
            headers={
                "X-API-Key": self.api_key,
                "Content-Type": "application/json"
            }
        )
        
        # 检查响应
        if response.status_code != 200:
            print(f"搜索股票失败: {response.status_code}, {response.text}")
            return {"error": response.text, "status_code": response.status_code}
        
        # 返回数据
        return response.json()
    
    def get_news(self, ticker: str, limit: int = 5) -> Dict[str, Any]:
        """
        获取公司新闻
        
        参数:
        - ticker: 股票代码
        - limit: 返回的新闻数量
        
        返回:
        - 包含新闻数据的字典
        """
        response = requests.get(
            f"{self.base_url}/news/",
            params={"ticker": ticker, "limit": limit},
            headers={"X-API-Key": self.api_key}
        )
        
        if response.status_code != 200:
            print(f"获取新闻失败: {response.status_code}, {response.text}")
            return {"error": response.text, "status_code": response.status_code}
        
        return response.json()
        
    def get_macro_data(self, data_type: str, limit: int = 10) -> Dict[str, Any]:
        """
        获取宏观经济数据（免费API）
        
        参数:
        - data_type: 数据类型 (interest_rates, gdp, inflation)
        - limit: 返回的数据点数量
        
        返回:
        - 包含宏观经济数据的字典
        """
        # 映射数据类型到API端点
        endpoint_map = {
            "interest_rates": "macro/interest-rates",
            "gdp": "macro/gdp",
            "inflation": "macro/inflation",
            "unemployment": "macro/unemployment"
        }
        
        endpoint = endpoint_map.get(data_type)
        if not endpoint:
            return {"error": f"不支持的宏观数据类型: {data_type}"}
        
        # 构建请求参数
        params = {"limit": limit}
        
        # 发送请求
        response = requests.get(
            f"{self.base_url}/{endpoint}/",
            params=params,
            headers={"X-API-Key": self.api_key}
        )
        
        # 检查响应
        if response.status_code != 200:
            print(f"获取宏观数据失败: {response.status_code}, {response.text}")
            return {"error": response.text, "status_code": response.status_code}
        
        # 返回数据
        return response.json()
        
    def get_company_profile(self, ticker: str) -> Dict[str, Any]:
        """
        获取公司概况（免费API）
        
        参数:
        - ticker: 股票代码
        
        返回:
        - 包含公司概况的字典
        """
        response = requests.get(
            f"{self.base_url}/company/profile/",
            params={"ticker": ticker},
            headers={"X-API-Key": self.api_key}
        )
        
        if response.status_code != 200:
            print(f"获取公司概况失败: {response.status_code}, {response.text}")
            return {"error": response.text, "status_code": response.status_code}
        
        return response.json()
        
    def get_earnings(self, ticker: str, limit: int = 5) -> Dict[str, Any]:
        """
        获取公司收益数据（免费API）
        
        参数:
        - ticker: 股票代码
        - limit: 返回的收益报告数量
        
        返回:
        - 包含收益数据的字典
        """
        response = requests.get(
            f"{self.base_url}/company/earnings/",
            params={"ticker": ticker, "limit": limit},
            headers={"X-API-Key": self.api_key}
        )
        
        if response.status_code != 200:
            print(f"获取收益数据失败: {response.status_code}, {response.text}")
            return {"error": response.text, "status_code": response.status_code}
        
        return response.json()
    
    def to_dataframe(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        将API返回的数据转换为Pandas DataFrame
        
        参数:
        - data: API返回的数据
        
        返回:
        - Pandas DataFrame
        """
        if isinstance(data, dict) and "results" in data:
            return pd.DataFrame(data["results"])
        elif isinstance(data, list):
            return pd.DataFrame(data)
        else:
            print("无法转换为DataFrame，返回原始数据")
            return data


# 使用示例
if __name__ == "__main__":
    # 使用提供的API密钥初始化
    api_key = "6b1d6fe9-833b-4071-8ac4-eadb1fc042c7"
    financial_data = FinancialDataProvider(api_key)
    
    # 获取苹果公司股票价格
    aapl_prices = financial_data.get_stock_prices("AAPL", start_date="2023-01-01", end_date="2023-12-31")
    print(f"获取到苹果公司股价数据: {len(aapl_prices.get('results', []))}条记录")
    
    # 获取苹果公司财务报表
    aapl_income = financial_data.get_financial_statements("AAPL", statement_type="income", period="annual")
    print(f"获取到苹果公司财务报表: {len(aapl_income.get('results', []))}份")
