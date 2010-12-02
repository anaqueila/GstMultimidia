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


class Convertevf(object):

	def on_executar_clicked(self, widget, Data=None):
		if self.player.get_state()[1] == gst.STATE_NULL:
			filepath = self.fcb.get_filename()
			filepath2 = self.fcb2.get_filename()
			name = filepath.split("/")[-1]
			print filepath
			print filepath2
			print name
			if os.path.isfile(filepath):
				self.source.set_property("location", filepath)
				self.sink.set_property("location", filepath2 + "/" + "output-%05d.png")
				self.player.set_state(gst.STATE_PLAYING)
	
	def on_sair_clicked(self, widget, Data=None):
		self.janela.hide_all()
		
	arquivoglade = "ConverteVF.glade"
	
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
		self.source = gst.element_factory_make("filesrc")
		decoder = gst.element_factory_make("decodebin")
		decoder.connect("new-decoded-pad", self.decoder_callback)
		colorspace = gst.element_factory_make("ffmpegcolorspace", "video-sink")
		encoder = gst.element_factory_make("pngenc")
		encoder.set_property("snapshot", False)
		self.sink = gst.element_factory_make("multifilesink")
		
		self.player.add(self.source, decoder, colorspace, encoder, self.sink)
		gst.element_link_many(self.source, decoder)
		gst.element_link_many(colorspace, encoder, self.sink)
		
		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect("message", self.on_message)
		
		gtk.main()

	# Decoder callback, used to link video pad to sink
	def decoder_callback(self, decoder, pad, data):
		structure_name = pad.get_caps()[0].get_name()
		print structure_name
		if structure_name.startswith("video"):
			video_pad = self.player.get_by_name("video-sink").get_pad("sink")
			pad.link(video_pad)
		
	def on_message(self, bus, message):
		t = message.type
		print t
		if t == gst.MESSAGE_EOS:
			self.player.set_state(gst.STATE_NULL)

		elif t == gst.MESSAGE_ERROR:
			err, debug = message.parse_error()
			print "Error: %s" % err, debug
			self.player.set_state(gst.STATE_NULL)

