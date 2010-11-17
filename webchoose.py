# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys, os
import os.path
import pygtk, gtk
import gobject
gobject.threads_init()

import gtk.glade


import pygst
pygst.require("0.10")
import gst


from webcam import *
from webcamg import *


class Webchoose():

	def on_usar_clicked (self, event):
		self.janela.iconify()
		web = Webcam()
		
	def on_gravar_clicked (self, event):
		g = Grava()

	arquivoglade = "webchoose.glade"
	
	def __init__ (self):
	
		builder = gtk.Builder()
		builder.add_from_file(self.__class__.arquivoglade)
		self.janela = builder.get_object("janela")
		builder.connect_signals(self)
		self.janela.show_all()
		
		gtk.main()
		
