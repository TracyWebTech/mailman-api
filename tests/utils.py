
import unittest
from webtest import TestApp


from mailmanapi.routes import get_application


class MailmanAPITestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(MailmanAPITestCase, self).__init__(*args, **kwargs)
        self.client = TestApp(get_application(['127.0.0.1']))
