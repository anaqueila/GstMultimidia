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


class Reproduz(object):


	def on_open_activate(self, widget, data=None):
		chooser = gtk.FileChooserDialog("Select file", self.janela, gtk.FILE_CHOOSER_ACTION_OPEN,\
						(   gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
						    gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		filter = gtk.FileFilter()
		filter.set_name("Video/Audio")
		filter.add_mime_type("video/xvid")
		filter.add_mime_type("video/divx")
		filter.add_mime_type("video/mpeg")
		filter.add_mime_type("video/rmvb")
		filter.add_mime_type("video/flv")
		filter.add_pattern("*.rmvb")
		filter.add_pattern("*.flv")
		filter.add_pattern("*.avi")
		filter.add_pattern("*.divx")
		filter.add_pattern("*.mpg")
		filter.add_pattern("*.wmv")
		filter.add_pattern("*.mpeg")
		filter.add_pattern("*.mkv")
		filter.add_pattern("*.ogg")
		filter.add_pattern("*.mp4")
		filter.add_pattern("*.wma")
		filter.add_pattern("*.mp3")
		filter.add_pattern("*.flac")
		filter.add_pattern("*.wav")
		filter.add_pattern("*.aac")
		filter.add_pattern("*.aiff")
		chooser.add_filter(filter)

		response = chooser.run()
        	if response == gtk.RESPONSE_OK:
            		self.currentFile= chooser.get_filename()
            		self.on_play()
        	chooser.destroy()

	def on_play_clicked(self, widget, data=None):

		if self.player.get_state()[1] == gst.STATE_NULL:
			filepath = self.currentFile
			if os.path.isfile(filepath):
				self.player.set_property("uri", "file://" + filepath)
				self.player.set_state(gst.STATE_PLAYING)
		elif self.player.get_state()[1] == gst.STATE_PAUSED:
			self.player.set_state(gst.STATE_PLAYING)

	def on_pause_clicked(self, widget, data=None):

		if self.player.get_state()[1] == gst.STATE_PLAYING:
			self.player.set_state(gst.STATE_PAUSED)

	def on_stop_clicked(self, widget, data=None):

		if self.player.get_state()[1] == gst.STATE_PLAYING:
			self.player.set_state(gst.STATE_NULL)
		elif self.player.get_state()[1] == gst.STATE_PAUSED:
			self.player.set_state(gst.STATE_NULL)

	def on_volume_value_changed(self, widget, vol):
		self.player.set_property("volume", float(vol))
		

	def on_quit_activate(self, widget, data=None):
		self.janela.hide()
		gtk.main_quit()

	def on_janela_destroy(self, widget, data=None):
		self.player.set_state(gst.STATE_NULL)

	arquivoglade = "Reproduz.glade"

	def __init__ (self):

		self.imagesink = None

		#Instancia a classe Builder
		builder = gtk.Builder()
		#Carregando o Arquivo glade
		builder.add_from_file(self.__class__.arquivoglade)
		#carregando janela
		self.janela = builder.get_object("janela")
		self.movie_window = builder.get_object("movie_window")
		self.volume = builder.get_object("volume")

		#conectando os sinais
		builder.connect_signals(self)
		self.janela.show_all()

		self.movie_window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(red=0, green=0, blue=0, pixel=65535))


		self.player = gst.element_factory_make("playbin", "src")
		sink = gst.element_factory_make("xvimagesink", "video-output")
		asink = gst.element_factory_make("osssink", "audio-output")
		self.player.set_property("video-sink", sink)
		self.player.set_property("audio-sink", asink)
		self.player.props.vis_plugin = gst.element_factory_make ("goom2k1")

		bus = self.player.get_bus()

		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect("message", self.on_message)
		bus.connect("sync-message::element", self.on_sync_message)

		gtk.gdk.threads_init()

		gtk.main()



	def on_play(self):

		if self.player.get_state()[1] == gst.STATE_NULL:
			filepath = self.currentFile
			if os.path.isfile(filepath):
				self.player.set_property("uri", "file://" + filepath)
				self.player.set_state(gst.STATE_PLAYING)
		elif self.player.get_state()[1] == gst.STATE_PAUSED:
			self.player.set_state(gst.STATE_PLAYING)


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
			return False
		message_name = message.structure.get_name()
		if message_name == "prepare-xwindow-id":
			imagesink = message.src
			imagesink.set_property("force-aspect-ratio", True)
			gtk.gdk.threads_enter()
			imagesink.set_xwindow_id(self.movie_window.window.xid)
			gtk.gdk.threads_leave()

