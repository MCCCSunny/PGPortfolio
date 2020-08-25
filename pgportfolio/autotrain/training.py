from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import os
import time
from multiprocessing import Process
from pgportfolio.learn.tradertrainer import TraderTrainer
from pgportfolio.tools.configprocess import load_config
import pdb

def train_one(save_path, config, log_file_dir, index, logfile_level, console_level, device):
    """
    train an agent
    :param save_path: the path to save the tensorflow model (.ckpt), could be None
    :param config: the json configuration file
    :param log_file_dir: the directory to save the tensorboard logging file, could be None
    :param index: identifier of this train, which is also the sub directory in the train_package,
    if it is 0. nothing would be saved into the summary file.
    :param logfile_level: logging level of the file
    :param console_level: logging level of the console
    :param device: 0 or 1 to show which gpu to use, if 0, means use cpu instead of gpu
    :return : the Result namedtuple
    """
    if log_file_dir:
        logging.basicConfig(filename=log_file_dir.replace("tensorboard","programlog"),
                            level=logfile_level)
        console = logging.StreamHandler()
        console.setLevel(console_level)
        logging.getLogger().addHandler(console)
    else:    
        print ('log_file_dir is not existent')
    print("training at %s started" % index)
    pdb.set_trace()
    trainer = TraderTrainer(config, save_path=save_path, device=device) #初始化训练器
    return trainer.train_net(log_file_dir=log_file_dir, index=index) #训练网络

