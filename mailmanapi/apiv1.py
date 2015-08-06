
import os
import uuid
import logging

from bottle import request, template

try:
    from Mailman import Utils, Errors, Post, mm_cfg
except ImportError:  # pragma: no cover
    logging.error('Could not import Mailman module')

from .members import Member
from .utils import parse_boolean, jsonify, get_mailinglist, get_timestamp


CWD = os.path.abspath(os.path.dirname(__file__))
EMAIL_TEMPLATE = os.path.join(CWD, 'templates', 'message.tpl')


def list_lists():
    """Lists existing mailing lists on the server.

    **Method**: GET

    **URI**: /

    Returns a list of the mailing lists that exist on this server."""

    all_lists = Utils.list_names()
    lists = []

    include_description = request.query.get('description')
    include_private = request.query.get('private')

    address = request.query.get('address')
    for listname in all_lists:
        mlist = get_mailinglist(listname, lock=False)
        members = mlist.getMembers()
        if not address or address in members:
            list_values = [listname]
            if include_description:
                list_values.append(mlist.description.decode('latin1'))
            if include_private:
                list_values.append(bool(mlist.archive_private))

            if len(list_values) == 1:
                lists.append(list_values[0])
            else:
                lists.append(list_values)

    return jsonify(lists)


def subscribe(listname):
    """Adds a new subscriber to the list called `<listname>`

    **Method**: PUT

    **URI**: /<listname>

    **Parameters**:

      * `address`: email address that is to be subscribed to the list.
      * `fullname`: full name of the person being subscribed to the list.
      * `digest`: if this equals `true`, the new subscriber will receive
        digests instead of every mail sent to the list.

    """

    address = request.forms.get('address')
    fullname = request.forms.get('fullname')
    digest = parse_boolean(request.forms.get('digest'))

    mlist = get_mailinglist(listname)
    userdesc = Member(fullname, address, digest)

    try:
        mlist.AddMember(userdesc)
    except Errors.MMAlreadyAMember:
        return jsonify("Address already a member.", 409)
    except Errors.MembershipIsBanned:
        return jsonify("Banned address.", 403)
    except (Errors.MMBadEmailError, Errors.MMHostileAddress):
        return jsonify("Invalid address.", 400)

    else:
        mlist.Save()
    finally:
        mlist.Unlock()

    return jsonify(True)


def unsubscribe(listname):
    """Unsubscribe an email address from the mailing list.

    **Method**: DELETE

    **URI**: /<listname>

    **Parameters**:

      * `address`: email address that is to be unsubscribed from the list

    """

    address = request.forms.get('address')
    mlist = get_mailinglist(listname)

    try:
        mlist.ApprovedDeleteMember(address, admin_notif=False, userack=True)
        mlist.Save()
    except Errors.NotAMemberError:
        return jsonify("Not a member.", 404)
    finally:
        mlist.Unlock()

    return jsonify(True)


def members(listname):
    """Lists subscribers for the `listname` list.

    **Method**: GET

    **URI**: /<listname>

    Returns an array of email addresses."""

    mlist = get_mailinglist(listname, lock=False)
    return jsonify(mlist.getMembers())


def sendmail(listname):
    """Posts an email to the mailing list.

    **Method**: POST

    **URI**: /<listname>/sendmail

    **Parameters**:

      * `name_from`: name of the poster
      * `email_from`: email address of the poster
      * `subject`: the subject of the message
      * `body`: the body of the message.
      * `in_reply_to` (optional): Message-ID of the message that is being
        replied to, if any."""

    mlist = get_mailinglist(listname, lock=False)

    context = {}
    context['email_to'] = mlist.GetListEmail()
    context['message_id'] = uuid.uuid1()
    context['ip_from'] = request.environ.get('REMOTE_ADDR')
    context['timestamp'] = get_timestamp()

    context['name_from'] = request.forms.get('name_from')
    context['email_from'] = request.forms.get('email_from')
    context['subject'] = request.forms.get('subject')
    context['body'] = request.forms.get('body')

    in_reply_to = request.forms.get('in_reply_to')
    if in_reply_to:
        context['in_reply_to'] = in_reply_to

    if None in context.values():
        return jsonify('Missing information. `email_from`, `subject` and '
                       '`body` are mandatory', 400)

    email = template(EMAIL_TEMPLATE, context)
    Post.inject(listname, email.encode('utf8'), qdir=mm_cfg.INQUEUE_DIR)
    return jsonify(True)
