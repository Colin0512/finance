"""
测试家康智投系统的主要功能
"""
import os
from investment_advisor import InvestmentAdvisor
from risk_classifier import FamilyRiskClassifier

def test_investment_advisor():
    """测试投资顾问模块"""
    print("\n===== 测试投资顾问模块 =====")
    advisor = InvestmentAdvisor()
    
    # 测试基本建议功能
    high_risk = advisor.get_investment_recommendation('High')
    medium_risk = advisor.get_investment_recommendation('Medium')
    low_risk = advisor.get_investment_recommendation('Low')
    
    print(f"高风险建议: {high_risk['name']}")
    print(f"中风险建议: {medium_risk['name']}")
    print(f"低风险建议: {low_risk['name']}")
    
    # 测试个性化建议功能
    personalized = advisor.get_personalized_recommendation('Medium', age=65, balance=20000, has_loans=True)
    print(f"\n个性化建议: {personalized['name']}")
    print(f"警告信息: {personalized['warning']}")
    
    return True

def test_risk_classifier():
    """测试风险分类器模块"""
    print("\n===== 测试风险分类器模块 =====")
    classifier = FamilyRiskClassifier(auto_init=True)
    
    # 测试风险分类功能
    low_risk_member = {
        'age': 35,
        'balance': 5000,
        'loan': 'no',
        'housing': 'no',
        'job': 'technician',
        'marital': 'married',
        'education': 'tertiary'
    }
    
    medium_risk_member = {
        'age': 45,
        'balance': 500,
        'loan': 'no',
        'housing': 'no',
        'job': 'management',
        'marital': 'married',
        'education': 'tertiary'
    }
    
    high_risk_member = {
        'age': 25,
        'balance': -100,
        'loan': 'yes',
        'housing': 'yes',
        'job': 'student',
        'marital': 'single',
        'education': 'secondary'
    }
    
    low_risk = classifier.classify_risk_level(**low_risk_member)
    medium_risk = classifier.classify_risk_level(**medium_risk_member)
    high_risk = classifier.classify_risk_level(**high_risk_member)
    
    print(f"低风险成员评估结果: {low_risk['rule_based']}")
    print(f"中风险成员评估结果: {medium_risk['rule_based']}")
    print(f"高风险成员评估结果: {high_risk['rule_based']}")
    
    return True

def test_system_integration():
    """测试系统集成"""
    print("\n===== 测试系统集成 =====")
    
    # 创建分类器和投资顾问
    classifier = FamilyRiskClassifier(auto_init=True)
    advisor = InvestmentAdvisor()
    
    # 测试成员
    test_member = {
        'age': 30,
        'balance': 2000,
        'loan': 'no',
        'housing': 'yes',
        'job': 'technician',
        'marital': 'single',
        'education': 'tertiary'
    }
    
    # 获取风险评估
    risk = classifier.classify_risk_level(**test_member)
    print(f"风险评估结果: {risk['rule_based']}")
    
    # 获取投资建议
    investment_rec = advisor.get_personalized_recommendation(
        risk_level=risk['rule_based'],
        age=test_member['age'],
        balance=test_member['balance'],
        has_loans=(test_member['loan'] == 'yes' or test_member['housing'] == 'yes')
    )
    
    print(f"投资组合建议: {investment_rec['name']}")
    print(f"推荐产品数量: {len(investment_rec['products'])}")
    
    # 检查投资产品分配是否合理
    total_allocation = sum(p['allocation'] for p in investment_rec['products'])
    print(f"总资产分配比例: {total_allocation}%")
    
    return total_allocation == 100  # 检查总分配是否为100%

def main():
    """运行所有测试"""
    print("开始测试家康智投系统...")
    
    tests = [
        test_investment_advisor,
        test_risk_classifier,
        test_system_integration
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            if result:
                print(f"✅ {test.__name__} 测试通过")
            else:
                print(f"❌ {test.__name__} 测试失败")
        except Exception as e:
            print(f"❌ {test.__name__} 测试出错: {e}")
            results.append(False)
    
    # 总结测试结果
    success_count = results.count(True)
    total_count = len(results)
    print(f"\n测试完成: {success_count}/{total_count} 测试通过")
    
    if success_count == total_count:
        print("🎉 所有测试通过！系统功能正常。")
    else:
        print("⚠️ 部分测试失败，请检查系统功能。")

if __name__ == "__main__":
    main()
