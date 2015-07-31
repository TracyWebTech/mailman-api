
import unittest
from webtest import TestApp


from mailmanapi.routes import get_application


class MailmanAPITestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(MailmanAPITestCase, self).__init__(*args, **kwargs)
        application = get_application(['127.0.0.1'])
        self.client = TestApp(application, extra_environ={
            'REMOTE_ADDR': '127.0.0.1',
        })
