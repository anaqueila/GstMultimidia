# -*- coding: utf-8 -*-
#!/usr/bin/env python
#Author: Ana Queila, Jeferson e Uesle

import sys, os

##### Importa a Biblioteca GTK+ #####
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
    

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
		
