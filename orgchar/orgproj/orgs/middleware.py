import uuid

from django.shortcuts import redirect
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# logger.setLevel(logging.WARNING)


class CustomMiddlewareToken:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        request.session.set_expiry(60 * 30)
        logger.debug(request.path_info)

        response = self._get_response(request)
        # Код, выполняемый при обработке каждого запроса после представления
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if '/edit-choice/' in request.path and not request.path.endswith('/edit-choice/'):
            if 'edit_token' not in request.COOKIES:
                logger.warning(f"Suspicious activity of {request.user}")
                # Надо добавить генерацию email о подозрительной активности
                return redirect('edit-choice')


    # @staticmethod
    # def set_custom_stats_cookie(request):
    #     if request.session.get("stats", False):
    #         request.session["stats"] = uuid.uuid4()




# class CustomMiddlewareToken:
#     def __init__(self, get_response):
#         self._get_response = get_response
#
#     def __call__(self, request):
#         if '/edit-choice/' in request.path and not request.path.endswith('/edit-choice/'):
#             if 'edit_token' not in request.session:
#                 # Надо добавить генерацию email о подозрительной активности
#                 return redirect('edit-choice')
#             # logger.warning(f"Suspicious activity of {request.user}")
#
#         response = self._get_response(request)
#         # Код, выполняемый при обработке каждого запроса после представления
#         return response