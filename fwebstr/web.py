#!/usr/bin/python
#-*- coding : utf-8 -*-
#
import sys,os
import tornado.ioloop
import tornado.web

base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../'));

from mager import Mager
from handlers import *
from database import Connect

class Application(tornado.web.Application):
	def __init__(self):
		self.mager = Mager();
		self.mager.init();
		self.conn = Connect();
		self.conn.connect('root','root','172.17.0.4','ChinaNet');
		handlers = [
			(r"/get_result",ResultHandler,{'mager':self.mager}),
			(r"/nlp",NlpHandler),
			(r"/nlp_process",NlpProcessHandler,{'mager':self.mager}),
			(r"/",IndexHandler),
			(r"/index",IndexHandler),
			(r"/table",TableHandler),
			(r"/readlist",ReadListHandler,{'conn':self.conn}),
			(r"/readtable",ReadTableHandler,{'conn':self.conn}),
			(r"/getitem",GetItemHandler,{'conn':self.conn}),
			(r"/additem",AddItemHandler,{'conn':self.conn}),
			(r"/delitem",DelItemHandler,{'conn':self.conn})

		];
		settings = dict(
				template_path = os.path.join(os.path.dirname(__file__),"templates"),
				static_path = os.path.join(os.path.dirname(__file__),"static"),
				debug = True,
		);
		tornado.web.Application.__init__(self, handlers, **settings);

if __name__=="__main__":

	port = sys.argv[1];
	server = Application();
	server.listen(port);
	tornado.ioloop.IOLoop.instance().start();
