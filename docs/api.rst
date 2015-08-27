API Documentation
=================

Requests can be made to any of the URI's below, strictly using the HTTP methods indicated.

The body of all responses contains valid JSON objects. Unless otherwise noted, successful requests get as response a 200 (OK) status code for response, and true in the response body. Failed requests will get responses with some HTTP error code in the 400s, and a string describing the problem in the response body.

Supported methods:

API V1
------

list_lists
++++++++++
Lists existing mailing lists on the server.

    **Method**: GET

    **URI**: /

    Returns a list of the mailing lists that exist on this server.

subscribe
+++++++++
Adds a new subscriber to the list called `<listname>`

    **Method**: PUT

    **URI**: /<listname>

    **Parameters**:

      * `address`: email address that is to be subscribed to the list.
      * `fullname`: full name of the person being subscribed to the list.
      * `digest`: if this equals `true`, the new subscriber will receive
        digests instead of every mail sent to the list.

unsubscribe
+++++++++++
Unsubscribe an email address from the mailing list.

    **Method**: DELETE

    **URI**: /<listname>

    **Parameters**:

      * `address`: email address that is to be unsubscribed from the list

members
+++++++
Lists subscribers for the `listname` list.

    **Method**: GET

    **URI**: /<listname>

    Returns an array of email addresses.
sendmail
++++++++
Posts an email to the mailing list.

    **Method**: POST

    **URI**: /<listname>/sendmail

    **Parameters**:

      * `name_from`: name of the poster
      * `email_from`: email address of the poster
      * `subject`: the subject of the message
      * `body`: the body of the message.
      * `in_reply_to` (optional): Message-ID of the message that is being
        replied to, if any.

API V2
------

list_lists
++++++++++
Lists existing mailing lists on the server.

    **Method**: GET

    **URI**: /v2/

    Returns a list of dictionaries the mailing lists and its public attributes that exist on this server.

create_list
+++++++++++
Create a mail list.

    **Method**: POST

    **URI**: /v2/lists/<listname>

    **Parameters**:

      * `admin`: email of list admin
      * `password`: list admin password
      * `subscription_policy`: 1) Confirm; 2) Approval; 3)Confirm and approval.
      Default is Confirm (1)
      * `archive_privacy`: 0) Public; 1) Private. Default is Public (0)

subscribe
+++++++++
Adds a new subscriber to the list called `<listname>`

    **Method**: PUT

    **URI**: /v2/subscribe/<listname>

    **Parameters**:

      * `address`: email address that is to be subscribed to the list.
      * `fullname`: full name of the person being subscribed to the list.
      * `digest`: if this equals `true`, the new subscriber will receive
        digests instead of every mail sent to the list.

unsubscribe
+++++++++++
Unsubscribe an email address from the mailing list.

    **Method**: DELETE

    **URI**: /v2/subscribe/<listname>

    **Parameters**:

      * `address`: email address that is to be unsubscribed from the list

members
+++++++
Lists subscribers for the `listname` list.

    **Method**: GET

    **URI**: /v2/members/<listname>

    Returns an array of email addresses.

sendmail
++++++++
Posts an email to the mailing list.

    **Method**: POST

    **URI**: /v2/sendmail/<listname>

    **Parameters**:

      * `name_from`: name of the poster
      * `email_from`: email address of the poster
      * `subject`: the subject of the message
      * `body`: the body of the message.
      * `in_reply_to` (optional): Message-ID of the message that is being
        replied to, if any.

.. automodule:: mailmanapi.api
      :members:
