from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .forms import EmailCampaignForm


def campaign(request):
    return render(request, "campaign/campaign.html")


def new_campaign(request):
    if request.method == "POST":
        form = EmailCampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            recipients = campaign.get_recipient_list()

            send_mail(
                subject=campaign.subject,
                message=campaign.message,
                from_email="jibon.belasea@gmail.com",  # Uses DEFAULT_FROM_EMAIL
                recipient_list=recipients,
                fail_silently=False,
            )

            campaign.save()  # Save to DB
            messages.success(request, "✅ Campaign email sent!")
            return redirect("new-campaign")
    else:
        form = EmailCampaignForm()
    context = {
        "form": form
    }
    return render(request, "campaign/new_campaign.html", context)
