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
    gobject.threads_init()
except:
    sys.exit(1)

import pygst 
pygst.require('0.10')

import gst

class Convertv(object):

	def on_stop_clicked(self,widget, data=None):
		self.player.set_state(gst.STATE_NULL)
		
	def on_sair_clicked(self, widget, data=None):
		pass
		
	def on_converte_clicked(self,widget, data=None):
		if self.player.get_state()[1] == gst.STATE_NULL:
			filepath = self.fcb.get_filename()
			filepath2 = self.fcb2.get_filename()
			name = filepath.split("/")[-1]
			name2 = name.split(".")[0]+".ogg"
			print filepath
			print filepath2
			print name
			print name2
			if os.path.isfile(filepath):
				self.source.set_property("location", filepath)
				self.sink.set_property("location", filepath2 + "/" + name2)
				self.player.set_state(gst.STATE_PLAYING)
			

	arquivoglade = "convertV.glade"
	
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
		
		self.player = gst.Pipeline()
		self.source = gst.element_factory_make("filesrc","source")
		mad = gst.element_factory_make("mad","mad")
		convert = gst.element_factory_make("audioconvert","converter")
		encoder = gst.element_factory_make("vorbisenc","encoder")
		muxer = gst.element_factory_make("oggmux","oggmux")
		self.sink = gst.element_factory_make("filesink","filesink")
		
		self.player.add(self.source,mad,convert,encoder,muxer,self.sink)
		
		gst.element_link_many(self.source,mad,convert,encoder,muxer,self.sink)
		
		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect("message", self.on_message)
		
		gtk.gdk.threads_init()
		gtk.main()
		
	def on_message(self, bus, message):
		t = message.type
		print t
		if t == gst.MESSAGE_EOS:
			self.player.set_state(gst.STATE_NULL)
			
		elif t == gst.MESSAGE_ERROR:
			err, debug = message.parse_error()
			print "Error: %s" % err, debug
			self.player.set_state(gst.STATE_NULL)

if __name__ == "__main__":
	
	cv = Convertv()
	#gtk.gdk.threads_init()	
