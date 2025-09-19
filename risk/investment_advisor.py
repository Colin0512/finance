import pandas as pd
import numpy as np

class InvestmentAdvisor:
    """
    投资建议模块，基于风险评估结果提供投资建议
    整合了Risk_Analysis_and_Investment_Recommendation_System的投资建议功能
    """
    
    def __init__(self):
        # 初始化投资建议映射
        self.investment_recommendations = {
            'High': {
                'name': '高风险投资组合',
                'description': '适合风险承受能力强、追求高回报的投资者',
                'products': [
                    {'name': '加密货币', 'allocation': 30, 'description': '比特币、以太坊等高波动性加密资产'},
                    {'name': '高波动性股票', 'allocation': 40, 'description': '成长型科技股、小盘股等高波动性股票'},
                    {'name': '杠杆ETF', 'allocation': 15, 'description': '提供2-3倍市场回报的杠杆型ETF'},
                    {'name': '期权/期货', 'allocation': 10, 'description': '金融衍生品，可提供高杠杆'},
                    {'name': '高收益债券', 'allocation': 5, 'description': '高收益但风险较高的债券'}
                ],
                'warning': '警告：此类投资具有高风险，可能导致本金大幅亏损。建议仅将可承受损失的资金用于此类投资。'
            },
            'Medium': {
                'name': '中等风险投资组合',
                'description': '平衡风险与回报，适合大多数投资者',
                'products': [
                    {'name': 'BIST30指数股票', 'allocation': 30, 'description': '土耳其30大蓝筹股，相对稳定'},
                    {'name': '混合型基金', 'allocation': 25, 'description': '股票与债券的平衡配置'},
                    {'name': '优质公司债', 'allocation': 20, 'description': '信用评级良好的企业债券'},
                    {'name': '房地产投资信托', 'allocation': 15, 'description': '投资商业地产的REITs'},
                    {'name': '黄金ETF', 'allocation': 10, 'description': '跟踪黄金价格的ETF，对冲通胀风险'}
                ],
                'warning': '注意：中等风险投资仍有可能在短期内出现波动，建议持有时间不少于3年。'
            },
            'Low': {
                'name': '低风险投资组合',
                'description': '追求资本保全，适合风险承受能力低的投资者',
                'products': [
                    {'name': '定期存款', 'allocation': 35, 'description': '银行定期存款，本金安全'},
                    {'name': '货币市场基金', 'allocation': 25, 'description': '投资短期高质量货币市场工具'},
                    {'name': '国债', 'allocation': 20, 'description': '政府发行的债券，安全性高'},
                    {'name': '短期债券基金', 'allocation': 15, 'description': '投资短期债券的基金产品'},
                    {'name': '高评级公司债', 'allocation': 5, 'description': 'AAA级企业债券'}
                ],
                'warning': '提示：低风险投资通常收益较低，可能无法跑赢通胀。'
            }
        }
    
    def get_investment_recommendation(self, risk_level):
        """
        根据风险等级获取投资建议
        
        参数:
        risk_level (str): 风险等级，可以是'High'、'Medium'或'Low'
        
        返回:
        dict: 包含投资建议的字典
        """
        # 将中文风险等级转换为英文
        risk_mapping = {
            '高风险': 'High',
            '中风险': 'Medium', 
            '低风险': 'Low',
            '高': 'High',
            '中': 'Medium',
            '低': 'Low',
            'Yüksek Risk': 'High',
            'Orta Risk': 'Medium',
            'Düşük Risk': 'Low'
        }
        
        # 如果输入的是中文风险等级，转换为英文
        if risk_level in risk_mapping:
            risk_level = risk_mapping[risk_level]
        
        # 确保风险等级有效
        if risk_level not in self.investment_recommendations:
            return {
                'name': '无法提供建议',
                'description': '无效的风险等级',
                'products': [],
                'warning': '请提供有效的风险等级（High、Medium或Low）'
            }
        
        return self.investment_recommendations[risk_level]
    
    def get_personalized_recommendation(self, risk_level, age=None, balance=None, has_loans=False):
        """
        获取个性化投资建议，考虑年龄、余额和贷款状况
        
        参数:
        risk_level (str): 风险等级
        age (int, optional): 年龄
        balance (float, optional): 账户余额
        has_loans (bool, optional): 是否有贷款
        
        返回:
        dict: 个性化投资建议
        """
        # 获取基础建议
        base_recommendation = self.get_investment_recommendation(risk_level)
        personalized = base_recommendation.copy()
        
        # 根据年龄调整
        if age is not None:
            if age > 60 and risk_level == 'High':
                # 老年人降低高风险投资比例
                personalized['warning'] += "\n考虑到您的年龄，建议降低高风险资产配置，增加稳健型资产比例。"
            elif age < 30 and risk_level == 'Low':
                # 年轻人可以考虑适当增加风险
                personalized['warning'] += "\n考虑到您的年轻年龄，可以适当增加一些成长型资产，提高长期回报潜力。"
        
        # 根据余额调整
        if balance is not None:
            if balance < 5000:
                personalized['warning'] += "\n考虑到您的账户余额较低，建议先建立应急基金，再考虑投资。"
            elif balance > 100000 and risk_level != 'Low':
                personalized['warning'] += "\n考虑到您的较高账户余额，建议适当分散投资，不要将所有资金投入单一市场或产品。"
        
        # 根据贷款状况调整
        if has_loans:
            personalized['warning'] += "\n您目前有贷款，建议优先考虑偿还高息贷款，再进行投资规划。"
        
        return personalized

# 测试代码
if __name__ == "__main__":
    advisor = InvestmentAdvisor()
    
    # 测试基础建议
    high_risk = advisor.get_investment_recommendation('High')
    print(f"高风险建议: {high_risk['name']}")
    print(f"产品数量: {len(high_risk['products'])}")
    
    # 测试个性化建议
    personalized = advisor.get_personalized_recommendation('Medium', age=65, balance=20000, has_loans=True)
    print(f"\n个性化建议: {personalized['name']}")
    print(f"警告信息: {personalized['warning']}")
