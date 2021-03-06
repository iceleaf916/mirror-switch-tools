#!/usr/bin/python2
# -*- coding: utf-8 -*-

# Copyright (C) 2011~2015 Deepin, Inc.
#               2011~2015 Kaisheng Ye
#
# Author:     Kaisheng Ye <kaisheng.ye@gmail.com>
# Maintainer: Kaisheng Ye <kaisheng.ye@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import ConfigParser
import gettext
import gtk
import os
import sys
import traceback

VERSION_FILE = "/etc/deepin-version"

source_list_template = '''\
# generated by `test mirror switching tool` for deepin
deb http://<host>/ubuntu trusty main restricted universe multiverse
deb http://<host>/ubuntu trusty-security main restricted universe multiverse
deb http://<host>/ubuntu trusty-updates main restricted universe multiverse
deb-src http://<host>/ubuntu trusty main restricted universe multiverse
deb-src http://<host>/ubuntu trusty-security main restricted universe multiverse
deb-src http://<host>/ubuntu trusty-updates main restricted universe multiverse

deb http://<host>/deepin trusty main universe non-free
deb-src http://<host>/deepin trusty main universe non-free
'''

test_mirror_host = "%s:%s@test.packages.linuxdeepin.com"
official_mirror_host = "packages.linuxdeepin.com"

class I18N(object):

    PROGRAM_NAME = "mirror-switching-tool"

    def __init__(self):
        self.locale_dir = os.path.join(self.get_parent_dir(__file__, 2), "locale", "mo")

        if not os.path.exists(self.locale_dir):
            self.locale_dir = "/usr/share/locale"

    def get_parent_dir(self, filepath, level=1):
        '''Get parent dir.'''

        parent_dir = os.path.realpath(filepath)

        while(level > 0):
            parent_dir = os.path.dirname(parent_dir)
            level -= 1

        return parent_dir


    def get_gettext(self):
        _ = None
        try:
            _ = gettext.translation(self.PROGRAM_NAME, self.locale_dir).gettext
        except Exception:
            _ = lambda i : i

        return _


