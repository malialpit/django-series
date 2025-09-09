import razorpay
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from razorpay.errors import SignatureVerificationError

from ecommerce import settings
from orders.forms import CheckoutForm, CouponForm
from orders.models import Cart, Order, Coupon, OrderItem, Payment, Transaction

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_ID, settings.RAZORPAY_ACCOUNT_ID))


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
            return redirect("orders:payment")

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


@login_required
def payment(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_items.delete()
    order = Order.objects.filter(user=request.user, ordered=True).last()
    if not order:
        messages.warning(request, "No active order found")
        return redirect("orders:checkout")

    payment_instance, created = Payment.objects.get_or_create(
        order=order,
        merchant_id=settings.RAZORPAY_ID,
        defaults={
            "merchant_transaction_id": f"TXN{order.order_id}{timezone.now().timestamp()}"
        }
    )

    order_currency = "INR"
    amount = int(order.get_total * 100)
    callback_url = request.build_absolute_uri("/order/callback/")
    notes = {"order-type": "basci order form the website", "key": "value"}

    razorpay_order = razorpay_client.order.create(
        dict(
            amount=amount,
            currency=order_currency,
            notes=notes,
            payment_capture="0",
        )
    )

    transaction = Transaction.objects.create(
        payment=payment_instance,
        razorpay_order_id=razorpay_order["id"],
        payment_status=3,
    )

    context = {
        "order": order,
        "payment": payment_instance,
        "transaction": transaction,
        "order_id": razorpay_order["id"],
        "orderId": order.order_id,
        "razorpay_merchant_id": settings.RAZORPAY_ID,
        "callback_url": callback_url,
        "amount": amount,
    }
    return render(request, "orders/payment.html", {"context": context})


@csrf_exempt
def callback(request):
    if request.method == "POST":
        params_dict = {
            "razorpay_order_id": request.POST.get("razorpay_order_id"),
            "razorpay_payment_id": request.POST.get("razorpay_payment_id"),
            "razorpay_signature": request.POST.get("razorpay_signature")
        }

        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
            transaction = Transaction.objects.get(razorpay_order_id=params_dict["razorpay_order_id"])
            if transaction.payment_status != '3':
                return render(request, "orders/payment-failed.html")
            payment = Payment.objects.get(payment_id=transaction.payment.payment_id)
            order = Order.objects.get(order_id=payment.order.order_id)
            transaction.razorpay_payment_id = params_dict["razorpay_payment_id"]
            transaction.razorpay_signature = params_dict["razorpay_signature"]
            transaction.razorpay_order_id = params_dict["razorpay_order_id"]
            transaction.payment_status = 1
            transaction.datetime_of_payment = timezone.now()
            transaction.payment.order.order_status = "RECEIVED"
            transaction.save()
            return render(request, "orders/payment-success.html", {"order": transaction.payment.order})

        except SignatureVerificationError:
            return render(request, "orders/payment-failed.html")

    return None
