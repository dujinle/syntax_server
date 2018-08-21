#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
from myexception import MyException
import hanzi2num as Han2Dig
import struct_utils as Sutil
#处理数字单位的组合
class CombineObjs():

	def load_data(self,dfile): pass;

	def encode(self,struct):
		try:
#			self._fetch_num(struct);
			self._fetch_eng(struct);
			self._fetch_num_unit(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _fetch_num(self,struct):
		if not struct.has_key('SomeNums'): struct['SomeNums'] = list();
		words = struct['text'];
		comp = re.compile('[0-9.]+');
		matchs = comp.findall(words);
		if matchs is None: return False;
		for match in matchs:
			tdic = dict();
			tdic['type'] = 'NUM';
			tdic['stype'] = match;
			tdic['str'] = match;
			struct['SomeNums'].append(tdic);

	def _fetch_eng(self,struct):
		if not struct.has_key('SomeEngs'): struct['SomeEngs'] = list();
		words = struct['text'];
		comp = re.compile('[a-zA-Z]+');
		matchs = comp.findall(words);
		if matchs is None: return False;
		for match in matchs:
			tdic = dict();
			tdic['type'] = 'ENG';
			tdic['stype'] = match;
			tdic['str'] = match;
			struct['SomeEngs'].append(tdic);

	def _fetch_num_unit(self,struct):
		if not struct.has_key('SomeNum'): return -1;
		if not struct.has_key('SomeUnits'): return -1;
		if not struct.has_key('SomeNunit'): struct['SomeNunit'] = list();
		for num_key in struct['SomeNum'].keys():
			num = struct['SomeNum'][num_key];
			for vit in struct['SomeUnits']:
				pstr = num_key + vit['str'];
				ppstr = ' {0,}'.join(list(pstr));
				comp = re.compile(ppstr);
				match = comp.search(struct['seg_text']);
				if not match is None:
					pstr = match.group(0);
					tdic = dict();
					tdic['str'] = pstr.replace(' ','');
					tdic['type'] = 'NUNIT';
					tdic['stype'] = 'NUNIT';
					tdic['stc'] = [num,vit];
					struct['SomeNunit'].append(tdic);
					struct['seg_text'] = struct['seg_text'].replace(pstr,' ' + tdic['str'] + ' ',1);
					num['match'] = True;
					vit['match'] = True;

		num_dic = dict();
		for num_key in struct['SomeNum'].keys():
			num = struct['SomeNum'][num_key];
			if num.has_key('match') and num['match'] == True:
				continue;
			else:
				num_dic[num_key] = num;
		struct['SomeNum'] = num_dic;

		unit_list = list();
		for vit in struct['SomeUnits']:
			if vit.has_key('match') and vit['match'] == True:
				continue;
			else:
				unit_list.append(vit);
		struct['SomeUnits'] = unit_list;

