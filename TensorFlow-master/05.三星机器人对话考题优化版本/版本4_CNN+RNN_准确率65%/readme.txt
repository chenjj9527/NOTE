1.代码执行顺序:run_cnn.py->run_rnn.py->eval.py

2.CNN准确率:65.2 RNN准确率:41.7%

3.data.py是不去除停用词，采用字符级的向量
  data2.py是去除停用词，切词后的向量
  目前是data.py的准确率明显高于data2.py
4.conf.py是配置文件

5.eval是加载训练好的cnn与rnn模型，分别计算准确率和模型融合后的准确率
  目前模型融合后的准确率只有58.7%
6.本次改进最大的亮点:
  1.训练时只保存最佳的测试模型，提升了2个点
  2.采用字符级的向量比去除停用词后切词的效果好
  3.实验了RNN+CNN的模型融合
  4.LSTM的训练速度比GRU慢一倍，同时GRU的准确率在43%，比LSTM略好，但是CNN远远更好
  
7.原始代码介绍:https://gaussic.github.io/2017/08/30/text-classification-tensorflow/
  该模型的工程化做的很好
