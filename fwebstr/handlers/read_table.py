#!/usr/bin/python
#-*- coding : utf-8 -*-

import sys,os
import tornado.web
from commons.handler import RequestHandler
from commons.logger import logging
from commons import common


class ReadTableHandler(RequestHandler):
	def initialize(self,conn):
		try:
			self.conn = conn
		except Exception as e: raise e;

	@tornado.gen.coroutine
	@common.json_loads_body
	def post(self):
		try:
			print 'go into ReadTableHandler......';
			if not self.body_json.has_key('tablename'):
				self.except_handle('the param table format error');
				return ;

			header_name = None;
			if self.body_json.has_key('header_name'):
				header_name = self.body_json['header_name'];

			table = self.body_json['tablename'];
			rec_dic = dict();
			rec_dic['dot'] = dict();
			self.conn.get_table(table);
			res = self.conn.query_data(None);
			print '........',res.count();
			for item in res:
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
			##find the header may be it has more than one
			headers = dict(rec_dic['dot']);
			keys = list();
			keys.extend(headers.keys());
			for key in headers.keys():
				item = headers[key];
				if item.has_key('child'):
					for child in item['child']:
						if child['str'] in keys:
							idx = keys.index(child['str']);
							del keys[idx];
				else:
					if item['str'] in keys:
						idx = keys.index(item['str']);
						del keys[idx];
			dot = None;
			if header_name is None or header_name == 'none':
				if len(keys) == 0:
					dot = common.graph_dot_dict(rec_dic['dot'],None);
				else:
					dot = common.graph_dot_dict(rec_dic['dot'],keys[0]);
			else:
				dot = common.graph_dot_dict(rec_dic['dot'],header_name);

			self.write(self.gen_result(0,'get succ',{"keys":keys,"dot":dot}));
			'''

			dot = common.graph_dot_dict(rec_dic['dot'],table);
			del rec_dic['dot'];
			rec_dic['dot'] = dot;
			self.write(self.gen_result(0,'get succ',rec_dic));
			'''
		except Exception,e:
			self.except_handle(format(e));
			return ;
