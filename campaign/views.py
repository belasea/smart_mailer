from django.shortcuts import render, redirect
from django.contrib import messages
from .models import EmailCampaign
from .forms import EmailCampaignForm
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


def campaign(request):
    queryset = EmailCampaign.objects.all().order_by('-created_at')
    query = request.GET.get('q')
    page = request.GET.get('page')
    if query:
        query = query.strip()
        queryset = queryset.filter(
            Q(subject__icontains=query) |
            Q(message__contains=query)
        ).distinct()
    paginator = Paginator(queryset, 8)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    context = {
        'object_list': queryset,
        'page': page,
        'query': query,
        'email': "jibon.belasea@gmail.com"
    }

    return render(request, "campaign/campaign.html", context)


def new_campaign(request):
    if request.method == "POST":
        form = EmailCampaignForm(request.POST)
        if form.is_valid():
            # Get the cleaned data
            cleaned_data = form.cleaned_data
            recipients_raw = cleaned_data.get("recipients", "")
            recipients = [email.strip() for email in recipients_raw.split(",") if email.strip()]

            # Prepare email content
            subject = cleaned_data.get("subject")
            html_content = cleaned_data.get("message")
            text_content = strip_tags(html_content)

            # Send email
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email="jibon.belasea@gmail.com",
                to=recipients,
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            # Save campaign to DB (excluding recipients)
            campaign = EmailCampaign(
                subject=subject,
                message=html_content,
                recipients="",  # Optional: You can skip saving or save as empty
            )
            campaign.save()

            messages.success(request, "✅ Campaign email sent!")
            return redirect("new-campaign")
    else:
        form = EmailCampaignForm()

    context = {
        "form": form
    }
    return render(request, "campaign/new_campaign.html", context)



"""
def new_campaign(request):
    if request.method == "POST":
        form = EmailCampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            recipients = campaign.get_recipient_list()

            # HTML and plain text content
            html_content = campaign.message
            text_content = strip_tags(html_content)

            # Compose the email
            email = EmailMultiAlternatives(
                subject=campaign.subject,
                body=text_content,
                from_email="jibon.belasea@gmail.com", # Uses DEFAULT_FROM_EMAIL
                to=recipients,
                fail_silently=False,
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            # Save campaign to DB
            campaign.save()

            messages.success(request, "✅ Campaign email sent!")
            return redirect("new-campaign")
    else:
        form = EmailCampaignForm()

    context = {
        "form": form
    }
    return render(request, "campaign/new_campaign.html", context)
"""


