import os
import unittest
import subprocess
from sys import stderr
from webtest import TestApp
from mailmanapi.routes import get_application
from Mailman import MailList


class MailmanAPITestCase(unittest.TestCase):

    name = ''
    api_version = ''

    def getName(self):
        """ Get the name of the test """
        self.name = str(self.id).split('=')[-1][:-2]
        self.name = self.name.split('test_')[-1]
        self.name = self.name.replace('_', ' ')

    def __str__(self):
        self.getName()
        out = '\r[%s] %s test ' % (self.api_version, self.name)
        out = out.ljust(70, '-')
        return out + ' '

    def tearDown(self):
        stderr.write(' Done\n')

    def shortDescription(self):
        return "Teste da classe %s" % self.__class__.__name__

    def setUp(self):
        stderr.write(self.__str__())
        self.shortDescription()

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

    @classmethod
    def remove_list(cls, list_name):
        fnull = open(os.devnull, 'w')
        subprocess.call(['/usr/lib/mailman/bin/rmlist', '-a', list_name],
                        stdout=fnull, stderr=subprocess.STDOUT)

    def change_list_attribute(self, attribute, value):
        mlist = MailList.MailList(self.list_name)
        setattr(mlist, attribute, value)
        mlist.Save()
        mlist.Unlock()
