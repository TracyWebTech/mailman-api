

from .utils import MailmanAPITestCase
from Mailman import MailList, UserDesc, Defaults
from time import strftime


class TestAPIv2(MailmanAPITestCase):
    api_version = 'API V2'
    url = '/v2/'
    data = {'address': 'user@email.com'}

    def test_subscribe_no_moderation(self):
        list_name = 'list0'
        path = 'subscribe/'

        self.create_list(list_name)
        resp = self.client.put(self.url + path + list_name,
                               self.data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(0, resp.json)

    def test_subscribe_confirm(self):
        list_name = 'list1'
        path = 'subscribe/'

        self.create_list(list_name, subscribe_policy=1)
        resp = self.client.put(self.url + path + list_name,
                               self.data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(1, resp.json)

    def test_subscribe_approval(self):
        list_name = 'list2'
        path = 'subscribe/'

        self.create_list(list_name, subscribe_policy=2)
        resp = self.client.put(self.url + path + list_name,
                               self.data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(2, resp.json)

    def test_subscribe_banned(self):
        list_name = 'list3'
        path = 'subscribe/'

        self.create_list(list_name)

        mlist = MailList.MailList(list_name)
        mlist.ban_list.append(self.data['address'])
        mlist.Save()
        mlist.Unlock()

        resp = self.client.put(self.url + path + list_name,
                               self.data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(4, resp.json)

    def test_subscribe_already_member(self):
        list_name = 'list4'
        path = 'subscribe/'
        user_desc = UserDesc.UserDesc(self.data['address'], 'fullname', 1)

        self.create_list(list_name)

        mlist = MailList.MailList(list_name)
        mlist.AddMember(user_desc)
        mlist.Save()
        mlist.Unlock()

        resp = self.client.put(self.url + path + list_name,
                               self.data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(3, resp.json)

    def test_subscribe_bad_email(self):
        list_name = 'list5'
        path = 'subscribe/'
        data = {'address': 'user@emailcom'}

        self.create_list(list_name)

        resp = self.client.put(self.url + path + list_name,
                               data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(5, resp.json)

    def test_unsubscribe(self):
        list_name = 'list6'
        path = 'subscribe/'
        user_desc = UserDesc.UserDesc(self.data['address'], 'fullname', 1)

        self.create_list(list_name)

        mlist = MailList.MailList(list_name)
        mlist.AddMember(user_desc)
        mlist.Save()
        mlist.Unlock()

        resp = self.client.delete(self.url + path + list_name,
                                  self.data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(0, resp.json)

    def test_unsubscribe_not_member(self):
        list_name = 'list7'
        path = 'subscribe/'

        self.create_list(list_name)

        resp = self.client.delete(self.url + path + list_name,
                                  self.data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(7, resp.json)

    def test_sendmail(self):
        list_name = 'list9'
        path = 'sendmail/'

        self.create_list(list_name)

        mlist = MailList.MailList(list_name)
        data = {}
        data['email_to'] = mlist.GetListEmail()
        data['message_id'] = 1
        data['ip_from'] = '127.0.0.1'
        data['timestamp'] = strftime('%a, %d %b %Y %H:%M:%S %z (%Z)')
        data['name_from'] = 'user test'
        data['email_from'] = self.data['address']
        data['subject'] = 'subject test'
        data['body'] = 'body test'

        resp = self.client.post(self.url + path + list_name,
                                data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(0, resp.json)

    def test_sendmail_missing_information(self):
        list_name = 'list10'
        path = 'sendmail/'

        self.create_list(list_name)
        resp = self.client.post(self.url + path + list_name,
                                data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(8, resp.json)

    def test_sendmail_unknown_list(self):
        list_name = 'list11'
        path = 'sendmail/'
        data = {}

        resp = self.client.post(self.url + path + list_name,
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
        listname = 'list8'

        self.create_list(listname)

        resp = self.client.get(self.url + path, expect_errors=True)
        total_lists = len(resp.json)
        found = False

        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.json, list)
        self.assertGreaterEqual(total_lists, 1)

        for mlist in resp.json:
            self.assertIsInstance(mlist, dict)
            if mlist.get("listname") == listname:
                found = True

        self.assertTrue(found)

    def test_create_list(self):
        list_name = 'list12'
        path = 'lists/'
        data = {}
        data['admin'] = self.data['address']
        data['password'] = '123456'
        data['subscription_policy'] = 1
        data['archive_privacy'] = 1

        resp = self.client.post(self.url + path + list_name,
                                data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(0, resp.json)

    def test_members(self):
        list_name = 'list13'
        path = 'members/'
        userDesc = UserDesc.UserDesc(self.data['address'], 'fullname', 1)

        self.create_list(list_name)

        mList = MailList.MailList(list_name)
        mList.AddMember(userDesc)
        mList.Save()
        mList.Unlock()

        resp = self.client.get(self.url + path + list_name, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([self.data['address']], resp.json)

    def test_members_unknown_list(self):
        list_name = 'list14'
        path = 'members/'

        resp = self.client.get(self.url + path + list_name, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(12, resp.json)
