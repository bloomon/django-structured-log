import django


def get_wsgi_application():
    """
    The public interface to Django's WSGI support. Return a WSGI callable.

    Avoids making django.core.handlers.WSGIHandler a public API, in case the
    internal WSGI implementation changes or moves in the future.
    """
    from .request_handler import WSGIHandler

    django.setup(set_prefix=False)
    return WSGIHandler()