class MainWindow(gtk.Window):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.set_title(_("deepin Test Mirror Switching Tool"))
        #self.set_size_request(404, 160)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_resizable(False)
        self.set_icon_name("deepin-logo")

        main_vbox = gtk.VBox(False, 5)

        title_label = gtk.Label(_("Select the mirror:"))
        title_label_align = gtk.Alignment(0, 0, 0, 0)
        title_label_align.add(title_label)

        group_radio = gtk.RadioButton()
        self.test_mirror_radio = gtk.RadioButton(group_radio, _("Internal test mirror"))
        self.test_mirror_radio.set_active(True)

        username_label = gtk.Label(_("Username:"))
        self.username_entry = gtk.Entry()
        self.username_entry.set_width_chars(14)
        password_label = gtk.Label(_("Password:"))
        self.password_entry = gtk.Entry()
        self.password_entry.set_width_chars(14)
        test_mirror_extra_hbox = gtk.HBox(False, 4)
        test_mirror_extra_hbox.pack_start(username_label, False, False)
        test_mirror_extra_hbox.pack_start(self.username_entry, False, False)
        test_mirror_extra_hbox.pack_start(password_label, False, False)
        test_mirror_extra_hbox.pack_start(self.password_entry, False, False)
        test_mirror_extra_hbox_align = gtk.Alignment(0, 0, 0, 0)
        test_mirror_extra_hbox_align.set_padding(0, 0, 24, 0)
        test_mirror_extra_hbox_align.add(test_mirror_extra_hbox)

        self.official_mirror_radio = gtk.RadioButton(group_radio, _("Official stable mirror"))

        radio_vbox = gtk.VBox()
        radio_vbox.pack_start(self.test_mirror_radio)
        radio_vbox.pack_start(test_mirror_extra_hbox_align)
        radio_vbox.pack_start(self.official_mirror_radio)
        radio_vbox_align = gtk.Alignment(0, 0, 0, 0)
        radio_vbox_align.add(radio_vbox)

        # action button
        button_hbox = gtk.HBox(False, 3)
        switch_button = gtk.Button(_("Switch"))
        switch_button.set_size_request(70, -1)
        switch_button.connect("clicked", self.switch_button_handler)
        close = gtk.Button(_("Exit"))
        close.set_size_request(70, -1)
        close.connect("clicked", self.quit)
        self.tip_message = gtk.Label()
        tip_message_align = gtk.Alignment(0, 0, 0, 0)
        tip_message_align.set_padding(0, 0, 20, 0)
        tip_message_align.add(self.tip_message)
        button_hbox.pack_start(tip_message_align, False, False)
        button_hbox.pack_end(close, False, False)
        button_hbox.pack_end(switch_button, False, False)
        button_halign = gtk.Alignment(0, 0, 1, 0)
        button_halign.add(button_hbox)

        main_vbox.pack_start(title_label_align, False, False)
        main_vbox.pack_start(radio_vbox_align, False, False)
        main_vbox.pack_start(button_halign, False, False, 3)

        main_vbox_align = gtk.Alignment(0.5, 0.5, 1, 1)
        main_vbox_align.set_padding(20, 20, 20, 20)
        if self.isDeepin2014():
            main_vbox_align.add(main_vbox)
        else:
            error_label = gtk.Label()
            error_label.set_line_wrap(True)
            error_label.set_markup('<span foreground="red">%s</span>' % (_("Note: Detecting that your system is not deepin 2014. The tool can only run in deepin 2014.")))
            main_vbox_align.add(error_label)
        self.add(main_vbox_align)

        self.connect("destroy", self.quit)
        self.show_all()

    def isDeepin2014(self):
        if os.path.exists(VERSION_FILE):
            config = ConfigParser.RawConfigParser()
            config.read(VERSION_FILE)
            ver = config.get("Release", "Version")
            return ver.startswith("2014")
        else:
            return False

    def show_tip(self, message, time=2000):
        self.tip_message.set_markup(message)
        gtk.timeout_add(time, lambda: self.tip_message.set_markup(""))

    def switch_button_handler(self, widget=None, data=None):
        if self.test_mirror_radio.get_active():
            username = self.username_entry.get_text()
            password = self.password_entry.get_text()
            if username == "":
                self.show_tip("<span foreground='red'>%s</span>" % (_("Username can not be empty")))
            elif password == "":
                self.show_tip("<span foreground='red'>%s</span>" % (_("Password can not be empty")))
            else:
                res = self.show_mirror_change_confirm(_("Internal test mirror"))
                if res == gtk.RESPONSE_OK:
                    host = test_mirror_host % (username, password)
                    if self.change_source_list(host):
                        self.show_tip("<span foreground='blue'>%s</span>" % (_("Switch successfully!")))
                    else:
                        self.show_tip("<span foreground='red'>%s</span>" % (_("Failed to switch!")))
        else:
            res = self.show_mirror_change_confirm(_("Official stable mirror"))
            if res == gtk.RESPONSE_OK:
                if self.change_source_list(official_mirror_host):
                    self.show_tip("<span foreground='blue'>%s</span>" %(_("Switch successfully!")))
                else:
                    self.show_tip("<span foreground='red'>%s</span>" % (_("Failed to switch!")))

    def show_mirror_change_confirm(self, mirror_name):
        dialog = gtk.MessageDialog(self, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK_CANCEL)
        dialog.format_secondary_markup('/etc/apt/sources.list %s<span foreground="blue">“%s”</span>?' % (_("file will be overwitten. Are you sure to switch the current system mirror to"), mirror_name))
        dialog.set_markup(_("Note:"))
        res = dialog.run()
        dialog.destroy()
        return res

    def quit(self, widget=None, data=None):
        gtk.main_quit()

    def change_source_list(self, host):
        contents = source_list_template.replace("<host>", host)
        print "========== Debug ============"
        print contents
        print "========== Debug ============"
        try:
            fp = open("/etc/apt/sources.list", "w")
            fp.write(contents)
            fp.close()
            print _("Switch successfully!")
            return True
        except Exception, e:
            print _("Error:") + str(e)
            traceback.print_exc(file=sys.stdout)
            return False

_ = I18N().get_gettext()

if __name__ == "__main__":
    MainWindow()
    gtk.main()
