from django.shortcuts import render
from django.views import View


"""

http_method_names = []
view_is_async = False

"""


def _allowed_methods(self):
    return [m.upper() for m in self.http_method_names if hasattr(self, m)]


@classmethod
def as_view(cls, **initkwargs):
    """ Main entry point for a request-response process."""
    for key in initkwargs:
        if key in cls.http_method_names:
            raise TypeError(
                "The method name %s is not accepted as a keyword argument "
                "to %s(). %(key, cls.__name__)"
            )
        if not hasattr(cls, key):
            raise TypeError(
                "%s() received an invalid keyword %r. as_view "
                "only accepts arguments that are already"
                "attributes of the class." %(cls.__name__, key)
            )
    def view(request, *args, **kwargs):
        self = cls(**initkwargs)
        self.setup(request, *args, **kwargs)
        if not hasattr(self, "request"):
            raise AttributeError(
                "%s instance has no 'request' attribute. Did you override "
                "setup() and forget to call super()?" %cls.__name__
            )
        return self.dispatch(request, *args, **kwargs)
    view.view_class = cls
    view.view_initkwargs = initkwargs
    # __name__ and __qualname__ are intentionally left unchanged as
    # view_class should be used to robustly determine the name of the view
    # instead.
    view.__doc__ = cls.__doc__
    view.__module__ = cls.__module__
    view.__annotations__ = cls.dispatch.__annotations__
    # Copy possible attributes set by decorators, e.g. @csrf_exempt, from
    # the despatch method.
    view.__dict__.update(cls.dispatch.__dict__)
    # Mark the callback if the view class is async.
    if cls.view_is_async:
        markcoroutinefunction(view)
    return view




def dispatch(self, request, *args, **kwargs):
    # Try to dispatch to the right method; if a method doesn't exist,
    # defer to the error handler. Also defer to the error handler if the
    # request method isn't on the approved list.
    if request.method.lower() in self.http_method_names:
        handler = getattr(
            self, request.method.lower(), self.http_method_not_allowed
        )
    else:
        handler = self.http_method_not_allowed
    return handler(request, *args, **kwargs)




def http_method_not_allowed(self, request, *args, **kwargs):
    logger.warning(
        "Method Not Allowed (%s): %s",
        request.method,
        request.path,
        extra={"status_code": 405, "request": request},
    )
    response = HttpResponseNotAllowed(self._allowed_methods())
    if self.veiw_is_async:
        async def func():
            return response
        return func()
    else:
        return response



