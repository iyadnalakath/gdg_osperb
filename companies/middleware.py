import time
from django.http import HttpRequest
from django.http.response import HttpResponseBase
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.utils.timezone import now
from .models import ActivityLog


class ActivityLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()
        try:
            request._body = request.body  # Cache request body to prevent re-reading
        except Exception as e:
            request._body = f'Error reading request body: {str(e)}'

    def process_response(self, request: HttpRequest, response: HttpResponseBase):
        execution_time = time.time() - request.start_time
        user = request.user if request.user.is_authenticated else None

        log_response_data = not settings.DEBUG  

        # Avoid storing activity log for activity API
        exclude_url = '/gdg/companies/log/'
        if request.path == exclude_url:
            return response  

        try:
            request_data = request._body.decode('utf-8', errors='replace') if isinstance(request._body, bytes) else str(request._body)
        except Exception as e:
            request_data = f'Error reading request body: {str(e)}'

        try:
            response_data = response.content.decode('utf-8', errors='replace') if log_response_data and hasattr(response, 'content') else ''
        except Exception as e:
            response_data = f'Error reading response content: {str(e)}'

        ActivityLog.objects.create(
            user=user,
            action_type='VIEW',
            timestamp=now(),
            url=request.path,
            method=request.method,
            request_data=request_data,
            response_data=response_data,
            status_code=response.status_code,
            execution_time=execution_time
        )

        return response