import json


import djstripe.models
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import generic, View
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site

import stripe

from djstripe.models import Customer, Product, Price
from user.models import ShepherdUser

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.DJSTRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        customer_email = session["customer_details"]['email']
        product_id = session['metadata']['product_id']

        product = Product.objects.get(id=product_id)

        current_site = get_current_site(request)
        subject = f"{product.name} Purchase Completed"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = request.user.email

        text_content = render_to_string(
            "email/purchase_complete.txt",
            {
                "user": request.user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(request.user.pk)),
                "product": product
            },
        )

        html_content = render_to_string(
            "email/purchase_complete.html",
            {
                "user": request.user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(request.user.pk)),
                "product": product,
            },
        )

        message = EmailMultiAlternatives(
            subject, text_content, from_email, [to_email]
        )
        message.attach_alternative(html_content, "text/html")
        message.send()

    return HttpResponse(status=200)


class CreateCheckoutSessionView(View):

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs["product"]
        product = Product.objects.get(id=product_id)
        price = Price.objects.get(product_id=product_id)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': price.unit_amount,
                        'product_data': {
                            'name': product.name,
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id": product.id
            },
            mode='payment',
            success_url= settings.PRIMARY_DOMAIN + '/subscription/success/',
            cancel_url=settings.PRIMARY_DOMAIN + '/subscription/cancel/',
        )

        return JsonResponse({
            'id': checkout_session.id
        })


class SuccessView(generic.TemplateView):
    template_name = "subscription/success.html"


class CancelView(generic.TemplateView):
    template_name = "subscription/cancel.html"


class CheckoutView(generic.TemplateView):
    template_name = 'subscription/checkout.html'

    def get_context_data(self, **kwargs):
        product = kwargs.get('product')
        customer = Customer.objects.get(subscriber=self.request.user)
        product = Product.objects.get(id=product)

        context = super(CheckoutView, self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "customer": customer,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })

        return context


def stripe_config(request):
    if request.method == "GET":
        stripe_config = {'publicKey': settings.STRIPE_PUBLIC_KEY}

        return JsonResponse(stripe_config, safe=False)


class PricingView(generic.TemplateView):
    template_name = "subscription/pricing.html"

    def get_context_data(self, **kwargs):
        products = Product.objects.all()
        context = super(PricingView, self).get_context_data(**kwargs)
        context.update({
            "products": products,
            "customer": self.request.user,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context

