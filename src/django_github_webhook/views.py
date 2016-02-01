# -*- coding: utf-8 -*-

import hashlib
import hmac
import json

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.generic import View


class WebHookView(View):
    secret = None
    allowed_events = [
        'commit_comment',
        'create',
        'delete',
        'deployment',
        'deployment_status',
        'fork',
        'gollum',
        'issue_comment',
        'issues',
        'member',
        'membership',
        'page_build',
        'ping',
        'public',
        'pull_request',
        'pull_request_review_comment',
        'push',
        'release',
        'repository',
        'status',
        'team_add',
        'watch',
    ]

    def get_secret(self):
        return self.secret

    def get_allowed_events(self):
        return self.allowed_events

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(WebHookView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        secret = self.get_secret()
        if not secret:
            raise ImproperlyConfigured('GitHub webhook secret ist not defined.')
        if 'HTTP_X_HUB_SIGNATURE' not in request.META:
            return HttpResponseBadRequest('Request does not contain X-GITHUB-SIGNATURE header')
        if 'HTTP_X_GITHUB_EVENT' not in request.META:
            return HttpResponseBadRequest('Request does not contain X-GITHUB-EVENT header')
        digest_name, signature = request.META['HTTP_X_HUB_SIGNATURE'].split('=')
        if digest_name != 'sha1':
            return HttpResponseBadRequest('Unsupported X-HUB-SIGNATURE digest mode found: {}'.format(digest_name))
        mac = hmac.new(
            secret.encode('utf-8'),
            msg=request.body,
            digestmod=hashlib.sha1
        )
        if not hmac.compare_digest(mac.hexdigest(), signature):
            return HttpResponseBadRequest('Invalid X-HUB-SIGNATURE header found')
        event = request.META['HTTP_X_GITHUB_EVENT']
        if event not in self.get_allowed_events():
            return HttpResponseBadRequest('Unsupported X-GITHUB-EVENT header found: {}'.format(event))
        handler = getattr(self, event, None)
        if not handler:
            return HttpResponseBadRequest('Unsupported X-GITHUB-EVENT header found: {}'.format(event))
        payload = json.loads(request.body.decode('utf-8'))
        response = handler(payload, request, *args, **kwargs)
        return JsonResponse(response)
