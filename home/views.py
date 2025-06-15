from django.shortcuts import render

def home(request):
    return render(request, "home/index.html")


def privacy_policy(request):
    return render(request, "home/privacy_policy.html")


def terms_and_condition(request):
    return render(request, "home/terms_condition.html")