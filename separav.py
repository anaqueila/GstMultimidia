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

class Separav(object):

	def on_iniciar_clicked(self, widget, Data=None):
		if self.player.get_state()[1] == gst.STATE_NULL:
			filepath = self.fcb.get_filename()
			filepath2 = self.fcb2.get_filename()
			name = filepath.split("/")[-1]
			if os.path.isfile(filepath):
				self.source.set_property("location", filepath)
				self.sink.set_property("location", filepath2 + "/" + name)
				self.player.set_state(gst.STATE_PLAYING)

	def on_stop_clicked(self, widget, Data=None):
		if self.player.get_state()[1] == gst.STATE_PLAYING:
			self.player.set_state(gst.STATE_NULL)
		
	def on_sair_clicked(self, widget, Data=None):
		self.janela.hide_all()
		

	arquivoglade = "Separav.glade"
	
	def __init__ (self):

		builder = gtk.Builder()
		builder.add_from_file(self.__class__.arquivoglade)
		#conectando os sinais
		builder.connect_signals(self)
		#carregando janela
		self.janela = builder.get_object("janela")
		self.fcb = builder.get_object("filechooserbutton1")
		self.fcb2 = builder.get_object("filechooserbutton2")
		self.janela.show_all()
		
		self.player = gst.Pipeline("MyPlayer")
		self.source = gst.element_factory_make("filesrc", "source")
		demux = gst.element_factory_make("oggdemux", "demuxer")
		demux.connect("pad-added", self.demuxer_callback)
		self.queue = gst.element_factory_make("queue","audqueue")
		decoder = gst.element_factory_make("vorbisdec", "decoder")
		encoder = gst.element_factory_make("vorbisenc", "encoder")
		muxer = gst.element_factory_make("oggmux", "muxer")
		self.sink = gst.element_factory_make("filesink", "sink")
		
		self.player.add(self.source,demux,self.queue,decoder,encoder,muxer,self.sink)
		gst.element_link_many(self.source,demux)
		gst.element_link_many(self.queue,decoder,encoder,muxer,self.sink)
		
		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect("message", self.on_message)
		
		gtk.main()
		
	def demuxer_callback(self, demuxer, pad):
		structure_name = pad.get_caps()[0].get_name()
		if structure_name.startswith("audio"):
			queuea_pad = self.queue.get_pad("sink")
			pad.link(queuea_pad)
		
	def on_message(self, bus, message):
		t = message.type
		print t
		if t == gst.MESSAGE_EOS:
			self.player.set_state(gst.STATE_NULL)

		elif t == gst.MESSAGE_ERROR:
			err, debug = message.parse_error()
			print "Error: %s" % err, debug
			self.player.set_state(gst.STATE_NULL)

