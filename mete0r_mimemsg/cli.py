# -*- coding: utf-8 -*-
#
#   mete0r.mimemsg : SOME_DESCRIPTION
#   Copyright (C) 2015 mete0r <mete0r@sarangbang.or.kr>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import logging
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.generator import Generator
from email.parser import Parser

from docopt import docopt


logger = logging.getLogger('mimemsg')


def main():
    doc = ('''mimemsg

Usage:
    mimemsg text [--subject=<subject>] [--subtype=<textsubtype>] [--charset=<charset>]
    mimemsg multipart init [--subject=<subject>] [--charset=<charset>] <filename>
    mimemsg multipart add [--attachment=<part-filename>] <filename> <part>
    mimemsg (-h | --help)
    mimemsg --version

Options:
    --charset=<charset>   Specify default charset for headers/payload. (default: 'utf-8')
    --subtype=<subtype>   Specify default MIME subtype. (default: 'plain')
''')
    logging.basicConfig(level=logging.WARNING)

    args = docopt(doc)
    logger.info('args: %s', args)

    if args['text']:
        return cmd_text(args)

    if args['multipart'] and args['init']:
        return cmd_multipart_init(args)

    if args['multipart'] and args['add']:
        return cmd_multipart_add(args)


def cmd_text(args):
    charset = args['--charset'] or 'utf-8'
    subtype = args['--subtype'] or 'plain'

    msg = MIMEText(sys.stdin.read(), subtype, charset)
    if args['--subject']:
        msg['Subject'] = Header(args['--subject'], charset)
    else:
        logger.warn('--subject is missing')

    Generator(sys.stdout).flatten(msg)


def cmd_multipart_init(args):
    charset = args['--charset'] or 'utf-8'

    msg = MIMEMultipart()
    if args['--subject']:
        msg['Subject'] = Header(args['--subject'], charset)
    else:
        logger.warn('--subject is missing')

    msg.preamble = 'Multipart message.\n'

    with file(args['<filename>'], 'w') as f:
        Generator(f).flatten(msg)


def cmd_multipart_add(args):
    parser = Parser()
    with file(args['<filename>']) as f:
        msg = parser.parse(f)

    if not msg.is_multipart():
        logger.error('%s is not a multipart message.', args['<filename>'])
        return 1

    with file(args['<part>']) as f:
        part = parser.parse(f)

    if args['--attachment']:
        # attachment_filename = ('utf-8', '', args['--attachment'])
        attachment_filename = args['--attachment']
        part.add_header('Content-Disposition', 'attachment',
                        filename=attachment_filename)
    msg.attach(part)

    with file(args['<filename>'], 'w') as f:
        Generator(f).flatten(msg)
