
import subprocess

from .utils import MailmanAPITestCase

from Mailman import MailList, Utils


class TestAPIv1(MailmanAPITestCase):

    def setUp(self):
        self.list_names = Utils.list_names()

    def test_list_lists_bare(self):
        resp = self.client.get('/', expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(sorted(self.list_names), sorted(resp.json))

    def test_list_lists_description(self):
        lists = []
        for list_name in self.list_names:
            list_ = MailList.MailList(list_name, False)
            lists.append([list_name, list_.description])

        resp = self.client.get('/?description=1', expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(sorted(lists), sorted(resp.json))

    def test_list_lists_private(self):
        lists = []
        for list_name in self.list_names:
            list_ = MailList.MailList(list_name, False)
            lists.append([list_name, bool(list_.archive_private)])

        resp = self.client.get('/?private=1', expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(sorted(lists), sorted(resp.json))

    def test_list_lists_all(self):
        lists = []
        for list_name in self.list_names:
            list_ = MailList.MailList(list_name, False)
            lists.append([
                list_name,
                list_.description,
                bool(list_.archive_private),
            ])

        resp = self.client.get('/?private=0&description=1', expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(sorted(lists), sorted(resp.json))
