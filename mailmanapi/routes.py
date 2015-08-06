
from bottle import default_app
from . import apiv1
from . import apiv2


def create_routes(app):

    # v1
    app.route('/', method='GET',
              callback=apiv1.list_lists)
    app.route('/<listname>', method='PUT',
              callback=apiv1.subscribe)
    app.route('/<listname>', method='DELETE',
              callback=apiv1.unsubscribe)
    app.route('/<listname>', method='GET',
              callback=apiv1.members)
    app.route('/<listname>/sendmail', method='POST',
              callback=apiv1.sendmail)

    # v2
    app.route('/v2/lists/', method='GET',
              callback=apiv1.list_lists)
    app.route('/v2/lists/<listname>', method='POST',
              callback=apiv2.create_list)
    app.route('/v2/subscribe/<listname>', method='PUT',
              callback=apiv2.subscribe)
    app.route('/v2/subscribe/<listname>', method='DELETE',
              callback=apiv2.unsubscribe)
    app.route('/v2/members/<listname>', method='GET',
              callback=apiv1.members)
    app.route('/v2/sendmail/<listname>', method='POST',
              callback=apiv1.sendmail)


def get_application(allowed_ips):
    bottle_app = default_app()

    def application(environ, start_response):
        create_routes(bottle_app)

        if environ['REMOTE_ADDR'] not in allowed_ips:
            status = '403 FORBIDDEN'
            headers = [('Content-type', 'text/plain')]
            start_response(status, headers)
            return 'FORBIDDEN'

        return bottle_app(environ, start_response)
    return application
