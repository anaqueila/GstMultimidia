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



from caudio import * 
from reproduz import *
from convertevf import *
from convertV import *
from desktop import *
from webchoose import *
from separav import *
		

class Tinicial():

	def on_reproduz_clicked(self, event):
		objct = Reproduz()

	def on_janela_destroy(self, event):
		sys.exit(1)

	def on_quit_clicked(self, event):
		sys.exit(1)
	
	def on_convertevf_clicked(self, event):
		objct = Convertevf()
		pass
	def on_web_clicked(self, event):
		objct = Webchoose()

	def on_cvideo_clicked(self, event):
		objct = Convertv()

	def on_separa_clicked(self, event):
		sv = Separav()

	def on_rvideo_clicked(self, event):
		sys.exit(1)

	def on_caudio_clicked(self, event):
		objct = Caudio()

	def on_captura_clicked(self, widget, Data=None):
		self.janela.iconify()
		objct = Desktop()
		
		
	#Importa o arquivo da interface
	arquivoglade = "Tinicial.glade"

	def __init__(self):

		#criando builder
		builder = gtk.Builder()
		#carregando arquivo do glade no builder
		builder.add_from_file(self.__class__.arquivoglade)
		#carregando janela
		self.janela = builder.get_object("janela")
		#conectando os sinais
		builder.connect_signals(self)
		#Exibe toda interface
		self.janela.show_all()
		
		#chama a função de inicialização da classe gtk
		gtk.main()
	
	#gtk.gdk.notify_startup_complete()

if __name__ == "__main__":
	
	t = Tinicial()
