import weasyprint

from io import BytesIO
from celery import shared_task

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from orders.models import Order


@shared_task
def payment_completed(order_id):
    """
     We need this to send an email
     if the payment is completed
    """
    order = Order.objects.get(id=order_id)
    #creating an incoice email
    subject = f'Pixel.by - Invoice no.{order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject,
                         message,
                         'admin@pixelby.com',
                         [order.email])
    #generating pdf file
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out,stylesheets=stylesheets)
    #attaching pdf file
    email.attach(f'order_{order_id}.pdf',
                 out.getvalue,
                 'application/pdf')
    #sending email
    email.send()
