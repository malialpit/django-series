from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from reportlab.lib.pagesizes import elevenSeventeen

from orders.forms import CheckoutForm, CouponForm
from orders.models import Cart, Order, Coupon, OrderItem


# Create your views here.

def cart_subtotal(cart_qs):
    return sum(ci.get_final_price for ci in cart_qs)


@login_required
def checkout_view(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty")
        return redirect("products:cart_detail")

    order, created = Order.objects.get_or_create(
        user=request.user,
        ordered=False,
        defaults={"ordered_date": timezone.now()},
    )

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        coupon_form = CouponForm(request.POST)

        if request.POST and form.is_valid():
            billing_address = form.save(commit=False)
            billing_address.user = request.user
            billing_address.save()
            order.billing_address = billing_address

            order.order_items.all().delete()
            for ci in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=ci.product,
                    quantity=ci.quantity,
                )

            order.order_status = "RECEIVED"
            order.ordered_date = timezone.now()
            order.ordered = True
            order.save()
            messages.success(request, "Your order has been created. Proceed to payment.")
            return redirect("orders:checkout")

    else:
        form = CheckoutForm()
        coupon_form = CouponForm()

    if order.order_items.exists():
        line_items = order.order_items.all()
        subtotal = order.get_subtotal()
        discount = order.get_discount()
        total = order.get_total()
    else:
        line_items = cart_items
        subtotal = cart_subtotal(cart_items)
        discount = float(order.coupon.amount) if order.coupon else 0.0
        total = subtotal - discount

    return render(
        request,
        "orders/checkout.html",
        {
            "form": form,
            "couponform": coupon_form,
            "order": order,
            "order_items": line_items,
            "subtotal": subtotal,
            "discount": discount,
            "total": total,
        },
    )


def coupon(request):
    cart_items = Cart.objects.filter(user=request.user)
    if request.method == "POST":
        code = request.POST.get("code", "").strip()
        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            return JsonResponse({"valid": False, "error": "Invalid Coupon"})

        order, _ = Order.objects.get_or_create(user=request.user, ordered=False)
        order.coupon = coupon
        order.save()

        sub_total = cart_subtotal(cart_items)
        discount = order.get_discount
        total = sub_total - discount

        return JsonResponse({
            "valid": True,
            "discount": discount,
            "total": total,
        })
    return JsonResponse({"valid": False, "error": "Invalid request"})
