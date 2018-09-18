#!/usr/bin/python
#-*- coding : utf-8 -*-

import sys,os
#=============================================
''' import common module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../commons'));
#=============================================

import tornado.web
from logger import *
import common
from handler import RequestHandler

class NlpProcessHandler(RequestHandler):

	def __init__(self,*args, **kwargs):
		RequestHandler.__init__(self, *args, **kwargs);

	def initialize(self,mager):
		self.mager = mager;

	@tornado.gen.coroutine
	@common.json_loads_body
	def post(self):
		try:
			itest = None;
			if not self.body_json.has_key('text'):
				self.except_handle('the url data format error');
				return ;
			itest = self.body_json['text'];
			if len(itest) == 0:
				self.except_handle('the param text is empty');
				return ;
			logging.info('input:%s' %(itest));
			sres = self.mager.encode(itest,None);
			logging.info(common.get_dicstr(sres));
			self.write(self.gen_result(0,'enjoy success',sres));
		except Exception as e:
			logging.error(str(e));
			raise e;
