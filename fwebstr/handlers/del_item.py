#!/usr/bin/python
#-*- coding : utf-8 -*-

import sys,os
import tornado.web
from commons.handler import RequestHandler
from commons.logger import logging
from commons import common

class DelItemHandler(RequestHandler):
	def initialize(self,conn):
		self.conn = conn;

	@tornado.gen.coroutine
	@common.json_loads_body
	def post(self):
		try:
			print 'go into ReadTableHandler......';
			if not self.body_json.has_key('tablename'):
				self.except_handle('the param table format error');
				return ;
			table = self.body_json['tablename'];
			word = self.body_json['word'];
			self.conn.get_table(table);
			self.conn.delete_data({"str":word});
			self.write(self.gen_result(0,'insert succ',None));
		except Exception,e:
			self.except_handle(format(e));
			return ;
