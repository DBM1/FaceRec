# 神经网络模块
## 在使用该模块时仅需调用下列函数：
### def impimg():
加载训练集，返回训练矩阵和标签矩阵（仅用于初始化训练模型）<br><br>
### def train(trainX, trainY, tfSavePath):
输入且只能输入由impimg()产生的训练矩阵、标签矩阵及模型保存路径，开始训练模型（仅用于初始化训练模型）<br><br>
### def addimpimg():
加载新添加的训练集，返回训练矩阵和标签矩阵（仅用于更新已存在的训练模型）<br><br>
### def train(trainX, trainY, tfSavePath):
输入且只能输入由addimpimg()产生的训练矩阵、标签矩阵及模型保存路径，开始训练模型（仅用于更新已存在的训练模型）<br><br>
### def rec(tfsavepath):
打开摄像头测试模型<br><br>
## 模型训练或更新完成后请注释代码，防止该模块被其他模块使用时产生错误
