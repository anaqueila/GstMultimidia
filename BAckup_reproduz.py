# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys, os, thread, time
try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk
    import gtk.glade
    import gobject
except:
    sys.exit(1)

import pygst 
pygst.require('0.10')

import gst



class Reproduz(object):


	def on_janela_destroy(self, widget, data=None):
		sys.exit(1)

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

	def on_volume_value_changed(self, widget, vol=10):

		self.player.set_property("volume", float(vol)) 

	def on_movie_window_expose_event(self, widget, event):

		if self.imagesink:
			self.imagesink.expose()
			return False
		
		else:

			return True

	def on_hscale1_change_value(adjustment=None):
		print adjustment


	def on_quit_activate(self, widget, data=None):
		sys.exit(1)

	arquivoglade = "Reproduz.glade"
	
	def __init__ (self, videowidget):

		self.imagesink = None

		builder = gtk.Builder()
		builder.add_from_file(self.__class__.arquivoglade)
		#carregando janela
		self.janela = builder.get_object("janela")
		self.movie_window = builder.get_object("movie_window")
		self.volume = builder.get_object("volume")
		
		#conectando os sinais
		builder.connect_signals(self)
		self.janela.show_all()
		self.janela.connect('destroy', gtk.main_quit)
		self.movie_window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(red=0, green=0, blue=0, pixel=65535))
		self.videowidget = videowidget

		#self.player = gst.pipeline("player")
		self.player = gst.element_factory_make("playbin", "src")
		#source = gst.element_factory_make("filesrc","file-source")
		fakesink = gst.element_factory_make("xvimagesink", "video-output")
		self.player.set_property("video-sink", fakesink)
		self.timeFormat = gst.Format(gst.FORMAT_TIME)

		bus = self.player.get_bus()
		print bus
		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect("message", self.on_message)
		bus.connect("sync-message::element", self.on_sync_message)

	gtk.gdk.notify_startup_complete()
	
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
			return 
		message_name = message.structure.get_name()
		if message_name == "prepare-xwindow-id":
			self.videowidget.set_sink(message.src)
            message.src.set_property('force-aspect-ratio', True)

class VideoWidget:
    ## Constructor.
    # \param TArea - GTK+ drowing area widget.
    def __init__(self, TArea):
        self.movie_window=TArea
        self.imagesink = None
        self.Area.unset_flags(gtk.DOUBLE_BUFFERED)

    ## \var Area
    # GTK+ drowing area widget.

    ## \var imagesink
    # Sink element for 

    def do_expose_event(self, event):
        if self.imagesink:
            self.imagesink.expose()
            return False
        else:
            return True

    def set_sink(self, sink):
        assert self.Area.window.xid
        self.imagesink = sink
        self.imagesink.set_xwindow_id(self.movie_window.window.xid)

#if __name__ == "__main__":
	
#	Reproduz()
#	gtk.gdk.threads_init()
#	gtk.main()	
