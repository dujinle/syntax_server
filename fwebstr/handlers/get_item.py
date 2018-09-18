#!/usr/bin/python
#-*- coding : utf-8 -*-

import sys,os
import tornado.web
from commons.handler import RequestHandler
from commons.logger import logging
from commons import common

class GetItemHandler(RequestHandler):
	def initialize(self,conn):
		self.conn = conn;

	@tornado.gen.coroutine
	@common.json_loads_body
	def post(self):
		try:
			print 'go into GetItemHandler......';
			if not self.body_json.has_key('words'):
				self.except_handle('the param words format error');
				return ;
			word = self.body_json['words'];
			if not self.body_json.has_key('tablename'):
				self.except_handle('the param tablename format error');
				return ;
			table = self.body_json['tablename'];
			rec_dic = dict();
			self.conn.get_table(table);
			res = self.conn.query_data({"str":word});
			print '........',res.count();
			for item in res:
				print item
				if item.has_key('_id'): del item['_id'];
				if rec_dic.has_key(item['str']): continue;
				else:
					rec_dic[item['str']] = item;
			self.write(self.gen_result(0,'get succ',rec_dic));
		except Exception,e:
			self.except_handle(format(e));
			return ;
