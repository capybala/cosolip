#!/usr/bin/env python
#coding: utf-8

import os
import re
import webapp2 as webapp
from google.appengine.ext.webapp import template
from google.appengine.api import mail

messages = {
    '1': 'チャック…あいてますよ',
    '2': 'スカート…めくれてますよ',
    '3': 'ストッキング…伝染してますよ',
    '4': '歯に…はさまってますよ',
    '5': '服に…タグついてますよ',
    '6': 'お口…臭いですよ',
}


class MainHandler(webapp.RequestHandler):

    def get(self):
        params = {}
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, params))


class ToHandler(webapp.RequestHandler):

    def get(self):
        mode = self.request.get('mode')
        if not re.search(r'^[1-6]$', mode):
            self.response.set_status(404)
            return

        params = {
            'mode': self.request.get('mode'),
        }
        path = os.path.join(os.path.dirname(__file__), 'to.html')
        self.response.out.write(template.render(path, params))

    def post(self):
        email = self.request.get('email')
        mode = self.request.get('mode')

        if not re.search(r'^[1-6]$', mode):
            self.response.set_status(404)
            return

        error = ''
        if not email:
            error = 'メールアドレスを入力してください'
        elif (not mail.is_email_valid(email)) or (re.search('^[^@]+@[^@]+$', email) is None):
            error = 'メールアドレスの形式をお確かめください'

        if error:
            params = {
                'mode': mode,
                'email': email,
                'error': error,
            }
            path = os.path.join(os.path.dirname(__file__), 'to.html')
            self.response.out.write(template.render(path, params))
            return

        sender = 'capybala@gmail.com'
        subject = 'コソリップからこっそりとお知らせです'
        body = messages[mode]

        params = {
            'base_url': 'http://cosolip.appspot.com/',
            'mode': mode,
        }
        path = os.path.join(os.path.dirname(__file__), 'mail.html')
        # for debug in browser
        # self.response.out.write(template.render(path, params))
        # return
        html = template.render(path, params)
        mail.send_mail(sender, email, subject, body, html=html)

        self.redirect('/sent?mode=%s' % mode)


class SentHandler(webapp.RequestHandler):

    def get(self):
        mode = self.request.get('mode')
        if not re.search(r'^[1-6]$', mode):
            self.response.set_status(404)
            return

        params = {
            'mode': mode,
        }
        path = os.path.join(os.path.dirname(__file__), 'sent.html')
        self.response.out.write(template.render(path, params))


app = webapp.WSGIApplication(
    [
        ('/', MainHandler),
        ('/to', ToHandler),
        ('/sent', SentHandler),
    ])
