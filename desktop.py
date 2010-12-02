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


class Desktop(object):

	def on_stop_clicked(self,event):
		if self.player.get_state()[1] == gst.STATE_PLAYING:
			self.player.set_state(gst.STATE_NULL)
			print "End"
		else:
			print "nao ha nada tocando"
		
	def on_quit_clicked(self,event):
		self.janela.hide()
		
	def on_record_clicked(self,widget, data=None):
		if self.player.get_state()[1] == gst.STATE_NULL:
			filepath = self.fcb.get_filename()
			name = self.campo.get_text() + ".flv"
			if os.path.isdir(filepath):
				self.sink.set_property("location", filepath + "/" + name)
				self.player.set_state(gst.STATE_PLAYING)
				self.janela.iconify()

	arquivoglade = "CapturaD.glade"
	
	def __init__ (self):

		builder = gtk.Builder()
		builder.add_from_file(self.__class__.arquivoglade)
		#conectando os sinais
		builder.connect_signals(self)
		#carregando janela
		self.janela = builder.get_object("janela")
		self.campo = builder.get_object("campo")
		self.fcb = builder.get_object("fcb")
		self.janela.show_all()
		
		self.player = gst.Pipeline()
		vsrc = gst.element_factory_make("ximagesrc","vsrc")
		caps = gst.Caps("video/x-raw-rgb,framerate=(fraction)5/1")
		capsfilter = gst.element_factory_make("capsfilter","filter")
		capsfilter.set_property("caps", caps)
		cspace = gst.element_factory_make("ffmpegcolorspace","colorspace")
		encoder = gst.element_factory_make("ffenc_flv","encoder")
		vqueue = gst.element_factory_make("queue","vqueue")
		asrc = gst.element_factory_make("osssrc","asrc")
		acaps = gst.Caps("audio/x-raw-int ,width=16,depth=16,rate=44100,channels=2,signed=true")
		acapsfilter = gst.element_factory_make("capsfilter","afilter")
		acapsfilter.set_property("caps", acaps)
		aconvert = gst.element_factory_make("audioconvert","aconvert")
		aqueue = gst.element_factory_make("queue","aqueue")
		mux = gst.element_factory_make("flvmux","mux")
		self.sink = gst.element_factory_make("filesink","sink")
		
		self.player.add(vsrc,capsfilter,cspace,encoder,vqueue,asrc,acapsfilter,aconvert,aqueue,mux,self.sink)
		
		gst.element_link_many(vsrc,capsfilter,cspace,encoder,vqueue,mux)
		gst.element_link_many(asrc,acapsfilter,aconvert,aqueue,mux)
		gst.element_link_many(mux,self.sink)
		
		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect("message", self.on_message)
		bus.connect("sync-message::element", self.on_sync_message)
		
		
		
		gtk.gdk.threads_init()
		gtk.main()
		
	def on_message(self, bus, message):
		t = message.type
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

