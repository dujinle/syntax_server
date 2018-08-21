#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
reload(sys);
sys.setdefaultencoding('utf-8');
import collections

#==============================================================
''' import tagpy wordsegs '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'./commons'));
#==============================================================

import common
from modules import *

class Mager:
	def __init__(self):
		self.wordseg = WordSeg();
		self.timer = TimeMager();
		self.pdeal = PrevMager();
		self.concpt = ConMager();

		self.struct = collections.OrderedDict();
		self.modules = dict();

	def init(self):
		try:
			self.timer.init();
			self.pdeal.init('PDeal');
			self.concpt.init('Concept');
		except Exception as e:
			raise e;

	def _clear_struct(self,struct):
		if struct.has_key('stseg'): del struct['stseg'];
		if struct.has_key('stc'): del struct['stc'];
		if struct.has_key('SomeNum'): del struct['SomeNum'];
		if struct.has_key('result'): del struct['result'];
		if struct.has_key('TimeLabel'): del struct['TimeLabel'];
		if struct.has_key('label_final'): del struct['label_final'];

	def encode(self,text,mdl = None):
		self._clear_struct(self.struct);
		self.struct['text'] = text;
		self.struct['label_final'] = dict();
		self.pdeal.encode(self.struct);

		self.struct['seg_text'] = self.wordseg.tokens(self.struct['text']);
		self.struct['otext'] = self.struct['text'];
		self.struct['result'] = dict();

		self.timer.encode(self.struct);

		self.concpt.encode(self.struct);
		return self.struct;
common.debug = False;

if common.debug == True:
	try:
		mg = Mager();
		mg.init();
		while True:
			istr = raw_input("raw_input: ");
			if istr == 'q' or istr == 'bye': break;
			print istr;
			sarr = istr.decode('utf8').split(' ');
			if len(sarr) == 2:
				common.print_dic(mg.encode(sarr[0],sarr[1]));
			elif len(sarr) == 3:
				common.print_dic(mg.encode(sarr[0],sarr[1],sarr[2]));
			else:
				common.print_dic(mg.encode(sarr[0]));
	except Exception as e:
		raise e;
