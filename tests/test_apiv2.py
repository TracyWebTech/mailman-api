

from .utils import MailmanAPITestCase
from Mailman import MailList, UserDesc, Defaults
from time import strftime


class TestAPIv2(MailmanAPITestCase):
    api_version = 'API V2'
    url = '/v2/'
    data = {'address': 'user@email.com'}
    list_name = 'list'

    def setUp(self):
        super(TestAPIv2, self).setUp()
        self.create_list(self.list_name)

    def tearDown(self):
        super(TestAPIv2, self).tearDown()
        self.remove_list(self.list_name)

    def test_subscribe_no_moderation(self):
        path = 'subscribe/'

        self.change_list_attribute('subscribe_policy', 0)
        resp = self.client.put(self.url + path + self.list_name,
                               self.data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(0, resp.json)

    def test_subscribe_confirm(self):
        path = 'subscribe/'

        self.change_list_attribute('subscribe_policy', 1)
        resp = self.client.put(self.url + path + self.list_name,
                               self.data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(1, resp.json)

    def test_subscribe_approval(self):
        path = 'subscribe/'

        self.change_list_attribute('subscribe_policy', 2)
        resp = self.client.put(self.url + path + self.list_name,
                               self.data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(2, resp.json)

    def test_subscribe_banned(self):
        path = 'subscribe/'
        mlist = MailList.MailList(self.list_name)
        mlist.ban_list.append(self.data['address'])
        mlist.Save()
        mlist.Unlock()

        resp = self.client.put(self.url + path + self.list_name,
                               self.data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(4, resp.json)

    def test_subscribe_already_member(self):
        path = 'subscribe/'
        user_desc = UserDesc.UserDesc(self.data['address'], 'fullname', 1)
        mlist = MailList.MailList(self.list_name)
        mlist.AddMember(user_desc)
        mlist.Save()
        mlist.Unlock()

        resp = self.client.put(self.url + path + self.list_name,
                               self.data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(3, resp.json)

    def test_subscribe_bad_email(self):
        path = 'subscribe/'
        data = {'address': 'user@emailcom'}
        resp = self.client.put(self.url + path + self.list_name,
                               data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(5, resp.json)

    def test_unsubscribe(self):
        path = 'subscribe/'
        user_desc = UserDesc.UserDesc(self.data['address'], 'fullname', 1)
        mlist = MailList.MailList(self.list_name)
        mlist.AddMember(user_desc)
        mlist.Save()
        mlist.Unlock()

        resp = self.client.delete(self.url + path + self.list_name,
                                  self.data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(0, resp.json)

    def test_unsubscribe_not_member(self):
        path = 'subscribe/'
        resp = self.client.delete(self.url + path + self.list_name,
                                  self.data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(7, resp.json)

    def test_sendmail(self):
        path = 'sendmail/'
        mlist = MailList.MailList(self.list_name)
        data = {}
        data['email_to'] = mlist.GetListEmail()
        data['message_id'] = 1
        data['ip_from'] = '127.0.0.1'
        data['timestamp'] = strftime('%a, %d %b %Y %H:%M:%S %z (%Z)')
        data['name_from'] = 'user test'
        data['email_from'] = self.data['address']
        data['subject'] = 'subject test'
        data['body'] = 'body test'

        resp = self.client.post(self.url + path + self.list_name,
                                data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(0, resp.json)

    def test_sendmail_missing_information(self):
        path = 'sendmail/'
        data = {}
        resp = self.client.post(self.url + path + self.list_name,
                                data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(8, resp.json)

    def test_sendmail_unknown_list(self):
        path = 'sendmail/'
        data = {}

        resp = self.client.post(self.url + path + 'unknown_list',
                                data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(12, resp.json)

    def test_mailman_site_list_not_listed_among_lists(self):
        path = 'lists/'
        mailman_site_list = Defaults.MAILMAN_SITE_LIST

        self.create_list(mailman_site_list)

        resp = self.client.get(self.url + path, expect_errors=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.json, list)

        for mlist in resp.json:
            self.assertIsInstance(mlist, dict)
            self.assertNotEqual(mlist.get("listname"), mailman_site_list)

    def test_list_lists(self):
        path = 'lists/'

        resp = self.client.get(self.url + path, expect_errors=True)
        total_lists = len(resp.json)
        found = False

        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.json, list)
        self.assertGreaterEqual(total_lists, 1)

        for mlist in resp.json:
            self.assertIsInstance(mlist, dict)
            if mlist.get("listname") == self.list_name:
                found = True

        self.assertTrue(found)

    def test_create_list(self):
        new_list = 'new_list'
        url = self.url + 'lists/' + new_list

        data = {'admin': self.data['address'], 'password': '123456',
                'subscription_policy': 1, 'archive_privacy': 1}

        resp = self.client.post(url, data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(0, resp.json)
        self.remove_list(new_list)

    def test_members(self):
        list_name = 'list13'
        path = 'members/'
        user_desc = UserDesc.UserDesc(self.data['address'], 'fullname', 1)

        self.create_list(list_name)

        mlist = MailList.MailList(list_name)
        mlist.AddMember(user_desc)
        mlist.Save()
        mlist.Unlock()

        resp = self.client.get(self.url + path + list_name, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([self.data['address']], resp.json)

    def test_members_unknown_list(self):
        list_name = 'list14'
        path = 'members/'

        resp = self.client.get(self.url + path + list_name, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(12, resp.json)
