#!/usr/bin/python3

# Copyright (C) 2015 Leonidas S. Barbosa <kirotawa@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.
#

import os
import argparse
from datetime import date

try:
    import sqlite3
except:
    print ("Need to install python-sqlite3")

__version__ = '0.0.1'

CONN_PATH = os.path.join(os.environ.get('HOME'), '.tdl.db')
TODAY = date.today()

COMMANDS = {
    'add': """INSERT INTO todo VALUES (NULL, '%s', '%s', '%s', '%s', '%s');""",
    'delete': """DELETE FROM todo WHERE id=%d;""",
    'list': """SELECT * FROM todo WHERE %s;""",
    'getd': """SELECT description FROM todo WHERE id=%d;""",
    'update': """UPDATE todo SET %s WHERE id=%d;""",
}

common = '\033['
blink = ';5m'
COLOR = {
    'red': common + '031m',
    'green': common + '032m',
    'yellow': common + '033m',
    'white': common + '037m',
    'black': common + '030m',
    'blue': common + '034m',
    'yblink': common + '033' + blink,
    'end':  '\033[0m',
}


def get_args():
    parser = argparse.ArgumentParser(description="'td' is acronym for TODO a \
                                     simple way to track todo things/list")
    parser.add_argument("-a", "--add",  help="adds a todo into list",
                        action="store_true")
    parser.add_argument("-d", "--desc", help="sets a description",
                        action="store", dest="desc")
    parser.add_argument("-S", "--status", type=str, choices=['created',
                                                             'started',
                                                             'finished',
                                                             'paused',
                                                             'canceled'
                                                             ],
                        help="sets todo status", action="store",
                        dest="status", default="created")
    parser.add_argument("-s", "--start", help="sets a start date",
                        action="store", dest="start",
                        default=date.strftime(TODAY, "%d/%m/%Y"))
    parser.add_argument("-e", "--end", help="sets a end date=d/m/y format",
                        action="store", dest="end", default="01/12/2042")
    parser.add_argument("-D", "--delete", help="delete a give todo by id",
                        action="store_true")
    parser.add_argument("-i", "--id", help="pass a id to other options",
                        type=int, action="store", dest="id")
    parser.add_argument("-p", "--priority", help="sets a priority", type=str,
                        action="store", dest="priority", default="normal",
                        choices=['normal', 'medium', 'high'])
    parser.add_argument("--debug", help="provides debug info",
                        action="store_true")
    parser.add_argument("-v", "--version", help="provies current version",
                        action="store_true")
    parser.add_argument("--getd", help="get full description of todo by id",
                        action="store_true")
    parser.add_argument("--up-status", help="update status given a id",
                        action="store_true")
    parser.add_argument("--up-end", help="update end date given a id",
                        action="store_true")
    parser.add_argument("--up-priority", help="update priority given a id",
                        action="store_true")
    parser.add_argument("--up-description", help="update description given a \
                        id", action="store_true")

    lists = parser.add_mutually_exclusive_group()
    lists.add_argument("--list", help="list everything todo by id",
                       action="store_true")
    lists.add_argument("-ls", "--lstart", help="list by start date",
                       action="store_true")
    lists.add_argument("-le", "--lend", help="list by end date",
                       action="store_true")
    lists.add_argument("-lp", "--lprio", help="list by priority",
                       action="store_true")
    lists.add_argument("-lS", "--lstatus", help="list by status",
                       action="store_true")

    return parser.parse_args()


def get_conn():
    try:
        return sqlite3.connect(CONN_PATH)
    except sqlite3.Connection.Error:
        print("Error on connection")


def execute(conn, command):
    cursor = conn.cursor()
    cursor.execute(command)
    conn.commit()

    if command[:6] == "SELECT":
        return cursor.fetchall()


def print_format(data):
    #  ID  |          DESC          |  START   |   END    | STATUS | PRIORT | #
    #     1|blalallalalala lalal ...|12/04/2014|12/08/2010|finished|  normal|
    #     2|lalalalleleljekrjlee ...|12/04/1022|1232323232| started|  medium|
    #    10|laklskjsjsksjsjsllsl ...|12/04/2014|13/08/1900| created|    high|
    if data:
        print("   ID  |          DESC          |  START   |   END    | STATUS | PRIORT ")
        print("------------------------------------------------------------------------")
    else:
        print("0 registers found")

    for d in data:
        id = str(d[0])
        start = d[2]
        desc = d[1]
        status = d[4]
        priority = d[5]

        # adjusting len of caracters allowed
        desc = desc[:21].ljust(21)
        id = id.rjust(6)

        # print what matters with colors
        if priority == 'high':
            priority = COLOR['red']+priority.rjust(8)+COLOR['end']
        if priority == 'normal':
            priority = COLOR['green']+priority.rjust(8)+COLOR['end']
        if priority == 'medium':
            priority = COLOR['yellow']+priority.rjust(8)+COLOR['end']

        if status == 'started':
            status = COLOR['blue']+status.rjust(8)+COLOR['end']
        if status == 'finished':
            status = COLOR['green']+status.rjust(8)+COLOR['end']
        if status == 'paused':
            status = COLOR['yblink']+status.rjust(8)+COLOR['end']
        if status == 'canceled':
            status = status.rjust(8)
        if status == 'created':
            status = status.rjust(8)
            start = ''
            start = start.rjust(10)

        # print in table format
        print(" %s|%s...|%s|%s|%s|%s"
              % (id, desc, start, d[3], status, priority))

if __name__ == "__main__":
    conn = get_conn()
    args = get_args()

    if args.debug:
        print("ARGS: %s" % args)

    if args.version:
        print("current: %s" % __version__)

    if args.add and args.desc:
        execute(conn, COMMANDS['add'] % (args.desc, args.start, args.end,
                                         args.status, args.priority))
    elif args.add:
        print("You need to provide a description\n")

    if args.delete and args.id:
        execute(conn, COMMANDS['delete'] % args.id)
    elif args.delete:
        print("An id is necessary for this action\n")

    if args.getd:
        if args.id:
            res = execute(conn, COMMANDS['getd'] % args.id)
            print("Description: ", res[0][0])

    if args.up_status:
        if args.id and args.status:
            execute(conn, COMMANDS['update'] % ("status='%s'" % args.status,
                                                args.id))

    if args.up_end:
        if args.id and args.end:
            execute(conn, COMMANDS['update'] % ("end='%s'" % args.end,
                                                args.id))

    if args.up_priority:
        if args.id and args.priority:
            execute(conn, COMMANDS['update'] % ("priority='%s'" %
                                                args.priority, args.id))
    if args.up_description:
        if args.id and args.desc:
            execute(conn, COMMANDS['update'] % ("description='%s'" %
                                                args.desc, args.id))

    if args.list:
        clausule = "id"
        if args.id:
            clausule = "id=%s" % args.id

        res = execute(conn, COMMANDS['list'] % clausule)
        print_format(res)
    if args.lstart and args.start:
        clausule = "start='%s'" % args.start
        res = execute(conn, COMMANDS['list'] % clausule)
        print_format(res)
    if args.lend and args.end:
        clausule = "end='%s'" % args.end
        res = execute(conn, COMMANDS['list'] % clausule)
        print_format(res)
    if args.lprio and args.priority:
        clausule = "priority='%s'" % args.priority
        res = execute(conn, COMMANDS['list'] % clausule)
        print_format(res)
    if args.lstatus and args.lstatus:
        clausule = "status='%s'" % args.status
        res = execute(conn, COMMANDS['list'] % clausule)
        print_format(res)
    elif None:
        print("provide a valid option")
