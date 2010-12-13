# -*- coding: utf-8 -*-
#!/usr/bin/env python
#Author: Ana Queila, Jeferson e Uesle

import sys, os

##### Importa a Biblioteca GTK+ #####
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
    
### Importa a Biblioteca Gstreamer ###

import pygst
pygst.require('0.10')
import gst

class Webcam():
	
	def on_play_clicked(self, widget, data=None): 

		if self.player.get_state()[1] == gst.STATE_NULL:
			self.player.set_state(gst.STATE_PLAYING)

	def on_stop_clicked(self, widget, data=None):
		if self.player.get_state()[1] == gst.STATE_PLAYING:
			self.player.set_state(gst.STATE_NULL)
			print "End"
		else:
			print "nao ha nada tocando"

	def on_finish_clicked(self, widget, data=None):
		self.janela.hide_all()
		
	def on_janela_destroy(self, widget, data=None):
		self.player.set_state(gst.STATE_NULL)
		gtk.main_quit()
		

	arquivoglade = "webcam.glade"
	
	def __init__ (self):
		
		
		#criando builder
		builder = gtk.Builder()
		#carregando arquivo do glade no builder
		builder.add_from_file(self.__class__.arquivoglade)
		
		#carregando janela
		self.janela = builder.get_object("janela")
		#Carregando o DrawingArea
		self.movie_window = builder.get_object("movie_window")
		#conectando os sinais
		builder.connect_signals(self)
		#Exibe toda interface
		self.janela.show_all()
		
		# Set up the gstreamer pipeline
		self.player = gst.parse_launch ("v4l2src ! video/x-raw-yuv, framerate=(fraction)30/1 ! ffmpegcolorspace ! xvimagesink")	


		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect("message", self.on_message)
		bus.connect("sync-message::element", self.on_sync_message)
		
		self.movie_window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(red=0, green=0, blue=0, pixel=65535))
		
		gtk.gdk.threads_init()
		gtk.main()

	gtk.gdk.notify_startup_complete()


	def on_message(self, bus, message):
		t = message.type
		print t
		if t == gst.MESSAGE_EOS:
			self.player.set_state(gst.STATE_NULL)

		elif t == gst.MESSAGE_ERROR:
			err, debug = message.parse_error()
			print "Error: %s" % err, debug
			self.player.set_state(gst.STATE_NULL)
			

	def on_sync_message(self, bus, message):
		if message.structure is None:
			return
		message_name = message.structure.get_name()
		if message_name == "prepare-xwindow-id":
			# Assign the viewport
			imagesink = message.src
			imagesink.set_property("force-aspect-ratio", True)
			gtk.gdk.threads_enter()
			imagesink.set_xwindow_id(self.movie_window.window.xid)
			gtk.gdk.threads_leave()
