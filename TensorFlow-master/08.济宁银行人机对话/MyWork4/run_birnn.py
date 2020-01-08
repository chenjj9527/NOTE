#coding:utf-8
'''
Created on 2017年12月15日

@author: cjj

@email:

'''
#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import time
 
from sklearn import metrics
from datetime import timedelta
from data import data
from birnn_module import BiRNN

import tensorflow as tf
import numpy as np
import conf
save_dir = 'checkpoints/textbirnn'
save_path = os.path.join(save_dir, 'best_validation')   # 最佳验证结果保存路径

def get_time_dif(start_time):
    """获取已使用时间"""
    end_time = time.time()
    time_dif = end_time - start_time
    return timedelta(seconds=int(round(time_dif)))

def feed_data(x_batch, y_batch, keep_prob):
    feed_dict = {
        model.input_x: x_batch,
        model.input_y: y_batch,
        model.keep_prob: keep_prob
    }
    return feed_dict

def evaluate(sess, x_, y_):
    """评估在某一数据上的准确率和损失"""
    feed_dict = feed_data(x_, y_, 1.0)
    loss, acc = sess.run([model.loss, model.acc], feed_dict=feed_dict)

    return loss, acc

def train():
    print("Configuring TensorBoard and Saver...")
    # 配置 Tensorboard，重新训练时，请将tensorboard文件夹删除，不然图会覆盖
    tensorboard_dir = 'tensorboard/textbinn'
    if not os.path.exists(tensorboard_dir):
        os.makedirs(tensorboard_dir)

    tf.summary.scalar("loss", model.loss)
    tf.summary.scalar("accuracy", model.acc)
    merged_summary = tf.summary.merge_all()
    writer = tf.summary.FileWriter(tensorboard_dir)

    # 配置 Saver
    saver = tf.train.Saver()
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    print("Loading training and validation data...")
    # 载入训练集与验证集
    start_time = time.time()
    batches=data.get_batch_data()
    time_dif = get_time_dif(start_time)
    print("Time usage:", time_dif)

    # 创建session
    session = tf.Session()
    session.run(tf.global_variables_initializer())
    writer.add_graph(session.graph)

    print('Training and evaluating...')
    start_time = time.time()
    total_batch = 0              # 总批次
    best_acc_val = 0.0           # 最佳验证集准确率
    last_improved = 0            # 记录上一次提升批次
    require_improvement = 10000   # 如果超过1000轮未提升，提前结束训练

    flag = False
    for x_batch, y_batch,x_val,y_val in batches:
        feed_dict = feed_data(x_batch, y_batch, conf.dropout_keep_prob)

        if total_batch % conf.save_per_batch == 0:
            # 每多少轮次将训练结果写入tensorboard scalar
            s = session.run(merged_summary, feed_dict=feed_dict)
            writer.add_summary(s, total_batch)

        if total_batch % conf.print_per_batch == 0:
            # 每多少轮次输出在训练集和验证集上的性能
            feed_dict[model.keep_prob] = 1.0
            loss_train, acc_train = session.run([model.loss, model.acc], feed_dict=feed_dict)
            loss_val, acc_val = evaluate(session, x_val, y_val)   # todo

            if acc_val > best_acc_val:
                # 保存最好结果
                best_acc_val = acc_val
                last_improved = total_batch
                saver.save(sess=session, save_path=save_path)
                improved_str = '*'
            else:
                improved_str = ''

            time_dif = get_time_dif(start_time)
            msg = 'Iter: {0:>6}, Train Loss: {1:>6.2}, Train Acc: {2:>7.2%},'\
                + ' Val Loss: {3:>6.2}, Val Acc: {4:>7.2%}, Time: {5} {6}'
            print(msg.format(total_batch, loss_train, acc_train, loss_val, acc_val, time_dif, improved_str))

        session.run(model.optim, feed_dict=feed_dict)  # 运行优化
        total_batch += 1

        if total_batch - last_improved > require_improvement:
            # 验证集正确率长期不提升，提前结束训练
            print("No optimization for a long time, auto-stopping...")
            flag = True
            break  # 跳出循环
    if flag:  # 同上
        print('最佳准确率:',best_acc_val)

if __name__ == '__main__': 
    data=data()  
    model = BiRNN()
    train()