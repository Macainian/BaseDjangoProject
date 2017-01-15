import sys

from django.template import Context, Template
from django.conf import settings

if sys.version_info >= (3, 5):
    import html
    html_parser = html
elif sys.version_info >= (3, 0):
    import html.parser
    html_parser = html.parser.HTMLParser()
else:
    import HTMLParser
    html_parser = HTMLParser.HTMLParser()


def get_clean_ckeditor_html_code(unparsed_injected_html_code, context):
    injected_html_code = html_parser.unescape(unparsed_injected_html_code)

    # current_site = Site.objects.get_current()
    # context["SITE_URL"] = current_site.domain

    context["SITE_URL"] = settings.SITE_URL

    template = Template(template_string=injected_html_code)
    context_object = Context(context)
    final_html_code = template.render(context_object)

    return final_html_code
