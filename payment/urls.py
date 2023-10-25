from django.urls import path
from django.utils.translation import gettext_lazy as _

from payment import views, webhooks

urlpatterns = [
    path(_('process/'), views.payment_process),
    path(_('completed/'), views.payment_completed),
    path(_('canceled/'), views.payment_canceled),
]