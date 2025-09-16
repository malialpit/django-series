from django import template

from orders.models import Cart
from products.models import Slider

register = template.Library()


@register.simple_tag
def get_sliders():
    sliders = Slider.objects.all()
    return sliders


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Cart.objects.filter(user=user)
        if qs.exists():
            return qs.count()
    return 0


@register.filter
def get_item(value, arg):
    """Retrieve dictionary value using the key"""
    return value.get(arg)