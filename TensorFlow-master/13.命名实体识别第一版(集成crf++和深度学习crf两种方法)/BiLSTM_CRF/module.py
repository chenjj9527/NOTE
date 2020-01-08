#coding:utf-8
'''
Created on 2018年2月9日

@author: cjj

@email:

'''
import tensorflow as tf
from tensorflow.contrib.rnn import LSTMCell
from tensorflow.contrib.crf import crf_log_likelihood


class BiLSTM_CRF(object):
    def __init__(self,data,args):
        self.data=data
        self.args=args
        self.build_graph()
    
    #建立graph
    def build_graph(self):
        self.add_placeholders()
        
        #词嵌入
        with tf.variable_scope("words"):
            _word_embeddings = tf.Variable(self.data.embeddings,
                                           dtype=tf.float32,
                                           name="_word_embeddings")
            self.word_embeddings = tf.nn.embedding_lookup(params=_word_embeddings,
                                                     ids=self.batch_x,
                                                     name="word_embeddings")        
        with tf.variable_scope("bi-lstm"):
            (output_fw_seq, output_bw_seq), _ = tf.nn.bidirectional_dynamic_rnn(
                cell_fw=LSTMCell(self.args.hidden_dim),#self.args.hidden_dim是指每次RNN的输出维度
                cell_bw=LSTMCell(self.args.hidden_dim),
                inputs=self.word_embeddings,
                sequence_length=self.sequence_lengths,
                dtype=tf.float32)
            print('output_fw_seq',output_fw_seq.shape,output_bw_seq.shape)#(?, ?, 128)
            output = tf.concat([output_fw_seq, output_bw_seq], axis=-1)#此处需要打印一下调试信息，观察一下维度
            print('output',output.shape)#(?, ?, 256),其中256就是这个词抽出来的特征
            output = tf.nn.dropout(output, self.keep_prob)        

        with tf.variable_scope("proj"):
            W = tf.get_variable(name="W",
                                shape=[2 * self.args.hidden_dim, len(self.data.labels)],
                                initializer=tf.contrib.layers.xavier_initializer(),
                                dtype=tf.float32)

            b = tf.get_variable(name="b",
                                shape=[len(self.data.labels)],
                                initializer=tf.zeros_initializer(),
                                dtype=tf.float32)

            s = tf.shape(output)
            output = tf.reshape(output, [-1, 2*self.args.hidden_dim])
            pred = tf.matmul(output, W) + b#得到[?,每个词对应的label]
            #s[1]应该是句子的长度,此处self.logits是[?,每个词对应的label]
            print('pred',pred.shape)#(?, 7)
            self.logits = tf.reshape(pred, [-1, s[1], len(self.data.labels)])
            print('logits',self.logits.shape)#(?, ?, 7)
            #batch_y是[Batch_size,句子长度,每个词对应的label]
            log_likelihood, self.transition_params = crf_log_likelihood(inputs=self.logits,
                                                                   tag_indices=self.batch_y,
                                                                   sequence_lengths=self.sequence_lengths)
            self.loss = -tf.reduce_mean(log_likelihood)

        with tf.variable_scope("train_step"):
            self.global_step = tf.Variable(0, name="global_step", trainable=False)
            if self.args.optimizer == 'Adam':
                optim = tf.train.AdamOptimizer(learning_rate=self.args.lr)
            elif self.args.optimizer == 'Adadelta':
                optim = tf.train.AdadeltaOptimizer(learning_rate=self.args.lr)
            elif self.args.optimizer == 'Adagrad':
                optim = tf.train.AdagradOptimizer(learning_rate=self.args.lr)
            elif self.args.optimizer == 'RMSProp':
                optim = tf.train.RMSPropOptimizer(learning_rate=self.args.lr)
            elif self.args.optimizer == 'Momentum':
                optim = tf.train.MomentumOptimizer(learning_rate=self.args.lr, momentum=0.9)
            elif self.args.optimizer == 'SGD':
                optim = tf.train.GradientDescentOptimizer(learning_rate=self.args.lr)
            else:
                optim = tf.train.GradientDescentOptimizer(learning_rate=self.args.lr)

            grads_and_vars = optim.compute_gradients(self.loss)
            grads_and_vars_clip = [[tf.clip_by_value(g, -5.0, 5.0), v] for g, v in grads_and_vars]
            self.train_op = optim.apply_gradients(grads_and_vars_clip, global_step=self.global_step)
   
    def add_placeholders(self):
        self.batch_x = tf.placeholder(tf.int32, shape=[None, None], name="x")
        self.batch_y = tf.placeholder(tf.int32, shape=[None,None], name="y")
        self.sequence_lengths = tf.placeholder(tf.int32, shape=[None], name="sequence_lengths")
        self.keep_prob = tf.placeholder(tf.float32, name="dropout_keep_prob")
