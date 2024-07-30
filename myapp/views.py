from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import SignUpForm, AdForm, ResponseForm
from .models import Ad, Response, Category

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.email = form.cleaned_data.get('email')
            user.save()
            send_mail(
                'Registration Confirmation',
                'Welcome to our site!',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.save()
            return redirect('ad_detail', ad_id=ad.id)
    else:
        form = AdForm()
    return render(request, 'create_ad.html', {'form': form})

@login_required
def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    responses = Response.objects.filter(ad=ad)
    return render(request, 'ad_detail.html', {'ad': ad, 'responses': responses})

@login_required
def respond_to_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.ad = ad
            response.author = request.user
            response.save()
            send_mail(
                'New Response to Your Ad',
                f'You have a new response to your ad "{ad.title}".',
                settings.DEFAULT_FROM_EMAIL,
                [ad.author.email],
                fail_silently=False,
            )
            return redirect('ad_detail', ad_id=ad.id)
    else:
        form = ResponseForm()
    return render(request, 'respond_to_ad.html', {'form': form, 'ad': ad})

@login_required
def manage_responses(request):
    responses = Response.objects.filter(ad__author=request.user)
    return render(request, 'manage_responses.html', {'responses': responses})

@login_required
def accept_response(request, response_id):
    response = get_object_or_404(Response, id=response_id)
    response.is_accepted = True
    response.save()
    send_mail(
        'Your Response was Accepted',
        f'Your response to the ad "{response.ad.title}" was accepted.',
        settings.DEFAULT_FROM_EMAIL,
        [response.author.email],
        fail_silently=False,
    )
    return redirect('manage_responses')

@login_required
def delete_response(request, response_id):
    response = get_object_or_404(Response, id=response_id)
    response.delete()
    return redirect('manage_responses')
