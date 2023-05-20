# from django import forms
# from django.contrib.auth.forms import PasswordChangeForm


# class CustomPasswordChangeForm(PasswordChangeForm):
#     new_password_confirmation = forms.CharField(
#         label="New password confirmation",
#         strip=False,
#         widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
#     )

#     def clean_new_password_confirmation(self):
#         new_password = self.cleaned_data.get('new_password')
#         new_password_confirmation = self.cleaned_data.get('new_password_confirmation')
#         if new_password and new_password_confirmation and new_password != new_password_confirmation:
#             raise forms.ValidationError('Passwords do not match')
#         return new_password_confirmation

from django import forms
from django.contrib.auth.forms import PasswordResetForm


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
    )


from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
    )

    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        """
        Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        email = render_to_string(email_template_name, context)
        send_mail(
            subject, email, from_email, [to_email],
            html_message=html_email_template_name is not None,
        )