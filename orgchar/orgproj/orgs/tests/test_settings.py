# import logging
# import os
# import sys
#
# import django
# from django.conf import settings
# from orgproj import settings
# from django.test.utils import get_runner
#
# if __name__ == "__main__":
#     os.environ["DJANGO_SETTINGS_MODULE"] = "tests.tests.test_settings"
#     django.setup()
#     TestRunner = get_runner(settings)
#     test_runner = TestRunner()
#     failures = test_runner.run_tests(["tests"])
#     sys.exit(bool(failures))


# settings.configure()
# django.setup()
#
# settings.configure(
#     DATABASES={
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': ':memory:',
#         }
#     },
#     LOGGING_CONFIG=False,
#     LOGGING={
#         'version': 1,
#         'disable_existing_loggers': False,
#         'handlers': {
#             'console': {
#                 'level': 'DEBUG',
#                 'class': 'logging.StreamHandler',
#             },
#         },
#         'root': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#     },
# )

# logging.config.dictConfig(LOGGING)


# SECRET_KEY = "fake-key"
# INSTALLED_APPS = [
#     "tests",
#     "orgs",
# ]

# if __name__ == "__main__":
#     os.environ["DJANGO_SETTINGS_MODULE"] = "tests.tests.test_settings"
#     django.setup()
#     TestRunner = get_runner(settings)
#     test_runner = TestRunner()
#     failures = test_runner.run_tests(["tests"])
#     sys.exit(bool(failures))
