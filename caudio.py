# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys, os, thread

##### Importa a Biblioteca GTK+ #####
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
    
### Importa a Biblioteca GObject ###

import gobject
gobject.threads_init()

### Importa a Biblioteca Gstreamer ###

import pygst
pygst.require('0.10')
import gst

	

class Caudio(object):


	def on_record_clicked(self, widget, data=None):
		if self.player.get_state()[1] == gst.STATE_NULL:
			filepath = self.fcb.get_filename()
			name = self.entry.get_text() + ".ogg"
			print filepath
			print name
			if os.path.isdir(filepath):
				print "sim"
	 			self.sink.set_property("location", filepath + "/" + name)
				self.player.set_state(gst.STATE_PLAYING)
			

	def on_stop_clicked(self, widget, data=None):

		if self.player.get_state()[1] == gst.STATE_PLAYING:
			self.player.set_state(gst.STATE_NULL)
			print "fim"
		else:
			print "nao tem fluxo"
				

	def on_quit_clicked(self, widget, data=None):
		self.janela.hide()
		#gtk.main_quit()

	#def on_janela_destroy(self, widget, data=None):
		#self.janela.hide()
		#gtk.main_quit()


	arquivoglade = "CapturaA.glade"
	
	def __init__ (self):

		builder = gtk.Builder()
		builder.add_from_file(self.__class__.arquivoglade)
		#carregando janela
		self.janela = builder.get_object("janela")
		self.fcb = builder.get_object("fcb")
		self.entry = builder.get_object("entry")
		builder.connect_signals(self)

		self.janela.show_all()

		self.player = gst.Pipeline("MyPlayer")
		source = gst.element_factory_make("osssrc", "source")
		convert = gst.element_factory_make("audioconvert",'audioconvert')
		enc = gst.element_factory_make("vorbisenc","encoder")	
		mux = gst.element_factory_make("oggmux", "mux")	
		self.sink = gst.element_factory_make("filesink","sink")
		
		self.player.add(source,convert,enc,mux,self.sink)
		gst.element_link_many(source,convert,enc,mux,self.sink)

		bus = self.player.get_bus()
		print bus
		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect("message", self.on_message)

		gtk.main()

	def on_message(self, bus, message):
		t = message.type
		print t
		if t == gst.MESSAGE_EOS:
			self.player.set_state(gst.STATE_NULL)
		elif t == gst.MESSAGE_ERROR:
			self.player.set_state(gst.STATE_NULL)
			err, debug = message.parse_error()
			print "Error: %s" % err, debug

