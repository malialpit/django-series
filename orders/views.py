from io import BytesIO

import razorpay
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views import View, generic
from razorpay.errors import SignatureVerificationError
from xhtml2pdf import pisa

from ecommerce import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import Cart, Order, OrderItem, Coupon, Payment, Transaction
from .forms import CheckoutForm, CouponForm, OrderStatusForm

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_ID, settings.RAZORPAY_ACCOUNT_ID))


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
            return JsonResponse({"valid": False, "error": "Invalid coupon"})

        order, _ = Order.objects.get_or_create(user=request.user, ordered=False)
        order.coupon = coupon
        order.save()

        subtotal = cart_subtotal(cart_items)
        discount = order.get_discount
        total = subtotal - discount

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
    amount = int(order.get_total * 100)  # amount in paise
    callback_url = request.build_absolute_uri("/order/callback/")
    notes = {"order-type": "basic order from the website", "key": "value"}

    razorpay_order = razorpay_client.order.create(
        dict(
            amount=amount,
            currency=order_currency,
            notes=notes,
            receipt=str(order.order_id),
            payment_capture="0"
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
        client = razorpay.Client(auth=(settings.RAZORPAY_ID, settings.RAZORPAY_ACCOUNT_ID))

        params_dict = {
            "razorpay_order_id": request.POST.get("razorpay_order_id"),
            "razorpay_payment_id": request.POST.get("razorpay_payment_id"),
            "razorpay_signature": request.POST.get("razorpay_signature"),
        }

        try:
            client.utility.verify_payment_signature(params_dict)

            transaction = Transaction.objects.get(razorpay_order_id=params_dict["razorpay_order_id"])
            if transaction.payment_status != '3':
                return render(request, "orders/payment-failed.html")
            payment = Payment.objects.get(payment_id=transaction.payment.payment_id)
            order = Order.objects.get(order_id=payment.order.order_id)
            items = OrderItem.objects.filter(order=order.order_id)
            transaction.razorpay_payment_id = params_dict["razorpay_payment_id"]
            transaction.razorpay_signature = params_dict["razorpay_signature"]
            transaction.razorpay_payment_id = params_dict["razorpay_payment_id"]
            transaction.payment_status = 1
            transaction.datetime_of_payment = timezone.now()
            transaction.payment.order.order_status = "DELIVERED"
            transaction.save()
            pdf_bytes, filename = generate_invoice_pdf(order, items, transaction)
            mail_subject = 'Recent Order Details'
            context_dict = {
                'user': order.user,
                'order_id': str(order),
                'order': items,
            }
            template = get_template('orders/emailinvoice.html')
            message = template.render(context_dict)
            to_email = order.user.email
            email = EmailMultiAlternatives(
                mail_subject,
                "hello",
                settings.EMAIL_HOST_USER,
                [to_email]
            )
            email.attach_alternative(message, "text/html")
            email.attach(filename, pdf_bytes, 'application/pdf')
            email.send(fail_silently=False)
            return render(request, "orders/payment-success.html", {"order": transaction.payment.order})

        except SignatureVerificationError:
            return render(request, "orders/payment-failed.html")

    return None


def generate_invoice_pdf(order, items, transaction=None):
    """
    Generate invoice PDF and return (pdf_bytes, filename)
    """
    context = {
        'first_name': order.user.first_name,
        'last_name': order.user.last_name,
        'order_id': str(order),
        'transaction_id': transaction.razorpay_payment_id if transaction else None,
        'user_email': order.user.email,
        'phone_number': getattr(order.billing_address, "phone_number", ""),
        'date': order.ordered_date,
        'items': items,
        'billing_address': getattr(order.billing_address, "street_address", ""),
        'city': getattr(order.billing_address, "city", ""),
        'state': getattr(order.billing_address, "state", ""),
        'country': getattr(order.billing_address, "country", ""),
        's_billing_address': getattr(order.billing_address, "s_street_address", ""),
        's_city': getattr(order.billing_address, "s_city", ""),
        's_state': getattr(order.billing_address, "s_state", ""),
        's_country': getattr(order.billing_address, "s_country", ""),
        'sub_total': order.get_subtotal,
        'discount': order.get_discount,
        'total': order.get_total,
    }

    template = get_template('orders/invoice.html')
    html = template.render(context)
    result = BytesIO()
    pisa_status = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)

    if pisa_status.err:
        return None, None

    pdf_bytes = result.getvalue()
    filename = f"Invoice_{order}.pdf"
    return pdf_bytes, filename


class GenerateInvoice(View):
    def get(self, request, order_id, *args, **kwargs):
        order = Order.objects.get(order_id=order_id, user=request.user, ordered=True)
        items = OrderItem.objects.filter(order=order_id)
        payment = Payment.objects.get(order_id=order_id)
        transaction = Transaction.objects.get(payment=payment.payment_id, payment_status=1)
        pdf_bytes, filename = generate_invoice_pdf(order, items, transaction)
        if pdf_bytes:
            response = HttpResponse(pdf_bytes, content_type='application/pdf')
            response['Content-Disposition'] = f"attachment; filename={filename}"
            return response
        return HttpResponse("Not found")


@login_required()
def manage_orders(request):
    order_no = request.GET.get('order_no', '')
    payment_id = request.GET.get('payment_id', '')
    status = request.GET.get('status', 'ALL')

    orders = Order.objects.all()

    # Search filters
    if order_no:
        orders = orders.filter(order_id__icontains=order_no)
    if payment_id:
        transactions = Transaction.objects.filter(
            razorpay_payment_id__icontains=payment_id
        )
        order_ids = transactions.values_list("payment__order__order_id", flat=True)
        orders = orders.filter(order_id__in=order_ids)

    # Status filter
    if status != 'ALL':
        if status in ['DELIVERED', 'RECEIVED', 'REFUND', 'GRANTED', 'UPDATE']:
            orders = orders.filter(order_status=status)
        elif status == 'PAYMENT_SUCCESS':
            orders = orders.filter(payment__transaction__payment_status='1')
        elif status == 'PAYMENT_FAILED':
            orders = orders.filter(payment__transaction__payment_status='2')

    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    order_ids = page_obj.object_list.values_list('order_id', flat=True)
    transactions = Transaction.objects.filter(payment__order__order_id__in=order_ids)
    transactions_dict = {}
    for transaction in transactions:
        transactions_dict.setdefault(transaction.payment.order.order_id, []).append(transaction)

    context = {
        'order': order_ids,
        'transaction': transactions_dict,
        'page_obj': page_obj,
        'order_no': order_no,
        'payment_id': payment_id,
        'status': status,
    }
    return render(request, 'orders/manage-orders.html', context)


class UpdateOrderStatus(LoginRequiredMixin, generic.UpdateView):
    model = Order
    template_name = "orders/order-status.html"
    form_class = OrderStatusForm
    login_url = '/login/'
    success_url = reverse_lazy('orders:manage_orders')

@login_required()
def orders(request):
    orders = Order.objects.filter(user=request.user)
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    order_ids = page_obj.object_list.values_list('order_id', flat=True)
    transactions = Transaction.objects.filter(payment__order__order_id__in=order_ids)
    transactions_dict = {}
    for transaction in transactions:
        transactions_dict.setdefault(transaction.payment.order.order_id, []).append(transaction)

    context = {
        'order': order_ids,
        'transaction': transactions_dict,
        'page_obj': page_obj,
    }
    return render(request, 'orders/orders.html', context)
