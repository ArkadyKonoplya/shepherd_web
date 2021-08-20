from django.urls import path

from .views import PricingView, CheckoutView, stripe_config, CreateCheckoutSessionView, SuccessView, CancelView, stripe_webhook

urlpatterns = [
    path("pricing/", PricingView.as_view(), name="pricing"),
    path("create-checkout-session/<str:product>/", CreateCheckoutSessionView.as_view(), name="create-checkout-session"),
    path("config/", stripe_config, name="stripe_config"),
    path("success/", SuccessView.as_view(), name="success"),
    path("cancel/", CancelView.as_view(), name="cancel"),
    path("webhooks/stripe/", stripe_webhook, name='stripe-webhook'),
]
