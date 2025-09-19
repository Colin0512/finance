# 家康智投系统 - AI金融能力增强版

本文档说明了如何将AI Financial Agent项目的功能整合到家康智投系统中，以增强其风险评估和投资建议能力。

## 整合内容

我们从AI Financial Agent项目中提取并整合了以下模块和能力：

1. **金融数据API集成**
   - 通过Financial Datasets API获取实时股票价格、财务报表和市场数据
   - 支持股票搜索、财务指标分析和新闻获取

2. **AI驱动的投资分析**
   - 使用Deepseek API提供智能投资建议和风险分析
   - 支持自然语言处理和对话式交互

3. **交互式数据可视化**
   - 股票价格走势图
   - 财务报表和指标可视化
   - 市场指数和行业ETF分析

## 新增文件

1. **financial_data_provider.py**
   - 金融数据提供者，整合Financial Datasets API的功能
   - 用于获取股票价格、财务报表和市场数据

2. **ai_assistant.py**
   - AI助手模块，整合Deepseek API的功能
   - 用于提供智能投资建议和自然语言交互

3. **financial_integration.py**
   - 整合模块，将金融数据API和AI助手整合到家康智投系统中
   - 提供增强版风险分类器、投资顾问和聊天助手

## 新增功能

1. **AI投资助手页面**
   - 通过聊天界面与AI助手交互
   - 获取投资建议、市场分析和财务概念解释

2. **市场数据页面**
   - 查询股票价格、财务报表和财务指标
   - 查看市场概览和热门股票

3. **增强的风险评估**
   - 结合规则型分类、机器学习模型和AI分析
   - 提供更全面、更深入的风险分析

4. **增强的投资建议**
   - 基于实时市场数据提供个性化投资建议
   - AI增强的资产配置方案和投资策略

## 使用的API密钥

- Financial Datasets API: 6b1d6fe9-833b-4071-8ac4-eadb1fc042c7
- Deepseek API: sk-f41ae42c0c7f4b9bbc8fd79ada481232

## 运行方式

与原始家康智投系统相同，可以通过以下两种方式运行：

1. 使用run_app.py脚本：
```bash
python run_app.py
```

2. 直接使用streamlit命令：
```bash
streamlit run app.py
```

## 注意事项

1. 确保已安装所有必要的依赖项：
```bash
pip install -r requirements.txt
```

2. API调用可能会受到限制，如果遇到API限制问题，请稍后再试。

3. 金融数据API提供的数据仅供参考，不应作为实际投资决策的唯一依据。

4. 本系统仅用于教育和研究目的，不构成投资建议。
