import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import json
import time
from typing import Dict, List, Any, Optional, Union

# 导入原有模块
from risk_classifier import FamilyRiskClassifier
from investment_advisor import InvestmentAdvisor
from matplotlib_chinese import setup_chinese_fonts
from streamlit_config import setup_streamlit_config

# 导入新增模块
from financial_data_provider import FinancialDataProvider
from ai_assistant import AIAssistant
from financial_integration import EnhancedRiskClassifier, EnhancedInvestmentAdvisor, AIFinancialChatAssistant

# 设置中文字体
setup_chinese_fonts()

# 设置Streamlit配置
setup_streamlit_config()

# 强制设置matplotlib字体，确保中文显示正常
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.font_manager import FontProperties

# 尝试加载Google Noto Sans字体
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'Noto Sans CJK JP', 'SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# 使用Streamlit原生图表功能，不需要自定义字体

# API密钥
FINANCIAL_API_KEY = "6b1d6fe9-833b-4071-8ac4-eadb1fc042c7"
AI_API_KEY = "sk-f41ae42c0c7f4b9bbc8fd79ada481232"

# 初始化分类器
@st.cache_resource
def load_classifier():
    # 使用增强版风险分类器
    classifier = EnhancedRiskClassifier(
        financial_api_key=FINANCIAL_API_KEY,
        ai_api_key=AI_API_KEY,
        auto_init=True
    )
    # 尝试加载已有模型
    loaded = classifier.load_models()
    if not loaded:
        st.info("系统将使用规则型分类逻辑进行风险评估，您也可以在'模型训练'页面训练机器学习模型以提高准确率。")
    else:
        st.success("已加载预训练模型")
    return classifier

# 初始化投资顾问
@st.cache_resource
def load_investment_advisor():
    # 使用增强版投资顾问
    return EnhancedInvestmentAdvisor(
        financial_api_key=FINANCIAL_API_KEY,
        ai_api_key=AI_API_KEY
    )

# 初始化AI金融聊天助手
@st.cache_resource
def load_chat_assistant():
    return AIFinancialChatAssistant(
        financial_api_key=FINANCIAL_API_KEY,
        ai_api_key=AI_API_KEY
    )

classifier = load_classifier()
investment_advisor = load_investment_advisor()
chat_assistant = load_chat_assistant()

# 侧边栏
st.sidebar.title("家康智投系统")
st.sidebar.image("https://img.icons8.com/color/96/000000/investment-portfolio.png", width=100)

# 主页面
page = st.sidebar.radio("选择功能", ["首页", "模型训练", "风险评估", "投资建议", "家庭投资组合", "AI投资助手", "市场数据"])

# 首页
if page == "首页":
    st.title("🏠 家康智投系统")
    st.markdown("""
    ### 系统功能
    本系统基于机器学习算法和人工智能，对家庭成员的财务风险进行评估，并提供个性化投资建议。
    
    #### 主要功能:
    - **风险评估**: 评估家庭成员财务风险，结合AI深度分析
    - **投资建议**: 根据风险等级提供个性化投资建议，整合实时市场数据
    - **家庭投资组合**: 查看整个家庭的风险分布和投资组合
    - **AI投资助手**: 通过自然语言对话获取投资建议和市场分析
    - **市场数据**: 查看实时股票价格、财务报表和市场指标
    - **模型训练**: 可选项，训练机器学习模型提高准确率
    
    #### 风险等级与投资策略:
    - 🔴 **高风险 (High)**: 适合追求高回报的积极型投资策略
    - 🟠 **中风险 (Medium)**: 适合平衡型投资策略
    - 🟢 **低风险 (Low)**: 适合保守型投资策略
    
    #### 使用方法:
    1. 在"风险评估"页面评估家庭成员风险等级
    2. 在"投资建议"页面获取个性化投资建议
    3. 在"家庭投资组合"页面查看整体风险分布和投资组合
    4. 在"AI投资助手"页面通过聊天获取专业投资建议
    5. 在"市场数据"页面查看实时股票和市场信息
    6. 可选：在"模型训练"页面训练机器学习模型以提高准确率
    
    #### 新增功能:
    - **AI驱动分析**: 使用先进的AI模型提供更深入的风险评估和投资建议
    - **实时市场数据**: 整合Financial Datasets API，提供实时股票和市场数据
    - **自然语言交互**: 通过聊天界面获取投资建议和市场分析
    """)

