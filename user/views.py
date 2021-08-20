from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import generic, View

from shepherd_web.tokens import account_activation_token

from farm.models import Farm, FarmUsers
from task.models import TaskHistory
from user.forms import ProfileForm, SignUpForm
from user.models import ShepherdUser, UserValidations, UserCertifications


class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = ShepherdUser.objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError, ShepherdUser.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.user_validations.email_validated = True
            user.save()
            login(request, user)
            messages.success(request, ("Your account is now confirmed."))

            return redirect("main_page")
        else:
            messages.warning(request, ("The confirmation link was invalid."))
            return redirect("main_page")


class ProfileView(generic.UpdateView):
    model = ShepherdUser
    form_class = ProfileForm
    success_url = reverse_lazy("profile")
    template_name = "user/profile.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()

        certifications = UserCertifications.objects.filter(cert_user__id=request.user.id)
        roles = FarmUsers.objects.select_related("role", "farm").filter(user_id=request.user.id)
        tasks = TaskHistory.objects.select_related("task_status", "task_id", "task_id__task_plan__crop", "task_id__task_activity", "task_id__task_plan__location").filter(update_user__id=request.user.id).order_by("-status_date_change")[:5]
        validation = UserValidations.objects.get(user_id=request.user.id)

        return render(request, self.template_name, {"form": form, "validation": validation, "user": request.user, "roles": roles, "certifications": certifications, "tasks": tasks})


class SignupView(generic.CreateView):
    form_class = SignUpForm
    template_name = "registration/register.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            token = account_activation_token.make_token(user)
            user.user_validations.activation_key = token
            user.save()

            current_site = get_current_site(request)
            subject = "Activate your Shepherd Farming Account"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = user.email

            text_content = render_to_string(
                "email/confirm-registration-email.txt",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": token,
                },
            )

            html_content = render_to_string(
                "email/confirm-registration-email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": token,
                },
            )

            message = EmailMultiAlternatives(
                subject, text_content, from_email, [to_email]
            )
            message.attach_alternative(html_content, "text/html")
            message.send()

            return redirect(
                "email-confirm", urlsafe_base64_encode(force_bytes(user.pk))
            )

        return render(request, self.template_name, {"form": form})


class ConfirmEmailView(View):
    template_name = "registration/confirm-mail.html"

    def get(self, request, uidb64, *args, **kwargs):

        uid = force_text(urlsafe_base64_decode(uidb64))
        user = ShepherdUser.objects.get(pk=uid)

        return render(request, self.template_name, {"email": user.email})


def worker_list(request):
    farms = Farm.objects.filter(member_farms__user=request.user)

    workers = FarmUsers.objects.select_related("user", "farm", "role").filter(
        farm_id__in=farms
    )

    return render(request, "user/workers.html", {"workers": workers})
