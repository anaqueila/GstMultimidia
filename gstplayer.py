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


from testechamada import *

import pygst 
pygst.require('0.10')

import gst

############# Classe Principal ####################


class Player(object):
	
	def __init__(self):
		#O Arquivo Glade
		self.arquivoglade = "gstplayer.glade"
		
		#Carrega a interface a partir do arquivo glade / A representação xml do arquivo
    		self.xml = gtk.glade.XML(self.arquivoglade)

	        # Nossos componentes
		
        	# Janela
    		self.window = self.xml.get_widget('window1')
		self.window.set_title("GstPlayer")
		self.draw = self.xml.get_widget('drawingarea2')
		#Botoes
    		self.play = self.xml.get_widget('play')
    		self.pause = self.xml.get_widget('pause')
		self.stop = self.xml.get_widget('stop')
		self.capturamic = self.xml.get_widget('capmic')
		self.volumebutton1 = self.xml.get_widget('volumebutton')
		self.timeFormat = gst.Format(gst.FORMAT_TIME)

		self.currentFile = None
		set_xid = None
		self.metadata = {} #Tags

		#Player
		self.pipeline = gst.Pipeline("mypipe")
		self.player = gst.element_factory_make("playbin", "src")
		self.pipeline.add(self.player)

		vsink = gst.element_factory_make("xvimagesink", "vsink")
        	self.vsink = vsink
        	self.player.set_property("video-sink", vsink)
        	vsink.set_property("force-aspect-ratio", True)

		self.volume = gst.element_factory_make("volume")
		#self.volume.set_property('volume',10)
		
		#Converter pipeline
		self.player01 = gst.Pipeline("MyPlayer")
		source = gst.element_factory_make("osssrc", "source")
		convert = gst.element_factory_make("audioconvert",'audioconvert')
		enc = gst.element_factory_make("vorbisenc","encoder")	
		mux = gst.element_factory_make("oggmux", "mux")	
		sink = gst.element_factory_make("filesink","sink")
		sink.set_property("location","mic-%05d.ogg")
		
		self.player01.add(source,convert,enc,mux,sink)
		gst.element_link_many(source,convert,enc,mux,sink)

		#Eventos

		#Fecha o Loop da Janela
		self.window.connect('destroy', gtk.main_quit)	
	

    		#Conecta Sinais aos Callbacks
		self.connect_signals()

		bus = self.player.get_bus()
		bus = self.player01.get_bus()
		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect("message", self.bus_handler)
		bus.connect("message", self.on_message)
        bus.connect("message::tag", self.on_tag_message)
		bus.connect("sync-message::element", self.on_sync_message)
		def bus_handler(bus, message):
	            	if message.type == gst.MESSAGE_ELEMENT:
	                	if message.structure.get_name() == 'prepare-xwindow-id':
	                	    set_xid(w)
	            	return gst.BUS_PASS
		bus.set_sync_handler(bus_handler)

    		#Exibe toda interface
    		self.window.show_all()
    			



	def connect_signals(self):
        	"""
        	    autoconnect signals
        	"""
        	self.xml.signal_autoconnect(
        	    {
        	    'on_play_clicked': lambda *e:  self.play_pause(),
		    'on_pause_clicked': lambda *e: self.Pause(),
        	    'on_stop_clicked': lambda *e: self.Stop(),
		    'on_volume_value_changed': self.on_vol_changed,
        	    'on_quit_button_activate': lambda *e: self.quit(),
        	    'on_open_file_activate' : lambda *e: self.open(),
		    'on_capmic_clicked': lambda *e: self.captura(),
		    'on_menuitem5_activate':lambda *e: self.on_menuitem5_activate()
        	    })

	gtk.gdk.notify_startup_complete()

#	def start_stop(self, w):
#		if self.button.get_label() == "Start":
#			filepath = self.file.get_filename()
#			if os.path.isfile(filepath):
#				self.player.set_property("uri", "file://" + filepath)
#				self.player.set_state(gst.STATE_PLAYING)

	def on_menuitem5_activate(self,*e):
		Novo = Teste()
		#Novo()
		print "Passou"

	def on_vol_changed(self,w,v):
	        self.set_vol(w.get_value())
		self.set_vol(v)

	def set_vol(self,vol = None):
		if not vol:
			vol = self.xml.get_widget("volume").get_value()
	        self.player.set_property("volume",vol)

    	def play_pause(self,*e):
        	"""
        	    Handle the play_pause button clickes
        	"""
        	if self.player.get_state()[1] == gst.STATE_NULL:
        	    filepath = self.currentFile
        	    if os.path.isfile(filepath):
        	        self.player.set_property("uri", "file://" + filepath)
        	        self.player.set_state(gst.STATE_PLAYING)

		elif self.player.get_state()[1] == gst.STATE_PAUSED:
            		self.player.set_state(gst.STATE_PLAYING)

	def Pause(self, *e):
		
		if self.player.get_state()[1] == gst.STATE_PLAYING:
			self.player.set_state(gst.STATE_PAUSED)

	def Stop(self, *e):

		if self.player.get_state()[1] == gst.STATE_PLAYING:
			self.player.set_state(gst.STATE_NULL)

	def captura(self, *e):
		if self.capturamic.get_label() == "Start":
			self.capturamic.set_label("Stop")
			self.player01.set_state(gst.STATE_PLAYING)
		else:
			self.player01.set_state(gst.STATE_NULL)
			self.capturamic.set_label("Start")

###	messages of gstreamer  ####					

	def on_tag_message(self, bus, message):
	        tags = message.parse_tag()
	        for x in tags.keys():
	            print x,"=",tags[x]
	            if x != "private-id3v2-frame":
	                self.metadata[x] = tags[x]

	def on_message(self, bus, message):
		t = message.type
		if t == gst.MESSAGE_EOS:
			self.player.set_state(gst.STATE_NULL)
			self.player01.set_state(gst.STATE_NULL)
			self.player01.set_label("Start")
		elif t == gst.MESSAGE_ERROR:
			self.player.set_state(gst.STATE_NULL)
			self.player01.set_state(gst.STATE_NULL)
			err, debug = message.parse_error()
			erro, debug = message.gdk_x_error()
			print "Error: %s" % err, debug
			print "Error: %s" % erro, debug
			self.player.set_label("Start")
	
	def on_sync_message(self, bus, message):
		if message.structure is None:
			return
		message_name = message.structure.get_name()
		if message_name == "prepare-xwindow-id":
			imagesink = message.src
			imagesink.set_property("force-aspect-ratio", True)
			imagesink.set_xwindow_id(self.draw.window.xid)
####

	def open(self):
        	chooser = gtk.FileChooserDialog("Select file", self.window, gtk.FILE_CHOOSER_ACTION_OPEN,\
						(   gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
						    gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        	filter = gtk.FileFilter()
        	filter.set_name("Video/Audio")
        	filter.add_mime_type("video/xvid")
        	filter.add_mime_type("video/divx")
        	filter.add_mime_type("video/mpeg")
		filter.add_pattern("video/rmvb")
		filter.add_pattern("video/flv")
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
            		#self.open()
            		self.play_pause()
        	chooser.destroy()

    	def quit(self):
		print "quit"
        	gtk.main_quit()

	  


if __name__ == "__main__":
	Player()
	gtk.gdk.threads_init()
	#Inicia o loop principal de eventos (GTK MainLoop)
	gtk.main()
