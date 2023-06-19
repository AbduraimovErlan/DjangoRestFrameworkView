from django.shortcuts import render
from django.views import View


"""

http_method_names = []
view_is_async = False

"""


def _allowed_methods(self):
    return [m.upper() for m in self.http_method_names if hasattr(self, m)]