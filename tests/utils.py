
import unittest
from webtest import TestApp
from mailmanapi.routes import get_application
from Mailman import MailList


class MailmanAPITestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(MailmanAPITestCase, self).__init__(*args, **kwargs)
        application = get_application(['127.0.0.1'])
        self.client = TestApp(application, extra_environ={
            'REMOTE_ADDR': '127.0.0.1',
        })

    @classmethod
    def create_list(cls, list_name, list_admin='admin@list.com',
                    list_pass='123456', subscribe_policy=0):
        m = MailList.MailList()
        m.Create(list_name, list_admin, list_pass)
        m.subscribe_policy = subscribe_policy
        m.Save()
        m.Unlock()
