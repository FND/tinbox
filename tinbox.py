#!/usr/bin/env python

"""
cf.
https://mteixeira.wordpress.com/2009/04/18/gnome-notification-area-application-in-python-english/

CAVEATS:
* tray to disappear in GNOME 3 and Ubuntu Unity
* icon overlays should ideally be auto-generated
"""

import sys
import shlex

import pygtk
pygtk.require('2.0') # XXX: accurate?
import gtk
import gobject

from optparse import OptionParser
from subprocess import Popen, PIPE


def main(args):
    args = [unicode(arg, 'utf-8') for arg in args]

    parser = OptionParser()
    parser.add_option('-s', '--script', help='path to todo.sh')
    (opts, args) = parser.parse_args()

    todosh = opts.script or _run('which todo.sh')[0]
    command = '/usr/bin/env TODOTXT_VERBOSE=0 %s -p listpri a' % todosh

    ToDoTray(command)
    gtk.main()

    return True


class ToDoTray():
    interval = 5

    def __init__(self, command):
        self.command = command # XXX: rename?

        tasks = self.get_tasks()
        if len(tasks) > 9:
            icon = gtk.STOCK_JUSTIFY_FILL
        else:
            icon = gtk.STOCK_EDIT

        self.statusIcon = gtk.StatusIcon()
        self.statusIcon.set_from_stock(icon)
        self.statusIcon.set_visible(True)
        self.statusIcon.set_tooltip('Hello World')

        self.menu = gtk.Menu()
        for task in tasks:
            menuItem = gtk.MenuItem(task)
            self.menu.append(menuItem)
        self.menu.append(gtk.SeparatorMenuItem())
        menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        menuItem.connect('activate', self.on_quit, self.statusIcon)
        self.menu.append(menuItem)

        self.statusIcon.connect('popup-menu', self.on_info, self.menu)

        gobject.timeout_add_seconds(self.interval, self.update_icon)

    def on_quit(self, widget, data=None):
        gtk.main_quit()

    def on_info(self, widget, button, time, data=None):
        if button == 3:
            if data:
                data.show_all()
                data.popup(None, None, gtk.status_icon_position_menu,
                        3, time, self.statusIcon)

    def update_icon(self):
        self.statusIcon.set_from_stock(gtk.STOCK_JUSTIFY_FILL)
        return True

    def get_tasks(self):
        return _run(self.command)


def _run(cmd): # XXX: rename
    """
    executes shell command and returns output as list of lines

    cmd argument can be either a string or a list (the latter is useful if
    arguments contain spaces)
    """
    if isinstance(cmd, basestring):
        cmd = shlex.split(cmd)
    return Popen(cmd, stdout=PIPE).communicate()[0].splitlines()


if __name__ == '__main__':
    status = not main(sys.argv)
    sys.exit(status)
