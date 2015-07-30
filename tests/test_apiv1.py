

from .utils import MailmanAPITestCase


class TestAPIv1(MailmanAPITestCase):

    def test_tests(self):
        self.client.get('/')
        assert True
