

from .utils import MailmanAPITestCase
from Mailman import MailList, UserDesc, Defaults


class TestAPIv2(MailmanAPITestCase):

    url = '/v2/'
    data = {'address' : 'user@email.com'}

    def test_subscribe_no_moderation(self):
        list_name = 'list0'
        path = 'subscribe/'

        self.create_list(list_name)
        resp = self.client.put(self.url + path + list_name, self.data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(0, resp.json)

    def test_subscribe_confirm(self):
        list_name = 'list1'
        path = 'subscribe/'

        self.create_list(list_name, subscribe_policy=1)
        resp = self.client.put(self.url + path + list_name, self.data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(1, resp.json)

    def test_subscribe_approval(self):
        list_name = 'list2'
        path = 'subscribe/'

        self.create_list(list_name, subscribe_policy=2)
        resp = self.client.put(self.url + path + list_name, self.data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(2, resp.json)

    def test_subscribe_banned(self):
        list_name = 'list3'
        path = 'subscribe/'

        self.create_list(list_name)

        mList = MailList.MailList(list_name)
        mList.ban_list.append(self.data['address'])
        mList.Save()
        mList.Unlock()

        resp = self.client.put(self.url + path + list_name, self.data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(4, resp.json)

    def test_subscribe_already_member(self):
        list_name = 'list4'
        path = 'subscribe/'
        userDesc = UserDesc.UserDesc(self.data['address'], 'fullname', 1)

        self.create_list(list_name)

        mList = MailList.MailList(list_name)
        mList.AddMember(userDesc)
        mList.Save()
        mList.Unlock()

        resp = self.client.put(self.url + path + list_name, self.data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(3, resp.json)

    def test_subscribe_bad_email(self):
        list_name = 'list5'
        path = 'subscribe/'
        data = {'address' : 'user@emailcom'}

        self.create_list(list_name)

        resp = self.client.put(self.url + path + list_name, data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(5, resp.json)

    def test_unsubscribe(self):
        list_name = 'list6'
        path = 'subscribe/'
        userDesc = UserDesc.UserDesc(self.data['address'], 'fullname', 1)

        self.create_list(list_name)

        mList = MailList.MailList(list_name)
        mList.AddMember(userDesc)
        mList.Save()
        mList.Unlock()

        resp = self.client.delete(self.url + path + list_name, self.data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(0, resp.json)

    def test_unsubscribe_not_member(self):
        list_name = 'list7'
        path = 'subscribe/'

        self.create_list(list_name)

        resp = self.client.delete(self.url + path + list_name, self.data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(7, resp.json)

    def test_mailman_site_list_not_listed_among_lists(self):
        path = 'lists/'
        mailman_site_list = Defaults.MAILMAN_SITE_LIST

        resp = self.client.get(self.url + path, expect_errors=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.json, list)

        for mlist in resp.json:
            self.assertIsInstance(mlist, dict)
            self.assertNotEqual(mlist.get("listname"), mailman_site_list)
