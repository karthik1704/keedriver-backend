import json

from django import template
from django.contrib.admin.templatetags.base import InclusionAdminNode
from django.template.context import Context

register = template.Library()


@register.tag(name="change_form_object_tools1")
def change_form_object_tools_tag1(parser, token):
    """Display the row of change form object tools."""
    return InclusionAdminNode(
        parser,
        token,
        func=lambda context: context,
        template_name="change_form_object_tools1.html",
    )
