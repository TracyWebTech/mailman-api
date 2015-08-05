

from .utils import MailmanAPITestCase
from Mailman import MailList, UserDesc


class TestAPIv2(MailmanAPITestCase):

    url = '/v2/'
    data = {'address' : 'user@email.com'}

    def test_subscribe_no_moderation(self):
        list_name = 'list0'

        self.create_list(list_name)
        resp = self.client.put(self.url + list_name, self.data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(0, resp.json)

    def test_subscribe_confirm(self):
        list_name = 'list1'

        self.create_list(list_name, subscribe_policy=1)
        resp = self.client.put(self.url + list_name, self.data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(1, resp.json)

    def test_subscribe_approval(self):
        list_name = 'list2'

        self.create_list(list_name, subscribe_policy=2)
        resp = self.client.put(self.url + list_name, self.data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(2, resp.json)

    def test_subscribe_banned(self):
        list_name = 'list3'

        self.create_list(list_name)

        mList = MailList.MailList(list_name)
        mList.ban_list.append(self.data['address'])
        mList.Save()
        mList.Unlock()

        resp = self.client.put(self.url + list_name, self.data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(4, resp.json)

    def test_subscribe_already_member(self):
        list_name = 'list4'
        userDesc = UserDesc.UserDesc(self.data['address'], 'fullname', 1)

        self.create_list(list_name)

        mList = MailList.MailList(list_name)
        mList.AddMember(userDesc)
        mList.Save()
        mList.Unlock()

        resp = self.client.put(self.url + list_name, self.data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(3, resp.json)

    def test_subscribe_bad_email(self):
        list_name = 'list5'
        data = {'address' : 'user@emailcom'}

        self.create_list(list_name)

        resp = self.client.put(self.url + list_name, data, expect_errors=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(5, resp.json)