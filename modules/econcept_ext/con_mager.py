#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys
import common
from mark_objs import MarkObjs
from combine_objs import CombineObjs
from remark_words import RemarkWords
from con_tail import ConTail
from database import Connect

import struct_utils as Sutil

class ConMager():
	def __init__(self):
		self.tag_objs = list();
		self.conn = Connect();
		self.mark_objs = MarkObjs(self.conn);
		self.combine_objs = CombineObjs();
		self.tail = ConTail();
		self.remark = RemarkWords();

	def init(self,dtype):
		try:
			self.conn.connect('root','root','172.17.0.4','ChinaNet');
			for table in self.conn.get_tables():
				self.tag_objs.append(table);
		except Exception as e:
			raise e;

	def encode(self,struct):
		try:
			self.remove_spaces(struct);
			for obj in self.tag_objs:
				self.mark_objs.encode(struct,obj,'seg_text');
			self.combine_objs.encode(struct);
			self.tail.encode(struct,self.tag_objs);
			self.remark.encode(struct);
			for obj in self.tag_objs:
				self.mark_objs.encode(struct,obj,'seg_text');
			self.combine_objs.encode(struct);
			self.tail.encode(struct,self.tag_objs);
			self._fetch_dkey(struct,'label_final','TIME');
		except Exception as e: raise e;

	def remove_spaces(self,struct):
		try:
			seg_text = list();
			for tstr in struct['seg_text'].split(' '):
				if len(tstr) > 0:
					seg_text.append(tstr);
			struct['seg_text'] = ' '.join(seg_text);
		except Exception as e: raise e;

	def _fetch_dkey(self,struct,ckey,ctype):
		if not struct.has_key(ckey): return None;
		stc = struct['stc'];
		for key in struct[ckey].keys():
			inter = struct[ckey][key];
			istr = key.replace('_','');
			if not ctype is None and not inter.has_key('type'):
				inter['stype'] = ctype;
				inter['type'] = ctype;
			inter['str'] = istr;
			stc[istr] = dict(inter);
		del struct[ckey];
