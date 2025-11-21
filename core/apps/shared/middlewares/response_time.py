import time

from django.utils.deprecation import MiddlewareMixin


class ResponseTimeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        if hasattr(request, "start_time"):
            response_time = time.time() - request.start_time
            response["X-Response-Time"] = f"{response_time:.3f}s"
        return response
