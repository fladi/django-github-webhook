=====
Usage
=====

.. _GitHub events: https://developer.github.com/v3/activity/events/types/

To use django-github-webhook in a project where you want to receive webhooks for ``push`` events::

    from django_github_webhook.views import WebHookView


    class MyWebHookReceiverView(WebHookView):
        secret = 'foobar'

        def push(self, payload, request):
            ''' Do something with the payload and return a JSON serializeable value. '''
            return {'status': 'received'}


If the secret has to be dynamically fetched for each request you should override the ``get_secret`` method::

    from .models import Hook

    class MyWebHookReceiverView(WebHookView):

        def get_secret(self):
            hook = Hook.objects.get(pk=self.request.kwargs['id'])
            return hook.secret

Each webhook can receive multiple `GitHub events`_ by implementing methods with the same name as the events. Right now the following events are accepted:

 * commit_comment
 * create
 * delete
 * deployment
 * deployment_status
 * fork
 * gollum
 * issue_comment
 * issues
 * member
 * membership
 * page_build
 * ping
 * public
 * pull_request
 * pull_request_review_comment
 * push
 * release
 * repository
 * status
 * team_add
 * watch

So in order to accept events of type ``fork`` and ``watch`` implement methods as follows. The ``payload`` parameter gets the already decoded JSON payload from
the request body::

    class MyWebHookReceiverView(WebHookView):

        def fork(self, payload, request):
            print('Forked by {payload[forkee][full_name]}'.format(payload=payload))
            return {'status': 'forked'}

        def watch(self, payload, request):
            print('Watched by {payload[sender][login]}'.format(payload=payload))

