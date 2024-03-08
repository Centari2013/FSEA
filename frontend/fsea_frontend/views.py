from django.http import HttpResponse
from django.template import loader


def login(request):
    template = loader.get_template("login.html")
    return HttpResponse(template.render())

def dashboard(request):
    template = loader.get_template("dashboard.html")
    return HttpResponse(template.render())