from gevent import monkey
monkey.patch_all()

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s  %(levelname)s  %(filename)s  '
                           '[%(lineno)d]  thread: %(threadName)s  %(funcName)s  msg: %(message)s',
                    datefmt='[%Y-%m-%d %H:%M:%S]',
                    filename='./log/run.log',
                    filemode='ab+')


from flask import Flask, request
app = Flask(__name__)

import view
