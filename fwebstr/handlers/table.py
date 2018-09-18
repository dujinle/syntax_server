#!/usr/bin/python
#-*- coding : utf-8 -*-

import sys,os
import tornado.web
from commons.handler import RequestHandler
from commons.logger import logging

class TableHandler(RequestHandler):

	def get(self):
		table = self.get_argument("tablename", "default");
		self.render('table.html',tablename=table);
