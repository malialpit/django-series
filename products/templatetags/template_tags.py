from django import template

from products.models import Slider

register = template.Library()


@register.simple_tag
def get_sliders():
    sliders = Slider.objects.all()
    return sliders
