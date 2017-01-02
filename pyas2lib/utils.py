from __future__ import absolute_import, unicode_literals
from .compat import StringIO, BytesIO, Generator, BytesGenerator
import email
import re
from uuid import uuid1


def unquote_as2name(quoted_name):
    return email.utils.unquote(quoted_name)


def quote_as2name(unquoted_name):
    if re.search(r'[\\" ]', unquoted_name, re.M):
        return '"' + email.utils.quote(unquoted_name) + '"'
    else:
        return unquoted_name


def mime_to_string(msg, header_len):
    fp = StringIO()
    g = Generator(fp, maxheaderlen=header_len)
    g.flatten(msg)
    return fp.getvalue()


def mime_to_bytes(msg, header_len):
    fp = BytesIO()
    g = BytesGenerator(fp, maxheaderlen=header_len)
    g.flatten(msg)
    return fp.getvalue()


def canonicalize(message):

    if message.is_multipart():
        # # parts = []
        # message.set_boundary(uuid1())
        # message_boundary = ('--' + message.get_boundary()).encode('utf-8')
        # message_body = ''
        # for part in message.walk():
        #     part_header = ''
        #     for k, v in part.items():
        #         part_header += '{}: {}\n'.format(k, v)
        #     part_header += '\n'
        #     # print part.as_string()
        #     print part.get_payload()
                # message_body += \
                #     message_boundary + \
                #     part_header.encode('utf-8') + \
                #     part.get_payload(decode=False)
        # message_body += message_boundary + '--'.encode('utf-8')
        # print message_body
        # message.set_boundary(uuid1())
        # message_boundary = '--' + message.get_boundary()

        return mime_to_bytes(message, 0).replace(
            '\r\n', '\n').replace('\r', '\n').replace('\n', '\r\n')
    else:
        message_header = ''
        message_body = message.get_payload(decode=True)
        for k, v in message.items():
            message_header += '{}: {}\r\n'.format(k, v)
        message_header += '\r\n'
        return message_header.encode('utf-8') + message_body