# 模型训练页面
elif page == "模型训练":
    st.title("🧠 模型训练")
    
    st.info("注意：系统默认使用规则型分类逻辑进行风险评估，训练机器学习模型可以提高评估准确率，但不是必需的。")
    
    # 使用简单的相对路径查找数据集
    dataset_path = os.path.join("Dataset", "bank.csv")
    
    # 检查数据集是否存在
    dataset_found = os.path.exists(dataset_path)
    
    if dataset_found:
        
        # 加载并显示数据集预览
        data = pd.read_csv(dataset_path, sep=',')
        st.subheader("数据集预览")
        st.dataframe(data.head())
        
        # 数据集信息
        st.subheader("数据集信息")
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"数据集大小: {data.shape[0]} 行 x {data.shape[1]} 列")
        with col2:
            st.info(f"特征: {', '.join(data.columns.tolist())}")
        
        # 训练模型
        if st.button("训练风险分类模型", type="primary"):
            with st.spinner("正在训练模型，请稍候..."):
                features = ['age', 'job', 'marital', 'education', 'balance', 'housing', 'loan']
                data_subset = data[features]
                
                results = classifier.train(data_subset)
                
                # 显示训练结果
                st.success("模型训练完成！")
                
                # 显示准确率
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("决策树准确率", f"{results['dt_accuracy']:.2%}")
                with col2:
                    st.metric("随机森林准确率", f"{results['rf_accuracy']:.2%}")
                
                # 显示分类报告
                st.subheader("决策树模型评估")
                dt_report = pd.DataFrame(results['dt_report']).transpose()
                st.dataframe(dt_report)
                
                st.subheader("随机森林模型评估")
                rf_report = pd.DataFrame(results['rf_report']).transpose()
                st.dataframe(rf_report)
    else:
        st.error("未找到数据集: Dataset/bank.csv")
        st.info("请确保数据集文件位于正确的路径，或者手动上传数据集")
        
        # 添加上传数据集的选项
        uploaded_file = st.file_uploader("上传CSV数据集", type=['csv'])
        if uploaded_file is not None:
            # 保存上传的文件
            try:
                # 确保Dataset目录存在
                os.makedirs("Dataset", exist_ok=True)
                
                # 保存文件
                with open(os.path.join("Dataset", "bank.csv"), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                st.success("数据集已成功上传！请刷新页面以加载数据集。")
                # 刷新页面
                st.experimental_rerun()
            except Exception as e:
                st.error(f"保存文件时出错: {str(e)}")

# 风险评估页面
elif page == "风险评估":
    st.title("👤 风险评估")
    
    # 创建表单
    with st.form("risk_assessment_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("姓名", "家庭成员")
            age = st.number_input("年龄", min_value=18, max_value=100, value=35)
            job = st.selectbox(
                "职业",
                options=["管理层", "技术人员", "企业家", "蓝领工人", "退休", "自雇", "服务业", "学生", "失业", "其他"],
                index=0
            )
            marital = st.selectbox(
                "婚姻状况",
                options=["已婚", "单身", "离异"],
                index=0
            )
        
        with col2:
            education = st.selectbox(
                "教育程度",
                options=["小学", "中学", "高等教育", "未知"],
                index=2
            )
            balance = st.number_input("账户余额", value=1000)
            housing = st.selectbox(
                "是否有住房贷款",
                options=["是", "否"],
                index=1
            )
            loan = st.selectbox(
                "是否有个人贷款",
                options=["是", "否"],
                index=1
            )
        
        submit = st.form_submit_button("评估风险")
    
    # 处理表单提交
    if submit:
        # 映射选项到英文
        job_map = {
            "管理层": "management", "技术人员": "technician", "企业家": "entrepreneur",
            "蓝领工人": "blue-collar", "退休": "retired", "自雇": "self-employed",
            "服务业": "services", "学生": "student", "失业": "unemployed", "其他": "unknown"
        }
        
        marital_map = {"已婚": "married", "单身": "single", "离异": "divorced"}
        education_map = {"小学": "primary", "中学": "secondary", "高等教育": "tertiary", "未知": "unknown"}
        
        # 构建成员数据
        member_data = {
            'name': name,
            'age': age,
            'balance': balance,
            'loan': loan == "是",
            'housing': housing == "是",
            'job': job_map[job],
            'marital': marital_map[marital],
            'education': education_map[education]
        }
        
        # 使用增强版风险分析 - 添加详细进度指示器
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # 第一阶段：初始化
        status_text.text("正在初始化风险分析...")
        progress_bar.progress(10)
        time.sleep(0.5)  # 短暂延迟以显示进度
        
        # 第二阶段：基础风险评估
        status_text.text("正在进行基础风险评估...")
        progress_bar.progress(30)
        basic_risk = classifier.classify_risk_level(
            age=member_data.get('age', 35),
            balance=member_data.get('balance', 0),
            loan="yes" if member_data.get('loan', False) else "no",
            housing="yes" if member_data.get('housing', False) else "no",
            job=member_data.get('job', 'unknown'),
            marital=member_data.get('marital', 'unknown'),
            education=member_data.get('education', 'unknown')
        )
        
        # 显示初步结果
        progress_bar.progress(50)
        status_text.text("基础评估完成，正在进行AI深度分析...")
        
        # 第三阶段：AI深度分析
        with st.expander("查看初步评估结果", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                risk_color = "🔴" if basic_risk['rule_based'] == "High" else "🟠" if basic_risk['rule_based'] == "Medium" else "🟢"
                st.info(f"规则型评估: {risk_color} {basic_risk['rule_based']}")
            with col2:
                risk_color = "🔴" if basic_risk['random_forest'] == "High" else "🟠" if basic_risk['random_forest'] == "Medium" else "🟢"
                st.info(f"模型评估: {risk_color} {basic_risk['random_forest']}")
        
        # 添加跳过选项
        skip_ai = st.checkbox("跳过AI深度分析（加快处理速度）")
        
        if skip_ai:
            # 如果用户选择跳过AI分析
            progress_bar.progress(100)
            status_text.text("分析完成！")
            risk = basic_risk
        else:
            # 继续AI深度分析
            progress_bar.progress(70)
            status_text.text("AI正在进行深度风险分析...")
            ai_risk_analysis = classifier.ai_assistant.analyze_investment_risk(member_data)
            progress_bar.progress(90)
            status_text.text("正在整合分析结果...")
            
            # 整合所有结果
            risk = {
                'rule_based': basic_risk['rule_based'],
                'decision_tree': basic_risk['decision_tree'],
                'random_forest': basic_risk['random_forest'],
                'ai_analysis': ai_risk_analysis.get('risk_level', basic_risk['random_forest']),
                'detailed_analysis': ai_risk_analysis.get('analysis', '')
            }
            
            progress_bar.progress(100)
            status_text.text("分析完成！")
        
        # 确定最终风险等级 (使用随机森林模型结果，因为它通常最准确)
        final_risk = risk['random_forest']
        
        # 显示风险评估结果
        st.subheader(f"{name}的风险评估结果")
        
        # 使用列显示不同模型的结果
        col1, col2, col3 = st.columns(3)
        
        with col1:
            risk_color = "🔴" if risk['rule_based'] == "High" else "🟠" if risk['rule_based'] == "Medium" else "🟢"
            st.info(f"规则型评估: {risk_color} {risk['rule_based']}")
        
        with col2:
            risk_color = "🔴" if risk['decision_tree'] == "High" else "🟠" if risk['decision_tree'] == "Medium" else "🟢"
            st.info(f"决策树评估: {risk_color} {risk['decision_tree']}")
        
        with col3:
            risk_color = "🔴" if risk['random_forest'] == "High" else "🟠" if risk['random_forest'] == "Medium" else "🟢"
            st.info(f"随机森林评估: {risk_color} {risk['random_forest']}")
        
        # 风险解释
        st.subheader("风险解释")
        if final_risk == "High":
            st.warning("高风险: 账户余额为负或同时拥有住房贷款和个人贷款")
        elif final_risk == "Medium":
            st.info("中风险: 账户余额在0-1000之间")
        else:
            st.success("低风险: 账户余额大于1000且贷款状况良好")
            
        # 显示AI分析结果
        if 'ai_analysis' in risk:
            st.subheader("AI风险分析")
            
            # 显示AI风险等级
            ai_risk = risk['ai_analysis']
            risk_color = "🔴" if ai_risk == "High" else "🟠" if ai_risk == "Medium" else "🟢"
            st.info(f"AI风险评估: {risk_color} {ai_risk}")
            
            # 显示详细分析
            if 'detailed_analysis' in risk and risk['detailed_analysis']:
                with st.expander("查看详细分析", expanded=True):
                    st.markdown(risk['detailed_analysis'])
                    
        # 显示投资组合分析（如果有）
        if 'portfolio_analysis' in risk and risk['portfolio_analysis']:
            st.subheader("投资组合分析")
            with st.expander("查看投资组合分析"):
                st.markdown(risk['portfolio_analysis'].get('ai_analysis', '暂无投资组合分析'))
        
        # 保存到会话状态
        if 'family_members' not in st.session_state:
            st.session_state.family_members = []
        
        # 检查是否已存在相同姓名的成员
        existing_names = [member['name'] for member in st.session_state.family_members]
        if name in existing_names:
            # 更新现有成员
            for i, member in enumerate(st.session_state.family_members):
                if member['name'] == name:
                    # 保留原有的投资相关信息（如果有的话）
                    investment_portfolio = member.get('investment_portfolio', None)
                    monthly_savings = member.get('monthly_savings', 0)
                    investment_horizon = member.get('investment_horizon', None)
                    investment_goal = member.get('investment_goal', None)
                    
                    st.session_state.family_members[i] = {
                        'name': name,
                        'age': age,
                        'balance': balance,
                        'risk_rule': risk['rule_based'],
                        'risk_dt': risk['decision_tree'],
                        'risk_rf': risk['random_forest'],
                        'investment_portfolio': investment_portfolio,
                        'monthly_savings': monthly_savings,
                        'investment_horizon': investment_horizon,
                        'investment_goal': investment_goal
                    }
                    st.success(f"已更新 {name} 的风险评估")
                    break
        else:
            # 添加新成员
            st.session_state.family_members.append({
                'name': name,
                'age': age,
                'balance': balance,
                'risk_rule': risk['rule_based'],
                'risk_dt': risk['decision_tree'],
                'risk_rf': risk['random_forest']
            })
            st.success(f"已添加 {name} 到家庭成员列表")
            
        # 提示用户前往投资建议页面
        st.info("您可以前往'投资建议'页面获取个性化投资建议")

# 投资建议页面
elif page == "投资建议":
    st.title("💰 投资建议")
    
    # 检查是否有家庭成员
    if 'family_members' not in st.session_state or len(st.session_state.family_members) == 0:
        st.warning("尚未添加任何家庭成员，请先在'风险评估'页面添加成员")
    else:
        # 选择家庭成员
        members = [member['name'] for member in st.session_state.family_members]
        selected_member = st.selectbox("选择家庭成员", members)
        
        # 获取选中成员信息
        member = next((m for m in st.session_state.family_members if m['name'] == selected_member), None)
        
        if member:
            # 显示成员基本信息
            st.subheader(f"{member['name']}的基本信息")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**年龄:** {member['age']}岁")
            
            with col2:
                st.write(f"**账户余额:** ¥{member['balance']:,.2f}")
            
            with col3:
                risk_level = member['risk_rf']  # 使用随机森林结果作为风险等级
                risk_color = "🔴" if risk_level == "High" else "🟠" if risk_level == "Medium" else "🟢"
                st.write(f"**风险等级:** {risk_color} {risk_level}")
            
            # 投资偏好表单
            st.subheader("投资偏好")
            with st.form("investment_preference_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    investment_horizon = st.selectbox(
                        "投资期限",
                        options=["短期(1年以内)", "中期(1-5年)", "长期(5年以上)"],
                        index=1
                    )
                    
                    investment_goal = st.selectbox(
                        "投资目标",
                        options=["资本保全", "稳定收益", "平衡增长", "激进增长"],
                        index=1
                    )
                
                with col2:
                    monthly_savings = st.number_input("每月可投资金额", min_value=0, value=member.get('monthly_savings', 1000))
                    
                    risk_tolerance = st.slider(
                        "风险承受能力 (1-10)",
                        min_value=1,
                        max_value=10,
                        value=5,
                        help="1表示极低风险承受能力，10表示极高风险承受能力"
                    )
                
                submit = st.form_submit_button("获取投资建议")
            
            if submit or 'investment_portfolio' in member:
                # 获取增强版投资建议
                has_loans = member.get('housing', False) or member.get('loan', False)
                
                # 构建额外数据
                additional_data = {
                    'investment_horizon': investment_horizon,
                    'investment_goal': investment_goal,
                    'risk_tolerance': risk_tolerance
                }
                
                # 使用进度指示器替代spinner
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # 第一阶段：初始化
                status_text.text("正在初始化投资建议生成...")
                progress_bar.progress(10)
                time.sleep(0.5)  # 短暂延迟以显示进度
                
                # 第二阶段：基础投资建议
                status_text.text("正在生成基础投资建议...")
                progress_bar.progress(30)
                base_recommendation = investment_advisor.get_personalized_recommendation(
                    risk_level=risk_level,
                    age=member['age'],
                    balance=member['balance'],
                    has_loans=has_loans
                )
                
                # 显示初步结果
                progress_bar.progress(50)
                status_text.text("基础建议生成完成，正在获取市场数据...")
                
                # 第三阶段：获取市场数据
                with st.expander("查看初步投资建议", expanded=True):
                    st.markdown(f"### {base_recommendation['name']}")
                    st.write(base_recommendation['description'][:200] + "...")
                
                # 添加跳过选项
                skip_ai = st.checkbox("跳过AI增强分析（加快处理速度）")
                
                if skip_ai:
                    # 如果用户选择跳过AI分析
                    progress_bar.progress(100)
                    status_text.text("投资建议生成完成！")
                    investment_rec = base_recommendation
                else:
                    # 继续获取市场数据和AI建议
                    progress_bar.progress(70)
                    status_text.text("正在获取市场数据和AI增强建议...")
                    investment_rec = investment_advisor.get_enhanced_recommendation(
                        risk_level=risk_level,
                        age=member['age'],
                        balance=member['balance'],
                        has_loans=has_loans,
                        additional_data=additional_data
                    )
                    
                    progress_bar.progress(100)
                    status_text.text("投资建议生成完成！")
                
                # 显示投资建议
                st.subheader("🔮 投资建议")
                
                # 投资组合名称和描述
                st.markdown(f"### {investment_rec['name']}")
                st.write(investment_rec['description'])
                
                # 投资产品分配
                st.subheader("推荐投资产品配置")
                
                # 直接使用Streamlit的原生图表功能，避免matplotlib中文问题
                products = [p['name'] for p in investment_rec['products']]
                allocations = [p['allocation'] for p in investment_rec['products']]
                
                # 使用中文标签
                product_mapping = {
                    'Stocks': '股票',
                    'Bonds': '债券',
                    'Cash': '现金',
                    'Real Estate': '房地产',
                    'Commodities': '大宗商品',
                    'Cryptocurrencies': '加密货币',
                    'ETFs': 'ETF基金',
                    'Mutual Funds': '共同基金',
                    'CDs': '定期存款',
                    'Treasury Bills': '国债',
                    'High-Yield Bonds': '高收益债券',
                    'Growth Stocks': '成长股',
                    'Value Stocks': '价值股',
                    'Index Funds': '指数基金',
                    'Money Market': '货币市场'
                }
                
                # 转换为中文标签（如果有对应的翻译）
                products_zh = [product_mapping.get(p, p) for p in products]
                
                # 创建饼图数据
                pie_data = pd.DataFrame({
                    '产品': products_zh,
                    '分配比例': allocations
                })
                
                # 使用matplotlib创建饼图，确保使用中文字体
                st.write("### 投资产品配置比例")
                fig, ax = plt.subplots()
                # 确保使用中文字体 - 使用系统字体
                try:
                    # 尝试使用系统字体
                    font_path = fm.findfont(fm.FontProperties(family=['SimHei', 'Microsoft YaHei']))
                    prop = fm.FontProperties(fname=font_path)
                    ax.pie(pie_data['分配比例'], labels=pie_data['产品'], autopct='%1.1f%%', startangle=90,
                          textprops={'fontproperties': prop})
                except Exception as e:
                    st.warning(f"使用系统字体失败: {str(e)}，尝试使用默认字体")
                    # 如果系统字体失败，使用默认字体
                    ax.pie(pie_data['分配比例'], labels=pie_data['产品'], autopct='%1.1f%%', startangle=90)
                
                ax.axis('equal')  # 确保饼图是圆的
                st.pyplot(fig)
                
                
                # 产品详情表格 - 使用中文标题
                product_df = pd.DataFrame([
                    {
                        '产品名称': product_mapping.get(p['name'], p['name']),
                        '分配比例': f"{p['allocation']}%",
                        '描述': p['description']
                    }
                    for p in investment_rec['products']
                ])
                st.write("### 产品详情")
                st.dataframe(product_df, width=800)
                
                # 投资警告
                st.warning(investment_rec['warning'])
                
                # 显示AI增强建议
                if 'ai_advice' in investment_rec and investment_rec['ai_advice']:
                    st.subheader("🤖 AI增强投资建议")
                    with st.expander("查看AI增强建议", expanded=True):
                        st.markdown(investment_rec['ai_advice'])
                
                # 显示市场数据
                if 'market_data' in investment_rec and investment_rec['market_data']:
                    st.subheader("📈 市场数据")
                    with st.expander("查看市场数据"):
                        # 显示主要指数
                        if 'indices' in investment_rec['market_data']:
                            st.subheader("主要指数")
                            indices_data = investment_rec['market_data']['indices']
                            
                            col1, col2, col3 = st.columns(3)
                            
                            # S&P 500
                            if 'SP500' in indices_data and 'error' not in indices_data['SP500']:
                                with col1:
                                    sp500 = indices_data['SP500']
                                    if 'historical' in sp500 and 'results' in sp500['historical']:
                                        try:
                                            # 转换为DataFrame
                                            df = pd.DataFrame(sp500['historical']['results'])
                                            df['date'] = pd.to_datetime(df['date'])
                                            df = df.sort_values('date')
                                            df = df.set_index('date')
                                            
                                            # 显示S&P 500走势
                                            st.subheader("S&P 500")
                                            st.line_chart(df['close'])
                                        except Exception as e:
                                            st.error(f"无法显示S&P 500图表: {str(e)}")
                            
                            # NASDAQ
                            if 'NASDAQ' in indices_data and 'error' not in indices_data['NASDAQ']:
                                with col2:
                                    nasdaq = indices_data['NASDAQ']
                                    if 'historical' in nasdaq and 'results' in nasdaq['historical']:
                                        try:
                                            # 转换为DataFrame
                                            df = pd.DataFrame(nasdaq['historical']['results'])
                                            df['date'] = pd.to_datetime(df['date'])
                                            df = df.sort_values('date')
                                            df = df.set_index('date')
                                            
                                            # 显示NASDAQ走势
                                            st.subheader("NASDAQ")
                                            st.line_chart(df['close'])
                                        except Exception as e:
                                            st.error(f"无法显示NASDAQ图表: {str(e)}")
                            
                            # 道琼斯
                            if 'DOW' in indices_data and 'error' not in indices_data['DOW']:
                                with col3:
                                    dow = indices_data['DOW']
                                    if 'historical' in dow and 'results' in dow['historical']:
                                        try:
                                            # 转换为DataFrame
                                            df = pd.DataFrame(dow['historical']['results'])
                                            df['date'] = pd.to_datetime(df['date'])
                                            df = df.sort_values('date')
                                            df = df.set_index('date')
                                            
                                            # 显示道琼斯走势
                                            st.subheader("道琼斯")
                                            st.line_chart(df['close'])
                                        except Exception as e:
                                            st.error(f"无法显示道琼斯图表: {str(e)}")
                        
                        # 显示行业ETF数据
                        if 'sectors' in investment_rec['market_data']:
                            st.subheader("行业表现")
                            sectors_data = investment_rec['market_data']['sectors']
                            
                            for sector_name, sector_data in sectors_data.items():
                                if 'error' not in sector_data and 'historical' in sector_data and 'results' in sector_data['historical']:
                                    try:
                                        # 转换为DataFrame
                                        df = pd.DataFrame(sector_data['historical']['results'])
                                        df['date'] = pd.to_datetime(df['date'])
                                        df = df.sort_values('date')
                                        df = df.set_index('date')
                                        
                                        # 显示行业ETF走势
                                        st.subheader(f"{sector_name} 行业")
                                        st.line_chart(df['close'])
                                    except Exception as e:
                                        st.error(f"无法显示{sector_name}图表: {str(e)}")
                
                # 每月投资建议
                if monthly_savings > 0:
                    st.subheader("每月投资分配")
                    monthly_allocations = []
                    for product in investment_rec['products']:
                        amount = round(monthly_savings * product['allocation'] / 100, 2)
                        monthly_allocations.append({
                            '产品': product['name'],
                            '分配比例': f"{product['allocation']}%",
                            '每月投资金额': f"¥{amount:.2f}"
                        })
                    
                    st.table(pd.DataFrame(monthly_allocations))
                
                # 更新会话状态中的成员信息
                for i, m in enumerate(st.session_state.family_members):
                    if m['name'] == selected_member:
                        st.session_state.family_members[i].update({
                            'investment_portfolio': investment_rec['name'],
                            'monthly_savings': monthly_savings,
                            'investment_horizon': investment_horizon,
                            'investment_goal': investment_goal
                        })
                        if submit:
                            st.success(f"已更新 {selected_member} 的投资建议")
                        break

# 家庭投资组合页面
elif page == "家庭投资组合":
    st.title("👨‍👩‍👧‍👦 家庭投资组合")
    
    if 'family_members' not in st.session_state or len(st.session_state.family_members) == 0:
        st.warning("尚未添加任何家庭成员，请先在'风险评估'页面添加成员")
    else:
        # 显示家庭成员列表
        st.subheader("家庭成员列表")
        members_df = pd.DataFrame(st.session_state.family_members)
        
        # 选择要显示的列
        display_columns = ['name', 'age', 'balance', 'risk_rf', 'investment_portfolio', 'monthly_savings', 'investment_horizon', 'investment_goal']
        # 确保所有列都存在
        for col in display_columns:
            if col not in members_df.columns:
                members_df[col] = "未设置"
                
        # 重命名列以便显示
        column_rename = {
            'name': '姓名',
            'age': '年龄',
            'balance': '账户余额',
            'risk_rf': '风险等级',
            'investment_portfolio': '投资组合',
            'monthly_savings': '每月投资',
            'investment_horizon': '投资期限',
            'investment_goal': '投资目标'
        }
        
        display_df = members_df[display_columns].rename(columns=column_rename)
        st.dataframe(display_df, width=800)
        
        # 创建风险分布和投资组合分布图表
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("家庭风险分布")
            # 随机森林风险分布
            risk_counts_rf = members_df['risk_rf'].value_counts()
            
            # 创建风险等级中文映射
            risk_mapping = {
                'High': '高风险',
                'Medium': '中风险',
                'Low': '低风险'
            }
            
            # 转换为中文标签
            risk_counts_zh = pd.Series(
                risk_counts_rf.values,
                index=[risk_mapping.get(idx, idx) for idx in risk_counts_rf.index]
            )
            
            # 使用matplotlib创建饼图，确保使用中文字体
            st.write("### 家庭风险分布")
            fig, ax = plt.subplots()
            # 确保使用中文字体 - 使用系统字体
            try:
                # 尝试使用系统字体
                font_path = fm.findfont(fm.FontProperties(family=['SimHei', 'Microsoft YaHei']))
                prop = fm.FontProperties(fname=font_path)
                ax.pie(risk_counts_zh.values, labels=risk_counts_zh.index, autopct='%1.1f%%', startangle=90,
                      textprops={'fontproperties': prop})
            except Exception as e:
                st.warning(f"使用系统字体失败: {str(e)}，尝试使用默认字体")
                # 如果系统字体失败，使用默认字体
                ax.pie(risk_counts_zh.values, labels=risk_counts_zh.index, autopct='%1.1f%%', startangle=90)
            
            ax.axis('equal')  # 确保饼图是圆的
            st.pyplot(fig)
        
        with col2:
            st.subheader("投资组合分布")
            # 投资组合分布
            if 'investment_portfolio' in members_df.columns:
                portfolio_counts = members_df['investment_portfolio'].value_counts()
                
                # 使用matplotlib创建饼图，确保使用中文字体
                st.write("### 投资组合分布")
                fig, ax = plt.subplots()
                # 确保使用中文字体 - 使用系统字体
                try:
                    # 尝试使用系统字体
                    font_path = fm.findfont(fm.FontProperties(family=['SimHei', 'Microsoft YaHei']))
                    prop = fm.FontProperties(fname=font_path)
                    ax.pie(portfolio_counts.values, labels=portfolio_counts.index, autopct='%1.1f%%', startangle=90,
                          textprops={'fontproperties': prop})
                except Exception as e:
                    st.warning(f"使用系统字体失败: {str(e)}，尝试使用默认字体")
                    # 如果系统字体失败，使用默认字体
                    ax.pie(portfolio_counts.values, labels=portfolio_counts.index, autopct='%1.1f%%', startangle=90)
                
                ax.axis('equal')  # 确保饼图是圆的
                st.pyplot(fig)
            else:
                st.info("尚无投资组合数据")
        
        # 家庭投资总额和月度投资总额
        st.subheader("家庭投资概览")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_balance = members_df['balance'].sum()
            balance_color = "red" if total_balance < 0 else "orange" if total_balance < 5000 else "green"
            st.metric("家庭总资产", f"¥{total_balance:,.2f}")
        
        with col2:
            if 'monthly_savings' in members_df.columns:
                monthly_investment = members_df['monthly_savings'].sum()
                st.metric("每月总投资额", f"¥{monthly_investment:,.2f}")
            else:
                st.metric("每月总投资额", "未设置")
        
        with col3:
            # 计算年度投资收益预估（假设年化收益率5%）
            if 'monthly_savings' in members_df.columns:
                annual_investment = members_df['monthly_savings'].sum() * 12
                estimated_return = annual_investment * 0.05
                st.metric("预估年度投资收益", f"¥{estimated_return:,.2f}", 
                         delta="5%", delta_color="normal",
                         help="基于5%的年化收益率估算")
            else:
                st.metric("预估年度投资收益", "未设置")
        
        # 家庭投资建议
        st.subheader("家庭投资建议")
        
        # 计算高风险成员比例
        high_risk_count = len(members_df[members_df['risk_rf'] == 'High'])
        high_risk_percent = high_risk_count / len(members_df) * 100
        
        # 计算家庭平均月度投资额
        if 'monthly_savings' in members_df.columns:
            avg_monthly_investment = members_df['monthly_savings'].mean()
        else:
            avg_monthly_investment = 0
        
        # 显示家庭投资建议
        if high_risk_percent > 50:
            st.error("⚠️ 家庭整体风险较高，建议降低高风险资产配置，增加稳健型投资比例。")
            st.info("建议家庭投资组合配置：20%高风险资产，40%中风险资产，40%低风险资产")
        elif high_risk_percent > 30:
            st.warning("⚠️ 家庭存在一定风险，建议平衡投资组合。")
            st.info("建议家庭投资组合配置：30%高风险资产，40%中风险资产，30%低风险资产")
        else:
            st.success("✅ 家庭整体风险较低，可以适当增加收益型资产比例。")
            st.info("建议家庭投资组合配置：40%高风险资产，40%中风险资产，20%低风险资产")
        
        # 显示家庭投资组合建议图表
        st.subheader("家庭整体投资组合建议")
        
        # 根据风险比例确定建议的资产配置
        if high_risk_percent > 50:
            portfolio_allocation = {'高风险资产': 20, '中风险资产': 40, '低风险资产': 40}
        elif high_risk_percent > 30:
            portfolio_allocation = {'高风险资产': 30, '中风险资产': 40, '低风险资产': 30}
        else:
            portfolio_allocation = {'高风险资产': 40, '中风险资产': 40, '低风险资产': 20}
        
        # 转换为DataFrame以便使用Streamlit原生饼图
        allocation_df = pd.DataFrame({
            '资产类型': list(portfolio_allocation.keys()),
            '比例': list(portfolio_allocation.values())
        })
        
        # 使用matplotlib创建饼图，确保使用中文字体
        st.write("### 建议家庭资产配置")
        fig, ax = plt.subplots()
        # 确保使用中文字体 - 使用系统字体
        try:
            # 尝试使用系统字体
            font_path = fm.findfont(fm.FontProperties(family=['SimHei', 'Microsoft YaHei']))
            prop = fm.FontProperties(fname=font_path)
            ax.pie(allocation_df['比例'], labels=allocation_df['资产类型'], autopct='%1.1f%%', startangle=90,
                  textprops={'fontproperties': prop})
        except Exception as e:
            st.warning(f"使用系统字体失败: {str(e)}，尝试使用默认字体")
            # 如果系统字体失败，使用默认字体
            ax.pie(allocation_df['比例'], labels=allocation_df['资产类型'], autopct='%1.1f%%', startangle=90)
        
        ax.axis('equal')  # 确保饼图是圆的
        st.pyplot(fig)
        
        # 家庭成员投资详情
        st.subheader("家庭成员投资详情")
        
        # 按风险等级排序
        risk_order = {'High': 0, 'Medium': 1, 'Low': 2}
        sorted_members = sorted(st.session_state.family_members, 
                               key=lambda x: (risk_order.get(x.get('risk_rf', 'Low'), 3), -x.get('age', 0)))
        
        # 显示每个成员的投资详情
        for i, member in enumerate(sorted_members):
            with st.expander(f"{member['name']} ({member['age']}岁) - {member.get('investment_portfolio', '未设置投资组合')}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("#### 基本信息")
                    st.write(f"**账户余额:** ¥{member['balance']:,.2f}")
                    risk_color = "red" if member['risk_rf'] == "High" else "orange" if member['risk_rf'] == "Medium" else "green"
                    st.write(f"**风险等级:** <span style='color:{risk_color}'>{member['risk_rf']}</span>", unsafe_allow_html=True)
                    
                    if 'monthly_savings' in member:
                        st.write(f"**每月投资:** ¥{member['monthly_savings']:,.2f}")
                    if 'investment_horizon' in member:
                        st.write(f"**投资期限:** {member['investment_horizon']}")
                    if 'investment_goal' in member:
                        st.write(f"**投资目标:** {member['investment_goal']}")
                
                with col2:
                    st.write("#### 投资建议")
                    # 获取该成员的投资建议
                    if 'risk_rf' in member:
                        investment_rec = investment_advisor.get_investment_recommendation(member['risk_rf'])
                        
                        # 显示投资产品分配
                        products = [p['name'] for p in investment_rec['products']]
                        allocations = [p['allocation'] for p in investment_rec['products']]
                        
                        
                        # 创建投资产品映射
                        product_mapping = {
                            'Stocks': '股票',
                            'Bonds': '债券',
                            'Cash': '现金',
                            'Real Estate': '房地产',
                            'Commodities': '大宗商品',
                            'Cryptocurrencies': '加密货币',
                            'ETFs': 'ETF基金',
                            'Mutual Funds': '共同基金',
                            'CDs': '定期存款',
                            'Treasury Bills': '国债',
                            'High-Yield Bonds': '高收益债券',
                            'Growth Stocks': '成长股',
                            'Value Stocks': '价值股',
                            'Index Funds': '指数基金',
                            'Money Market': '货币市场'
                        }
                        
                        # 转换为中文标签
                        products_zh = [product_mapping.get(p, p) for p in products]
                        
                        # 创建DataFrame
                        product_df = pd.DataFrame({
                            '产品': products_zh,
                            '比例': allocations
                        })
                        
                        # 使用matplotlib创建饼图，确保使用中文字体
                        st.write("### 建议投资配置")
                        fig, ax = plt.subplots()
                        # 确保使用中文字体 - 使用系统字体
                        try:
                            # 尝试使用系统字体
                            font_path = fm.findfont(fm.FontProperties(family=['SimHei', 'Microsoft YaHei']))
                            prop = fm.FontProperties(fname=font_path)
                            ax.pie(product_df['比例'], labels=product_df['产品'], autopct='%1.1f%%', startangle=90,
                                  textprops={'fontproperties': prop})
                        except Exception as e:
                            st.warning(f"使用系统字体失败: {str(e)}，尝试使用默认字体")
                            # 如果系统字体失败，使用默认字体
                            ax.pie(product_df['比例'], labels=product_df['产品'], autopct='%1.1f%%', startangle=90)
                        
                        ax.axis('equal')  # 确保饼图是圆的
                        st.pyplot(fig)
        
        # 添加清除按钮
        if st.button("清除所有家庭成员"):
            st.session_state.family_members = []
            st.success("已清除所有家庭成员数据")
            st.rerun()

# AI投资助手页面
elif page == "AI投资助手":
    st.title("💬 AI投资助手")
    
    # 初始化聊天历史
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    
    # 显示聊天历史
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 用户输入
    if prompt := st.chat_input("请输入您的投资问题，例如：'分析苹果公司股票'、'我是35岁的工程师，请推荐投资组合'"):
        # 添加用户消息到聊天历史
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        
        # 显示用户消息
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 使用更详细的进度指示器
        with st.status("AI思考中...", expanded=True) as status:
            st.write("分析您的问题...")
            
            # 分解查询为子任务
            tasks = chat_assistant.ai_assistant.decompose_query(prompt)
            st.write("已确定需要完成的任务:")
            
            # 显示任务列表
            for i, task in enumerate(tasks):
                st.write(f"- {task}")
            
            # 创建进度条
            progress_bar = st.progress(0)
            progress_text = st.empty()
            progress_text.text("正在处理任务...")
            
            # 处理每个任务并显示进度
            task_results = []
            for i, task in enumerate(tasks):
                progress_percent = int((i / len(tasks)) * 80)  # 前80%用于任务处理
                progress_bar.progress(progress_percent)
                progress_text.text(f"正在处理: {task}")
                
                # 执行任务
                result_task = chat_assistant.execute_task(task, prompt)
                task_results.append({
                    "task": task,
                    "result": result_task
                })
                time.sleep(0.5)  # 短暂延迟以显示进度
            
            # 生成最终回复
            progress_bar.progress(90)
            progress_text.text("正在生成最终回复...")
            
            # 构建完整结果
            result = {
                "tasks": tasks,
                "task_results": task_results
            }
            
            # 生成回复
            system_message = "你是一位专业的投资顾问，擅长解释复杂的金融概念和提供投资建议。请基于任务结果生成一个全面、专业的回复。"
            user_message = f"用户查询: {prompt}\n\n任务结果:\n"
            for i, task_result in enumerate(task_results):
                user_message += f"任务{i+1}: {task_result['task']}\n"
                user_message += f"结果: {json.dumps(task_result['result'], ensure_ascii=False)}\n\n"
            
            user_message += "请基于以上信息生成一个专业、全面的回复。"
            
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
            
            response = chat_assistant.ai_assistant.chat_completion(messages)
            
            # 提取回复内容
            if "error" in response:
                final_response = "抱歉，我无法处理您的请求。请稍后再试。"
            else:
                try:
                    final_response = response["choices"][0]["message"]["content"]
                except Exception:
                    final_response = "抱歉，处理您的请求时出现错误。"
            
            result['response'] = final_response
            
            # 更新进度
            progress_bar.progress(100)
            progress_text.text("处理完成!")
            
            # 更新状态
            status.update(label="完成!", state="complete", expanded=False)
        
        # 显示AI回复
        with st.chat_message("assistant"):
            st.markdown(result['response'])
            
            # 如果有任务结果中包含股票数据，显示图表
            for task_result in result.get('task_results', []):
                if 'result' in task_result and isinstance(task_result['result'], dict):
                    # 检查是否有股票价格数据
                    if 'historical' in task_result['result'] and 'results' in task_result['result']['historical']:
                        try:
                            # 转换为DataFrame
                            prices_data = pd.DataFrame(task_result['result']['historical']['results'])
                            prices_data['date'] = pd.to_datetime(prices_data['date'])
                            prices_data = prices_data.set_index('date')
                            
                            # 显示股票价格图表
                            st.subheader("股票价格走势")
                            st.line_chart(prices_data['close'])
                        except Exception as e:
                            st.error(f"无法显示股票图表: {str(e)}")
        
        # 更新聊天历史
        st.session_state.chat_messages.append({"role": "assistant", "content": result['response']})
    
    # 显示使用提示
    if not st.session_state.chat_messages:
        st.info("👋 欢迎使用AI投资助手！您可以向我询问：")
        st.markdown("""
        - 股票分析：例如"分析苹果公司最近的表现"
        - 投资建议：例如"我是35岁的工程师，月收入2万元，请推荐投资组合"
        - 财务概念：例如"什么是市盈率？如何使用它评估股票？"
        - 市场趋势：例如"当前市场趋势如何？哪些行业表现较好？"
        """)

# 市场数据页面
elif page == "市场数据":
    st.title("📊 市场数据")
    
    # 初始化金融数据提供者
    financial_data = FinancialDataProvider(api_key=FINANCIAL_API_KEY)
    
    # 股票查询部分
    st.subheader("股票数据查询")
    
    col1, col2 = st.columns(2)
    
    with col1:
        ticker = st.text_input("股票代码", "AAPL")
    
    with col2:
        data_type = st.selectbox(
            "数据类型",
            options=["股票价格", "财务报表", "财务指标", "公司新闻"],
            index=0
        )
    
    if st.button("获取数据", type="primary"):
        with st.spinner(f"正在获取 {ticker} 的{data_type}..."):
            try:
                if data_type == "股票价格":
                    # 获取股票价格
                    end_date = pd.Timestamp.now().strftime('%Y-%m-%d')
                    start_date = (pd.Timestamp.now() - pd.Timedelta(days=365)).strftime('%Y-%m-%d')
                    
                    # 确保日期参数有效
                    if not start_date or not end_date:
                        import datetime
                        end_date = datetime.datetime.now().strftime('%Y-%m-%d')
                        start_date = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
                    
                    stock_data = financial_data.get_stock_prices(
                        ticker=ticker,
                        start_date=start_date,
                        end_date=end_date,
                        interval="day",
                        interval_multiplier=1
                    )
                    
                    if 'error' in stock_data:
                        st.error(f"获取股票数据失败: {stock_data['error']}")
                    else:
                        # 显示股票快照数据
                        snapshot = financial_data.get_stock_snapshot(ticker)
                        if 'error' not in snapshot:
                            st.subheader(f"{ticker} 当前数据")
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                current_price = snapshot.get('price', 'N/A')
                                st.metric("当前价格", f"${current_price}")
                            
                            with col2:
                                change = snapshot.get('change', 'N/A')
                                change_percent = snapshot.get('change_percent', 'N/A')
                                # 确保change是数值类型才进行比较
                                delta_color = "normal" if isinstance(change, (int, float)) and change >= 0 else "inverse"
                                st.metric("价格变动", f"${change}", f"{change_percent}%", delta_color=delta_color)
                            
                            with col3:
                                market_cap = snapshot.get('market_cap', 'N/A')
                                if isinstance(market_cap, (int, float)) and market_cap > 1000000000:
                                    market_cap = f"${market_cap/1000000000:.2f}B"
                                st.metric("市值", market_cap)
                        
                        # 显示历史价格图表
                        if 'results' in stock_data.get('historical', {}):
                            st.subheader(f"{ticker} 历史价格")
                            
                            # 转换为DataFrame
                            prices_df = pd.DataFrame(stock_data['historical']['results'])
                            prices_df['date'] = pd.to_datetime(prices_df['date'])
                            prices_df = prices_df.sort_values('date')
                            prices_df = prices_df.set_index('date')
                            
                            # 显示价格图表
                            st.line_chart(prices_df['close'])
                            
                            # 显示交易量图表
                            st.subheader("交易量")
                            st.bar_chart(prices_df['volume'])
                            
                            # 显示数据表格
                            st.subheader("价格数据")
                            st.dataframe(prices_df[['open', 'high', 'low', 'close', 'volume']])
                
                elif data_type == "财务报表":
                    # 创建选项卡
                    tab1, tab2, tab3 = st.tabs(["损益表", "资产负债表", "现金流量表"])
                    
                    with tab1:
                        st.subheader(f"{ticker} 损益表")
                        income_data = financial_data.get_financial_statements(ticker, statement_type="income")
                        if 'error' in income_data:
                            st.error(f"获取损益表失败: {income_data['error']}")
                        else:
                            if 'results' in income_data:
                                income_df = pd.DataFrame(income_data['results'])
                                if not income_df.empty:
                                    st.dataframe(income_df)
                                else:
                                    st.info("没有找到损益表数据")
                    
                    with tab2:
                        st.subheader(f"{ticker} 资产负债表")
                        balance_data = financial_data.get_financial_statements(ticker, statement_type="balance")
                        if 'error' in balance_data:
                            st.error(f"获取资产负债表失败: {balance_data['error']}")
                        else:
                            if 'results' in balance_data:
                                balance_df = pd.DataFrame(balance_data['results'])
                                if not balance_df.empty:
                                    st.dataframe(balance_df)
                                else:
                                    st.info("没有找到资产负债表数据")
                    
                    with tab3:
                        st.subheader(f"{ticker} 现金流量表")
                        cashflow_data = financial_data.get_financial_statements(ticker, statement_type="cashflow")
                        if 'error' in cashflow_data:
                            st.error(f"获取现金流量表失败: {cashflow_data['error']}")
                        else:
                            if 'results' in cashflow_data:
                                cashflow_df = pd.DataFrame(cashflow_data['results'])
                                if not cashflow_df.empty:
                                    st.dataframe(cashflow_df)
                                else:
                                    st.info("没有找到现金流量表数据")
                
                elif data_type == "财务指标":
                    # 获取财务指标
                    metrics_data = financial_data.get_financial_metrics(ticker)
                    if 'error' in metrics_data:
                        st.error(f"获取财务指标失败: {metrics_data['error']}")
                    else:
                        st.subheader(f"{ticker} 财务指标")
                        if 'results' in metrics_data:
                            metrics_df = pd.DataFrame(metrics_data['results'])
                            if not metrics_df.empty:
                                # 显示关键指标
                                st.subheader("关键财务指标")
                                col1, col2, col3 = st.columns(3)
                                
                                # 获取最新的财务指标
                                latest_metrics = metrics_df.iloc[0] if not metrics_df.empty else {}
                                
                                with col1:
                                    pe_ratio = latest_metrics.get('pe_ratio', 'N/A')
                                    st.metric("市盈率 (P/E)", pe_ratio)
                                
                                with col2:
                                    pb_ratio = latest_metrics.get('pb_ratio', 'N/A')
                                    st.metric("市净率 (P/B)", pb_ratio)
                                
                                with col3:
                                    roe = latest_metrics.get('roe', 'N/A')
                                    if isinstance(roe, (int, float)):
                                        roe = f"{roe:.2%}"
                                    st.metric("股本回报率 (ROE)", roe)
                                
                                # 显示完整数据表格
                                st.subheader("完整财务指标")
                                st.dataframe(metrics_df)
                            else:
                                st.info("没有找到财务指标数据")
                
                elif data_type == "公司新闻":
                    # 获取公司新闻
                    news_data = financial_data.get_news(ticker)
                    if 'error' in news_data:
                        st.error(f"获取公司新闻失败: {news_data['error']}")
                    else:
                        st.subheader(f"{ticker} 相关新闻")
                        if 'results' in news_data:
                            for news in news_data['results']:
                                with st.container():
                                    st.markdown(f"### [{news.get('title', 'No Title')}]({news.get('url', '#')})")
                                    st.markdown(f"**来源**: {news.get('source', 'Unknown')} | **日期**: {news.get('date', 'Unknown')}")
                                    st.markdown(news.get('summary', 'No summary available'))
                                    st.divider()
            
            except Exception as e:
                st.error(f"处理数据时出错: {str(e)}")
    
    # 市场概览部分
    st.subheader("市场概览")
    
    if st.button("加载市场数据"):
        with st.spinner("正在获取市场数据..."):
            try:
                # 获取宏观经济数据（免费API）
                macro_data = financial_data.get_macro_data("interest_rates", limit=5)
                
                # 显示宏观经济指标
                st.subheader("宏观经济指标")
                
                if 'error' not in macro_data and 'results' in macro_data:
                    # 显示利率数据
                    st.write("### 利率数据")
                    
                    # 转换为DataFrame以便显示
                    try:
                        rates_df = pd.DataFrame(macro_data['results'])
                        if not rates_df.empty:
                            # 格式化日期和数值
                            if 'date' in rates_df.columns:
                                rates_df['date'] = pd.to_datetime(rates_df['date']).dt.strftime('%Y-%m-%d')
                            
                            # 显示表格
                            st.dataframe(rates_df)
                            
                            # 如果有足够的数据，显示图表
                            if len(rates_df) > 1 and 'value' in rates_df.columns and 'date' in rates_df.columns:
                                rates_df['value'] = pd.to_numeric(rates_df['value'], errors='coerce')
                                rates_df = rates_df.sort_values('date')
                                
                                st.subheader("利率趋势")
                                st.line_chart(rates_df.set_index('date')['value'])
                        else:
                            st.info("暂无利率数据")
                    except Exception as e:
                        st.error(f"处理利率数据时出错: {str(e)}")
                else:
                    st.info("暂无宏观经济数据，请稍后再试")
                
                # 获取通胀数据
                inflation_data = financial_data.get_macro_data("inflation", limit=5)
                
                if 'error' not in inflation_data and 'results' in inflation_data:
                    # 显示通胀数据
                    st.write("### 通胀数据")
                    
                    # 转换为DataFrame以便显示
                    try:
                        inflation_df = pd.DataFrame(inflation_data['results'])
                        if not inflation_df.empty:
                            # 格式化日期和数值
                            if 'date' in inflation_df.columns:
                                inflation_df['date'] = pd.to_datetime(inflation_df['date']).dt.strftime('%Y-%m-%d')
                            
                            # 显示表格
                            st.dataframe(inflation_df)
                            
                            # 如果有足够的数据，显示图表
                            if len(inflation_df) > 1 and 'value' in inflation_df.columns and 'date' in inflation_df.columns:
                                inflation_df['value'] = pd.to_numeric(inflation_df['value'], errors='coerce')
                                inflation_df = inflation_df.sort_values('date')
                                
                                st.subheader("通胀趋势")
                                st.line_chart(inflation_df.set_index('date')['value'])
                        else:
                            st.info("暂无通胀数据")
                    except Exception as e:
                        st.error(f"处理通胀数据时出错: {str(e)}")
                
                # 获取GDP数据
                gdp_data = financial_data.get_macro_data("gdp", limit=5)
                
                if 'error' not in gdp_data and 'results' in gdp_data:
                    # 显示GDP数据
                    st.write("### GDP数据")
                    
                    # 转换为DataFrame以便显示
                    try:
                        gdp_df = pd.DataFrame(gdp_data['results'])
                        if not gdp_df.empty:
                            # 格式化日期和数值
                            if 'date' in gdp_df.columns:
                                gdp_df['date'] = pd.to_datetime(gdp_df['date']).dt.strftime('%Y-%m-%d')
                            
                            # 显示表格
                            st.dataframe(gdp_df)
                            
                            # 如果有足够的数据，显示图表
                            if len(gdp_df) > 1 and 'value' in gdp_df.columns and 'date' in gdp_df.columns:
                                gdp_df['value'] = pd.to_numeric(gdp_df['value'], errors='coerce')
                                gdp_df = gdp_df.sort_values('date')
                                
                                st.subheader("GDP趋势")
                                st.line_chart(gdp_df.set_index('date')['value'])
                        else:
                            st.info("暂无GDP数据")
                    except Exception as e:
                        st.error(f"处理GDP数据时出错: {str(e)}")
                else:
                    st.info("暂无GDP数据，请稍后再试")
                
                # 获取热门股票公司概况数据（免费API）
                popular_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
                company_data = {}
                
                for stock in popular_stocks:
                    try:
                        profile = financial_data.get_company_profile(stock)
                        if 'error' not in profile:
                            company_data[stock] = profile
                        else:
                            print(f"获取{stock}公司概况失败: {profile.get('error', '未知错误')}")
                    except Exception as e:
                        print(f"获取{stock}公司概况异常: {str(e)}")
                
                # 显示热门公司概况
                st.subheader("热门公司概况")
                
                # 创建列，但只为有数据的股票创建
                available_stocks = [stock for stock in popular_stocks if stock in company_data]
                if available_stocks:
                    for stock in available_stocks:
                        with st.expander(f"{stock} - 公司概况", expanded=False):
                            data = company_data[stock]
                            
                            if 'results' in data and data['results']:
                                profile = data['results'][0] if isinstance(data['results'], list) else data['results']
                                
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.write(f"**公司名称:** {profile.get('name', 'N/A')}")
                                    st.write(f"**股票代码:** {profile.get('ticker', 'N/A')}")
                                    st.write(f"**行业:** {profile.get('industry', 'N/A')}")
                                    st.write(f"**部门:** {profile.get('sector', 'N/A')}")
                                
                                with col2:
                                    st.write(f"**市值:** {profile.get('market_cap', 'N/A')}")
                                    st.write(f"**员工数:** {profile.get('employees', 'N/A')}")
                                    st.write(f"**国家:** {profile.get('country', 'N/A')}")
                                    st.write(f"**交易所:** {profile.get('exchange', 'N/A')}")
                                
                                st.write("**公司描述:**")
                                st.write(profile.get('description', 'N/A'))
                            else:
                                st.info(f"暂无{stock}的公司概况数据")
                    
                    # 获取收益数据
                    st.subheader("最新收益报告")
                    
                    for stock in available_stocks:
                        try:
                            earnings = financial_data.get_earnings(stock, limit=3)
                            if 'error' not in earnings and 'results' in earnings and earnings['results']:
                                with st.expander(f"{stock} - 收益报告", expanded=False):
                                    # 转换为DataFrame
                                    earnings_df = pd.DataFrame(earnings['results'])
                                    if not earnings_df.empty:
                                        st.dataframe(earnings_df)
                                    else:
                                        st.info(f"暂无{stock}的收益数据")
                        except Exception as e:
                            st.error(f"获取{stock}收益数据异常: {str(e)}")
                else:
                    st.info("暂时无法获取公司数据，请稍后再试。")
            
            except Exception as e:
                st.error(f"获取市场数据时出错: {str(e)}")