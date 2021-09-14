from datetime import datetime

from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages

from .forms import FeedbackForm

from farm.models import Farm
from task.models import Task


def index(request):

    return render(request, "index.html")


def settings(request):

    return render(request, "settings.html")

def management_list(request):

    return render(request, "management_list.html")

def new_contact_task(request):

    return render(request, "new_contact_task.html")

def feedback(request):

    form = FeedbackForm(request.POST or None)

    if form.is_valid():
        current_site = get_current_site(request)

        user = request.user
        subject = f"User Feedback From {user.first_name} {user.last_name}"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = settings.DEFAULT_FEEDBACK_EMAIL

        text_content = render_to_string(
            "email/feedback-email.txt",
            {
                "user": user,
                "user_email": user.email,
                "domain": current_site.domain,
                "message": form.cleaned_data["message"],
            },
        )

        html_content = render_to_string(
            "email/feedback-email.html",
            {
                "user": user,
                "user_email": user.email,
                "domain": current_site.domain,
                "message": form.cleaned_data["message"],
            },
        )

        message = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        message.attach_alternative(html_content, "text/html")
        message.send()

        messages.add_message(request, messages.INFO, "Thank you for your feedback!")

        return redirect("main_page")

    else:
        return render(request, "feedback.html", {"form": form})
