#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
import tensorflow as tf
import tflearn
from pgportfolio.tools.capsLayer import CapsLayer
import pdb
import numpy as np

class NeuralNetWork:
    def __init__(self, feature_number, rows, columns, layers, device):
        tf_config = tf.ConfigProto()
        self.session = tf.Session(config=tf_config)
        if device == "cpu":
            tf_config.gpu_options.per_process_gpu_memory_fraction = 0
        else:
            tf_config.gpu_options.per_process_gpu_memory_fraction = 0.2
        self.input_num = tf.placeholder(tf.int32, shape=[])
        #print (self.input_num.shape,'================================')
        self.input_tensor = tf.placeholder(tf.float32, shape=[None, feature_number, rows, columns]) # (?,4,5,31)
        self.previous_w = tf.placeholder(tf.float32, shape=[None, rows])
        self._rows = rows
        self._columns = columns

        self.layers_dict = {}
        self.layer_count = 0

        self.output = self._build_network(layers) #(?,12)

    def _build_network(self, layers):
        pass


class CNN_cap(NeuralNetWork):
    # input_shape (features, rows, columns)
    def __init__(self, feature_number, rows, columns, layers, device):
        NeuralNetWork.__init__(self, feature_number, rows, columns, layers, device)
    def add_layer_to_dict(self, layer_type, tensor, weights=True):

        self.layers_dict[layer_type + '_' + str(self.layer_count) + '_activation'] = tensor
        self.layer_count += 1

    # grenrate the operation, the forward computaion
    def _build_network(self, layers):
        network = tf.transpose(self.input_tensor, [0, 2, 3, 1]) #(?,5,31,4)
        # [batch, assets, window, features]
        network = network / network[:, :, -1, 0, None, None] #用最近一个时刻的收盘价数据进行正则化，收盘价应该为最后一列
        # (?,5,31,4)
        for layer_number, layer in enumerate(layers):
            if layer["type"] == "DenseLayer":
                network = tflearn.layers.core.fully_connected(network,
                                                              int(layer["neuron_number"]),
                                                              layer["activation_function"],
                                                              regularizer=layer["regularizer"],
                                                              weight_decay=layer["weight_decay"] )
                
                self.add_layer_to_dict(layer["type"], network)
            elif layer["type"] == "DropOut":
                network = tflearn.layers.core.dropout(network, layer["keep_probability"])

            elif layer["type"] == "EIIE_Dense":
                #print (layer,'===========================')
                width = network.get_shape()[2] # 16
                network = tflearn.layers.conv_2d(network, int(layer["filter_number"]),
                                                 [1, width],
                                                 [1, 1],
                                                 "valid",
                                                 layer["activation_function"],
                                                 regularizer=layer["regularizer"],
                                                 weight_decay=layer["weight_decay"]) #(?,5,1,10)
                self.add_layer_to_dict(layer["type"], network)
                # (?, 960, 1, 10)
            elif layer["type"] == "EI3":
                """
                paper: A Multi-Scale Temporal Feature Aggregation Convolutional Neural Network for Portfolio Management
                """
                # short feature
                network = tf.transpose(network, [0, 3, 2, 1]) #(?, feature_num, window_size, asset_num)
                filter_num = int(self.input_tensor.shape[2])
                feature1 = tflearn.layers.conv_2d(network, filter_num, [1,3], [1,1], "valid", "relu", bias=True, weights_init="Xavier", bias_init="Xavier")
                feature11 = tflearn.layers.conv_2d(feature1, filter_num, [1, 48], [1,1], "valid", "relu", bias=True, weights_init="Xavier", bias_init="Xavier")               
                # medium feature
                feature2 = tflearn.layers.conv_2d(network, filter_num, [1,21], [1,1], "valid", "relu", bias=True, weights_init="Xavier", bias_init="Xavier")
                feature21 = tflearn.layers.conv_2d(feature2, filter_num, [1,30], [1,1], "valid", "relu", bias=True, weights_init="Xavier", bias_init="Xavier")
                # maxpooling提取特征
                feature3 = tflearn.layers.conv.max_pool_2d(network, [1, 50], [1,1], "valid")
                # concate
                feature = tf.concat([feature11, feature21], 1)
                feature = tf.concat([feature, feature3], 1)
                # concate with the previous weight
                self.previous_w1 = self.previous_w[:, None, None, :]
                feature = tf.concat([feature, self.previous_w1], 1)
                # 1*1 conv layer
                feature = tflearn.layers.conv_2d(feature, filter_num, [10,1], [1,1], "valid", "relu", bias=True, weights_init="Xavier", bias_init="Xavier")
                feature_sq = tf.squeeze(feature, [1,2])
                # add cash 
                cash_bias = tf.ones((self.input_num, 1))
                feature_all = tf.concat([feature_sq, cash_bias], 1)
                network = tflearn.layers.core.activation(feature_all, activation="softmax")
                self.add_layer_to_dict('softmax_layer', network, weights=False)

            elif layer["type"] == "ConvLayer":
                #print (layer,'=============ConvLayer')
                network = tflearn.layers.conv_2d(network, int(layer["filter_number"]),
                                                 allint(layer["filter_shape"]),
                                                 allint(layer["strides"]),
                                                 layer["padding"],
                                                 layer["activation_function"],
                                                 regularizer=layer["regularizer"],
                                                 weight_decay=layer["weight_decay"])
                self.add_layer_to_dict(layer["type"], network)
                
            elif layer["type"] == "MaxPooling":
                network = tflearn.layers.conv.max_pool_2d(network, layer["strides"])
            elif layer["type"] == "AveragePooling":
                network = tflearn.layers.conv.avg_pool_2d(network, layer["strides"])
            elif layer["type"] == "LocalResponseNormalization":
                network = tflearn.layers.normalization.local_response_normalization(network)
            elif layer["type"] == "EIIE_Output":
                width = network.get_shape()[2]
                network = tflearn.layers.conv_2d(network, 1, [1, width], padding="valid",
                                                 regularizer=layer["regularizer"],
                                                 weight_decay=layer["weight_decay"])
                self.add_layer_to_dict(layer["type"], network)
                network = network[:, :, 0, 0]
                cash_bias = tf.ones((self.input_num, 1))
                self.add_layer_to_dict(layer["type"], network)
                network = tf.concat([cash_bias, network], 1)
                network = tflearn.layers.core.activation(network, activation="softmax")
                self.add_layer_to_dict(layer["type"], network, weights=False)
            elif layer["type"] == "Output_WithW":
                network = tflearn.flatten(network)
                network = tf.concat([network,self.previous_w], axis=1)
                network = tflearn.fully_connected(network, self._rows+1,
                                                  activation="softmax",
                                                  regularizer=layer["regularizer"],
                                                  weight_decay=layer["weight_decay"])
            elif layer["type"] == "EIIE_Output_WithW":
                #print (layer,'============EIIE_OUTPUT_Layer')
                width = network.get_shape()[2]
                height = network.get_shape()[1]
                features = network.get_shape()[3]
                network = tf.reshape(network, [self.input_num, int(height), 1, int(width*features)]) #(?,5,1,10)
                #print (self.previous_w,'==============previous_w============')
                w = tf.reshape(self.previous_w, [-1, int(height), 1, 1]) # (?, 5, 1, 1)
                network = tf.concat([network, w], axis=3) # (?, 5, 1, 11)
                network = tflearn.layers.conv_2d(network, 1, [1, 1], padding="valid",
                                                 regularizer=layer["regularizer"],
                                                 weight_decay=layer["weight_decay"]) #(?,5,1,1)
                
                self.add_layer_to_dict(layer["type"], network)
                network = network[:, :, 0, 0] #(?,5)
                #btc_bias = tf.zeros((self.input_num, 1))
                cash_bias = tf.get_variable("cash_bias", [1, 1], dtype=tf.float32,
                                       initializer=tf.zeros_initializer) #(?,1)
                cash_bias = tf.tile(cash_bias, [self.input_num, 1])
                network = tf.concat([cash_bias, network], 1) # (?,6)
                self.voting = network
                self.add_layer_to_dict('voting', network, weights=False)
                network = tflearn.layers.core.activation(network, activation="softmax") # (?,6)
                self.add_layer_to_dict('softmax_layer', network, weights=False)

            elif layer["type"] == "EIIE_LSTM" or\
                            layer["type"] == "EIIE_RNN" or layer["type"] == 'EIIE_GRU':
                network = tf.transpose(network, [0, 2, 3, 1])
                resultlist = []
                reuse = False
                for i in range(self._rows):
                    if i > 0:
                        reuse = True
                    if layer["type"] == "EIIE_LSTM":
                        result = tflearn.layers.recurrent.lstm(network[:, :, :, i],
                                                     int(layer["neuron_number"]),
                                                     #dropout=layer["dropouts"],
                                                     scope="lstm"+str(layer_number),
                                                     reuse=reuse)
                    elif layer["type"] == "EIIE_RNN":
                        result = tflearn.layers.recurrent.simple_rnn(network[:, :, :, i],
                                                           int(layer["neuron_number"]),
                                                           #dropout=layer["dropouts"],
                                                           scope="rnn"+str(layer_number),
                                                           reuse=reuse)
                    elif layer["type"] == "EIIE_GRU":
                        result = tflearn.layers.gru(network[:, :, :, i],
                                                           int(layer["neuron_number"]),
                                                           #dropout=layer["dropouts"],
                                                           scope="gru"+str(layer_number),
                                                           reuse=reuse)
                    resultlist.append(result)
                
                network = tf.stack(resultlist) # (5,?,20)
                network = tf.transpose(network, [1, 0, 2])
                network = tf.reshape(network, [-1, self._rows, 1, int(layer["neuron_number"])])

            elif layer["type"] == "capsule_layer":                
                # Primary Capsules layer, return tensor with shape [batch_size, 1152, 8, 1]  
                primaryCaps = CapsLayer(num_outputs=int(layer["filter_number"]), vec_len=int(layer["vec_len"]), 
                                        with_routing=layer["with_routing"], layer_type=layer["layer_type"])
                network_caps = primaryCaps(network, kernel_size=int(layer["filter_size"]), stride=int(layer["strides"]))
                self.add_layer_to_dict('capsule_CNN', network_caps)
                digitCaps = CapsLayer(num_outputs=self._rows, vec_len=int(layer["vec_len_fc"]), with_routing=True, layer_type='FC')
                network = digitCaps(network_caps)  #(?,5,16,1)
                self.add_layer_to_dict("capsule_FC", network)
                # (?, 960, 8, 1)
            else:
                raise ValueError("the layer {} not supported.".format(layer["type"]))
        return network


def allint(l):
    if type(l) == list:
        return [int(i) for i in l]
    else:
        return int(l)

