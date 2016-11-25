from functools import wraps
from htmlmin.minify import html_minify


def minified_response(function):
  @wraps(function)
  def minified_view(*args, **kwargs):
    return_value = function(*args, **kwargs)
    if type(return_value) == str:
      return html_minify(return_value.encode('utf-8'))
    return return_value

  return minified_view
