from datetime import datetime
from statistic.models import Visit
from statistic.utils import views_in_month
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives


def monthly_report():
    cur_year = datetime.now().year
    cur_month = datetime.now().month
    visitors = Visit.objects.filter(date__year=cur_year, date__month=cur_month)
    _, views, total_views = views_in_month(cur_year, cur_month)

    # send html email
    plaintext = get_template('email.txt')
    html = get_template('email.html')
    admins = User.objects.filter(
        is_staff=True, is_active=True, is_superuser=True, )

    context = {
        "year": cur_year,
        "month": cur_month,
        "visitors_info": visitors,
        "views": views,
        "total_views": total_views,
    }
    subject = "Movie-Quote Monthly Report"
    for admin in admins:
        context["username"] = admin.username
        text_context = plaintext.render(context)
        html_context = html.render(context)
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_context,
            from_email="pythontestsendingemail@gmail.com", to=[admin.email]
        )

        msg.attach_alternative(html_context, "text/html")
        try:
            msg.send(fail_silently=False)
        except Exception:
            raise Exception("not able to send Email. its probably\
            smtp security blocking this action")

    log = "[{}] Report sent".format(
        datetime.now().strftime("%Y-%m-%d-%H:%M:%S.%f"))

    print(log)
