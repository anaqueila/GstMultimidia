#!/usr/bin/python 

# Copyright (C) 2009 Mauricio Teixeira. 
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see «http://www.gnu.org/licenses/».

# 
# Author: Mauricio Teixeira «mauricio.teixeira at gmail dot com» 
# 
# This code is the example of the following blog post: 
# https://mteixeira.wordpress.com/2009/04/18/gnome-notification-area-application-in-python-english/


import pygtk 
pygtk.require('2.0') 
import gtk 

class HelloTray: 

  def __init__(self): 
    self.statusIcon = gtk.StatusIcon() 
    self.statusIcon.set_from_stock(gtk.STOCK_ABOUT) 
    self.statusIcon.set_visible(True) 
    self.statusIcon.set_tooltip("Hello World") 

    self.menu = gtk.Menu() 
    self.menuItem = gtk.ImageMenuItem(gtk.STOCK_EXECUTE) 
    self.menuItem.connect('activate', self.execute_cb, self.statusIcon) 
    self.menu.append(self.menuItem) 
    self.menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT) 
    self.menuItem.connect('activate', self.quit_cb, self.statusIcon) 
    self.menu.append(self.menuItem) 

    self.statusIcon.connect('popup-menu', self.popup_menu_cb, self.menu) 
    self.statusIcon.set_visible(1) 

    gtk.main() 

  def execute_cb(self, widget, event, data = None): 
    window = gtk.Window(gtk.WINDOW_TOPLEVEL) 
    window.set_border_width(10) 

    button = gtk.Button("Hello World") 
    button.connect_object("clicked", gtk.Widget.destroy, window) 

    window.add(button) 
    button.show() 
    window.show() 

  def quit_cb(self, widget, data = None): 
    gtk.main_quit() 

  def popup_menu_cb(self, widget, button, time, data = None): 
    if button == 3: 
      if data: 
        data.show_all() 
        data.popup(None, None, gtk.status_icon_position_menu, 
                   3, time, self.statusIcon) 

if __name__ == "__main__": 
  helloWord = HelloTray()