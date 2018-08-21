#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys
import common
from myexception import MyException

class ConTail():

	def init(self,dtype): pass;

	def encode(self,struct,tables):
		try:
			if not struct.has_key('stc'): struct['stc'] = dict();

			for key in tables:
				if not struct.has_key(key): continue;
				self.fetch_cept(struct['stc'],struct[key]);
				del struct[key];
			self._fetch_dkey(struct,'SomeNum',None);
			self._fetch_ckey(struct,'SomeEngs',None);
			self._fetch_ckey(struct,'SomeNunit',None);

		except Exception as e:
			raise MyException(sys.exc_info());

	def fetch_cept(self,stc,cepts):
		for ib in cepts:
			istr = ib['str'];
			stc[istr] = dict(ib);

	def _fetch_ckey(self,struct,ckey,ctype):
		if not struct.has_key(ckey): return None;
		stc = struct['stc'];
		for inter in struct[ckey]:
			istr = inter['str'].replace('_','');
			if not ctype is None:
				inter['stype'] = ctype;
				inter['type'] = ctype;
			inter['str'] = istr;
			stc[istr] = dict(inter);
		del struct[ckey];

	def _fetch_dkey(self,struct,ckey,ctype):
		if not struct.has_key(ckey): return None;
		stc = struct['stc'];
		for key in struct[ckey].keys():
			inter = struct[ckey][key];
			istr = key.replace('_','');
			if not ctype is None:
				inter['stype'] = ctype;
				inter['type'] = ctype;
			inter['str'] = istr;
			stc[istr] = dict(inter);
		del struct[ckey];
