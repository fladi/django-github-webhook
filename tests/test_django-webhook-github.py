# -*- coding: utf-8 -*-

import hashlib
import hmac
import json
import unittest

from django.core.exceptions import ImproperlyConfigured
from django.http import (
    HttpResponseNotAllowed,
    HttpResponseBadRequest,
    JsonResponse
)
from django.test import RequestFactory

from django_github_webhook.views import WebHookView


class TestNoSecretView(unittest.TestCase):

    def setUp(self):
        class NoSecretView(WebHookView):
            pass

        self.factory = RequestFactory()
        self.view = NoSecretView.as_view()

    def test_raises_exception(self):
        #import pudb; pu.db
        request = self.factory.post('/fake')
        with self.assertRaises(ImproperlyConfigured):
            self.view(request)


class TestSimpleView(unittest.TestCase):

    def setUp(self):
        class SimpleView(WebHookView):
            secret = 'foobar'

            def ping(self, payload, request):
                return payload

        self.factory = RequestFactory()
        self.view = SimpleView.as_view()
        self.payload = json.dumps({'success': True})
        self.mac_valid = hmac.new(
            self.view.view_class.secret.encode('utf-8'),
            msg=self.payload.encode('utf-8'),
            digestmod=hashlib.sha1
        )
        self.mac_invalid = hmac.new(
            'malicious'.encode('utf-8'),
            msg=self.payload.encode('utf-8'),
            digestmod=hashlib.sha1
        )

    def test_get(self):
        request = self.factory.get('/fake')
        response = self.view(request)
        self.assertIsInstance(response, HttpResponseNotAllowed)

    def test_post(self):
        request = self.factory.post('/fake')
        response = self.view(request)
        self.assertIsInstance(response, HttpResponseBadRequest)

    def test_valid_signature(self):
        request = self.factory.post(
            '/fake',
            self.payload,
            content_type='application/json',
            HTTP_X_GITHUB_EVENT='ping',
            HTTP_X_HUB_SIGNATURE='sha1={mac}'.format(mac=self.mac_valid.hexdigest())
        )
        response = self.view(request)
        self.assertIsInstance(response, JsonResponse)

    def test_invalid_signature(self):
        request = self.factory.post(
            '/fake',
            self.payload,
            content_type='application/json',
            HTTP_X_GITHUB_EVENT='ping',
            HTTP_X_HUB_SIGNATURE='sha1={mac}'.format(mac=self.mac_invalid.hexdigest())
        )
        response = self.view(request)
        self.assertIsInstance(response, HttpResponseBadRequest)

    def test_no_event(self):
        request = self.factory.post(
            '/fake',
            self.payload,
            content_type='application/json',
            HTTP_X_HUB_SIGNATURE='sha1=x'
        )
        response = self.view(request)
        self.assertIsInstance(response, HttpResponseBadRequest)

    def test_invalid_digest(self):
        request = self.factory.post(
            '/fake',
            self.payload,
            content_type='application/json',
            HTTP_X_GITHUB_EVENT='ping',
            HTTP_X_HUB_SIGNATURE='md5=x'
        )
        response = self.view(request)
        self.assertIsInstance(response, HttpResponseBadRequest)

    def test_event_not_allowed(self):
        request = self.factory.post(
            '/fake',
            self.payload,
            content_type='application/json',
            HTTP_X_GITHUB_EVENT='merge',
            HTTP_X_HUB_SIGNATURE='sha1={mac}'.format(mac=self.mac_valid.hexdigest())
        )
        response = self.view(request)
        self.assertIsInstance(response, HttpResponseBadRequest)

    def test_event_not_supported(self):
        request = self.factory.post(
            '/fake',
            self.payload,
            content_type='application/json',
            HTTP_X_GITHUB_EVENT='push',
            HTTP_X_HUB_SIGNATURE='sha1={mac}'.format(mac=self.mac_valid.hexdigest())
        )
        response = self.view(request)
        self.assertIsInstance(response, HttpResponseBadRequest)
