#!/usr/bin/python
#-*- coding : utf-8 -*-

import sys,os
import tornado.web
from commons.handler import RequestHandler
from commons.logger import logging
from commons import common

class ReadListHandler(RequestHandler):
	def __init__(self,*args, **kwargs):
		RequestHandler.__init__(self, *args, **kwargs);

	def initialize(self,conn):
		try:
			self.conn = conn;
		except Exception as e: raise e;

	@tornado.gen.coroutine
	@common.json_loads_body
	def post(self):
		try:
			print 'go into ReadListHandler......';
			if not self.body_json.has_key('level'):
				self.except_handle('the param level format error');
				return ;
			level = self.body_json['level'];
			tables = self.conn.get_tables();
			del tables[0];
			print tables;
			rec_dic = dict();
			rec_dic['tables'] = tables;
			rec_dic['dot'] = dict();
			for table in tables:
				self.conn.get_table(table);
				res = self.conn.query_data({'track_num':{'$lte':level}});
				print '........',res.count();
				for item in res:
					if item.has_key('_id'):
						del item['_id'];
					if rec_dic['dot'].has_key(item['str']):
						continue;
					else:
						rec_dic['dot'][item['str']] = item;
			for key in rec_dic['dot'].keys():
				item = rec_dic['dot'][key];
				if len(item['track']) > 0:
					idx = len(item['track']) - 1;
					tail = item['track'][idx];
					if not rec_dic['dot'][tail].has_key('child'):
						rec_dic['dot'][tail]['child'] = list();
					rec_dic['dot'][tail]['child'].append(item);
			self.write(self.gen_result(0,'succ',rec_dic));
		except Exception,e:
			self.except_handle(format(e));
			return ;
