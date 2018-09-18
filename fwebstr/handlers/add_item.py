#!/usr/bin/python
#-*- coding : utf-8 -*-

import sys,os,json
import tornado.web
from commons.handler import RequestHandler
from commons.logger import logging
from commons import common

class AddItemHandler(RequestHandler):

	def initialize(self,conn):
		self.conn = conn;

	@tornado.gen.coroutine
	@common.json_loads_body
	def post(self):
		try:
			print 'go into AddItemHandler......';
			if not self.body_json.has_key('tablename'):
				self.except_handle('the param table format error');
				return ;
			table = self.body_json['tablename'];
			item = self.body_json['item'];
			parent = self.body_json['parent'];
			print table,item,parent;
			self.conn.get_table(table);
			res = self.conn.query_data({"str":parent});
			if not item.has_key('type'):
				self.except_handle('no found type param');
				return ;
			if not item.has_key('stype'):
				self.except_handle('no found stype param');
				return ;
			for pitem in res:
				print pitem['track'],type(pitem['track']);
				item['track'] = list();
				item['track'].extend(pitem['track'])
				item['track'].append(parent);
				item['track_num'] = len(item['track']);
				break;
			common.print_dic(item);
			self.conn.insert_data(item);
			self.write(self.gen_result(0,'insert succ',item));
		except Exception,e:
			self.except_handle(format(e));
			return ;
