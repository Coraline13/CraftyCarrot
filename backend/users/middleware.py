from django.contrib.sessions.middleware import SessionMiddleware as DjangoSessionMiddleware

from main.api import is_api_request


class TokenSessionMiddleware(DjangoSessionMiddleware):
    """
    Middleware that authenticates against a token in the http authorization
    header and blocks cookies and csrf protection on token endpoints.
    """
    block_cookies = True

    def should_block_cookies(self, request, response=None):
        return self.block_cookies and is_api_request(request)

    def process_request(self, request):
        if is_api_request(request):
            if self.should_block_cookies(request):
                request.COOKIES.clear()
                request.META.pop('HTTP_COOKIE', None)
                request.csrf_processing_done = True
                request._dont_enforce_csrf_checks = True

        super().process_request(request)

    def process_response(self, request, response):
        if self.should_block_cookies(request, response):
            response.cookies.clear()

        response = super().process_response(request, response)

        if self.should_block_cookies(request, response):
            response.cookies.clear()
            del response['Set-Cookie']

        return response
