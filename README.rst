mailman-api
===========

Introduction
------------

`mailman-api` provides a daemon that will listen to HTTP requests,
providing access to a REST API that can be used to interact with a
locally-installed Mailman instance.

Usage
-----

::

    $ mailman-api [OPTIONS]

OPTIONS
--------

::

    -h, --help            show this help message and exit
    -b BIND, --bind=BIND  Bind address. Default: '127.0.0.1:8000'.
    --allow-from=ALLOW_FROM
                          IPs to allow incoming requests. By deufalt only allow
                          connections from '127.0.0.1'.
    -l MAILMANLIB_PATH, --mailman-lib-path=MAILMANLIB_PATH
                          Path to mailman libs directory. Default:
                          '/usr/lib/mailman'.
    -d, --debug           Print debug information



API usage
---------

Requests can be made to any of the URI's below, strictly using the HTTP
methods indicated.

The body of all responses contains valid JSON objects. Unless otherwise
noted, successful requests get as response a 200 (OK) status code for
response, and `true` in the response body. Failed requests will get
responses with some HTTP error code in the 400s, and a string describing
the problem in the response body.

Supported methods:

* `GET /`

  Lists existing mailing lists on the server.

  Takes no arguments.

  Returns a list of the mailing lists that exist on this server.

* `GET /<listname>`

  Lists subscribers.

  Takes no arguments.

  Returns an array of email addresses.

* `PUT /<listname>`

  Adds a new subscriber to the list called `<listname>`

  Arguments:

    * `address`: email address that is to be subscribed to the list.
    * `fullname`: full name of the person being subscribed to the list.
    * `digest`: if this equals `true`, the new subscriber will receive
      digests instead of every mail sent to the list.

* `DELETE /<listname>`

  Unsubsribe an email address from the mailing list.

  Arguments:

  * `address`: email address that is to be unsubscribed from the list

* `POST /<listname>/sendmail`

  Posts an email to the mailing list.

  Arguments:

  * `name_from`: name of the poster
  * `email_from`: email address of the poster
  * `subject`: the subject of the message
  * `body`: the body of the message.
  * `in_reply_to` (optional): Message-ID of the message that is being
    replied to, if any.


Licensing information
---------------------

Copyright (C) 2013-2014 Sergio Oliveira Campos

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
