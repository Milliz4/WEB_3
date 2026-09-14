from django.http import HttpResponse
from customers.models import Customer


def show_customers(request):
    customers = Customer.objects.all()

    result = ""
    for c in customers:
        result += c.name + "<br>"

    return HttpResponse(result)