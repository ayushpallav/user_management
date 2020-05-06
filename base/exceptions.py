from django.http import HttpResponse


class HttpResponseUnauthorized(HttpResponse):
    def __init__(self):
        self.status_code = 401
