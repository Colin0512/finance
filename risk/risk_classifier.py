import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os

class FamilyRiskClassifier:
    def __init__(self, auto_init=True):
        self.dt_model = None
        self.rf_model = None
        self.label_encoders = {}
        self.risk_encoder = None
        self.model_path = os.path.join(os.path.dirname(__file__), 'models')
        self.feature_names = None
        
        # 确保模型目录存在
        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)
        
        # 自动初始化模型
        if auto_init:
            self._initialize_models()
    
    def _initialize_models(self):
        """自动初始化模型，如果没有预训练模型，则使用规则型分类"""
        # 尝试加载模型
        if not self.load_models():
            print("未找到预训练模型，将使用规则型分类逻辑")
            # 初始化风险编码器
            self.risk_encoder = LabelEncoder()
            self.risk_encoder.fit(['High', 'Medium', 'Low'])
            # 设置默认特征名称
            self.feature_names = ['age', 'job', 'marital', 'education', 'balance', 'housing', 'loan']
    
    def preprocess_data(self, data):
        """预处理数据，包括标签编码"""
        # 复制数据，避免修改原始数据
        processed_data = data.copy()
        
        # 对分类特征进行编码
        for col in processed_data.select_dtypes(include='object').columns:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
                processed_data[col] = self.label_encoders[col].fit_transform(processed_data[col])
            else:
                # 处理新数据中可能出现的未知类别
                known_classes = set(self.label_encoders[col].classes_)
                processed_data[col] = processed_data[col].apply(
                    lambda x: x if x in known_classes else list(known_classes)[0]
                )
                processed_data[col] = self.label_encoders[col].transform(processed_data[col])
        
        return processed_data
    
    def assign_risk_levels(self, data):
        """根据规则分配风险等级"""
        conditions = [
            (data['balance'] < 0) | ((data['loan'] == 1) & (data['housing'] == 1)),
            ((data['balance'] >= 0) & (data['balance'] < 1000)),
            (data['balance'] >= 1000)
        ]
        risk_labels = ['High', 'Medium', 'Low']
        data['risk_level'] = np.select(conditions, risk_labels, default='Medium')
        return data
    
    def train(self, data, features=None):
        """训练风险分类模型"""
        if features is None:
            features = ['age', 'job', 'marital', 'education', 'balance', 'housing', 'loan']
        
        # 保存特征名称顺序
        self.feature_names = features
        
        # 选择特征
        data = data[features].copy()
        
        # 预处理数据
        processed_data = self.preprocess_data(data)
        
        # 分配风险等级
        processed_data = self.assign_risk_levels(processed_data)
        
        # 编码风险等级
        self.risk_encoder = LabelEncoder()
        processed_data['risk_level_encoded'] = self.risk_encoder.fit_transform(processed_data['risk_level'])
        
        # 准备训练数据
        X = processed_data.drop(['risk_level', 'risk_level_encoded'], axis=1)
        y = processed_data['risk_level_encoded']
        
        # 分割训练集和测试集
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        # 训练决策树模型
        self.dt_model = DecisionTreeClassifier(max_depth=4, random_state=42)
        self.dt_model.fit(X_train, y_train)
        
        # 训练随机森林模型
        self.rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.rf_model.fit(X_train, y_train)
        
        # 评估模型
        dt_pred = self.dt_model.predict(X_test)
        rf_pred = self.rf_model.predict(X_test)
        
        dt_accuracy = accuracy_score(y_test, dt_pred)
        rf_accuracy = accuracy_score(y_test, rf_pred)
        
        print(f"决策树模型准确率: {dt_accuracy:.4f}")
        print(f"随机森林模型准确率: {rf_accuracy:.4f}")
        
        print("\n决策树分类报告:")
        print(classification_report(y_test, dt_pred, target_names=self.risk_encoder.classes_))
        
        print("\n随机森林分类报告:")
        print(classification_report(y_test, rf_pred, target_names=self.risk_encoder.classes_))
        
        # 保存模型
        self.save_models()
        
        return {
            'dt_accuracy': dt_accuracy,
            'rf_accuracy': rf_accuracy,
            'dt_report': classification_report(y_test, dt_pred, target_names=self.risk_encoder.classes_, output_dict=True),
            'rf_report': classification_report(y_test, rf_pred, target_names=self.risk_encoder.classes_, output_dict=True)
        }
    
    def predict(self, data, model_type='dt'):
        """使用训练好的模型预测风险等级"""
        # 如果模型未加载，则使用规则型分类
        if self.dt_model is None or self.rf_model is None:
            # 使用规则型分类
            result = []
            for _, row in data.iterrows():
                if row['balance'] < 0 or (row['loan'] == 1 and row['housing'] == 1):
                    result.append('High')
                elif 0 <= row['balance'] < 1000:
                    result.append('Medium')
                else:
                    result.append('Low')
            return np.array(result)
        
        # 确保数据包含所有必要的特征，并按正确顺序排列
        if self.feature_names:
            # 创建一个包含所有必要特征的新数据框
            missing_features = set(self.feature_names) - set(data.columns)
            for feature in missing_features:
                data[feature] = 0  # 用默认值填充缺失特征
            
            # 按照训练时的特征顺序排列
            data = data[self.feature_names]
        
        # 预处理数据
        processed_data = self.preprocess_data(data)
        
        # 选择模型
        model = self.dt_model if model_type.lower() == 'dt' else self.rf_model
        
        # 预测
        risk_encoded = model.predict(processed_data)
        risk_labels = self.risk_encoder.inverse_transform(risk_encoded)
        
        return risk_labels
    
    def classify_risk_level(self, age, balance, loan, housing, job='unknown', marital='unknown', education='unknown'):
        """根据单个家庭成员的特征预测风险等级"""
        # 创建数据帧
        data = pd.DataFrame([{
            'age': age,
            'balance': balance,
            'loan': 1 if loan.lower() == 'yes' else 0,
            'housing': 1 if housing.lower() == 'yes' else 0,
            'job': job,
            'marital': marital,
            'education': education
        }])
        
        # 使用规则分配风险等级
        if balance < 0 or (data['loan'][0] == 1 and data['housing'][0] == 1):
            rule_based_risk = 'High'
        elif 0 <= balance < 1000:
            rule_based_risk = 'Medium'
        else:
            rule_based_risk = 'Low'
        
        # 使用模型预测风险等级
        try:
            # 如果模型已训练，使用模型预测
            if self.dt_model is not None and self.rf_model is not None:
                dt_risk = self.predict(data, 'dt')[0]
                rf_risk = self.predict(data, 'rf')[0]
            else:
                # 如果模型未训练，使用规则型分类
                dt_risk = rule_based_risk
                rf_risk = rule_based_risk
        except Exception as e:
            print(f"预测错误: {e}")
            # 发生错误时使用规则型分类
            dt_risk = rule_based_risk
            rf_risk = rule_based_risk
        
        return {
            'rule_based': rule_based_risk,
            'decision_tree': dt_risk,
            'random_forest': rf_risk
        }
    
    def save_models(self):
        """保存训练好的模型和编码器"""
        # 保存决策树模型
        with open(os.path.join(self.model_path, 'dt_model.pkl'), 'wb') as f:
            pickle.dump(self.dt_model, f)
        
        # 保存随机森林模型
        with open(os.path.join(self.model_path, 'rf_model.pkl'), 'wb') as f:
            pickle.dump(self.rf_model, f)
        
        # 保存标签编码器
        with open(os.path.join(self.model_path, 'label_encoders.pkl'), 'wb') as f:
            pickle.dump(self.label_encoders, f)
        
        # 保存风险等级编码器
        with open(os.path.join(self.model_path, 'risk_encoder.pkl'), 'wb') as f:
            pickle.dump(self.risk_encoder, f)
            
        # 保存特征名称
        with open(os.path.join(self.model_path, 'feature_names.pkl'), 'wb') as f:
            pickle.dump(self.feature_names, f)
    
    def load_models(self):
        """加载保存的模型和编码器"""
        try:
            # 加载决策树模型
            with open(os.path.join(self.model_path, 'dt_model.pkl'), 'rb') as f:
                self.dt_model = pickle.load(f)
            
            # 加载随机森林模型
            with open(os.path.join(self.model_path, 'rf_model.pkl'), 'rb') as f:
                self.rf_model = pickle.load(f)
            
            # 加载标签编码器
            with open(os.path.join(self.model_path, 'label_encoders.pkl'), 'rb') as f:
                self.label_encoders = pickle.load(f)
            
            # 加载风险等级编码器
            with open(os.path.join(self.model_path, 'risk_encoder.pkl'), 'rb') as f:
                self.risk_encoder = pickle.load(f)
                
            # 加载特征名称
            try:
                with open(os.path.join(self.model_path, 'feature_names.pkl'), 'rb') as f:
                    self.feature_names = pickle.load(f)
            except:
                # 如果特征名称文件不存在，使用默认特征名称
                self.feature_names = ['age', 'job', 'marital', 'education', 'balance', 'housing', 'loan']
            
            return True
        except Exception as e:
            print(f"加载模型失败: {e}")
            return False

# 示例用法
if __name__ == "__main__":
    # 加载数据
    data = pd.read_csv("Dataset/bank.csv", sep=',')
    
    # 选择特征
    features = ['age', 'job', 'marital', 'education', 'balance', 'housing', 'loan']
    data = data[features]
    
    # 创建分类器
    classifier = FamilyRiskClassifier()
    
    # 训练模型
    results = classifier.train(data)
    
    # 测试单个家庭成员
    member = {
        'age': 35,
        'balance': 2000,
        'loan': 'no',
        'housing': 'yes',
        'job': 'technician',
        'marital': 'married',
        'education': 'tertiary'
    }
    
    risk = classifier.classify_risk_level(**member)
    print("\n家庭成员风险评估:")
    print(f"规则型风险: {risk['rule_based']}")
    print(f"决策树模型风险: {risk['decision_tree']}")
    print(f"随机森林模型风险: {risk['random_forest']}")