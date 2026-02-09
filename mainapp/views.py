from django.shortcuts import render

def home(request):
    return render(request, 'mainapp/home.html')

from django.shortcuts import render
from .ai_api import generate_image
from django.http import HttpResponseRedirect
from urllib.parse import urlencode

from django.contrib.auth.decorators import login_required

from .models import PromptHistory

def image_generate(request):
    image_url = None
    error_message = None

    if request.method == "POST":
        if not request.user.is_authenticated:
            error_message = "Please login to generate the image."
        else:
            prompt = request.POST.get("prompt", "").strip()
            image_url = generate_image(request)

            if image_url and prompt:
                PromptHistory.objects.create(
                    user=request.user,
                    prompt=prompt,
                    image_url=image_url
                )

    return render(
        request,
        "mainapp/image.html",
        {
            "image_url": image_url,
            "error_message": error_message
        }
    )

# Add this for downloads
def serve_generated_image(request):
    return generate_image(request)


import requests
from urllib.parse import quote
from django.shortcuts import render

def article_generate(request):
    article = ""
    topic = ""

    if request.method == "POST":
        topic = request.POST.get("topic", "").strip().lower()

        if topic:
            # Handle input like: "about ai"
            if topic.startswith("about"):
                clean_topic = topic.replace("about", "").strip()
            else:
                clean_topic = topic

            # Internal AI prompt
            ai_prompt = f"Explain {clean_topic} in simple words."
            encoded_prompt = quote(ai_prompt)

            url = f"https://text.pollinations.ai/{encoded_prompt}"

            try:
                response = requests.get(url, timeout=30)

                if response.status_code == 200:
                    # Remove markdown symbols like **
                    article = response.text.replace("**", "")
                else:
                    article = "Failed to generate article."

            except Exception:
                article = "Error while generating article."

    return render(
        request,
        "mainapp/article.html",
        {
            "article": article,
            "topic": topic
        }
    )

from django.shortcuts import render, redirect

def signin(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        user = authenticate(request, username=phone, password=password)

        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid phone number or password")

    return render(request, "mainapp/signin.html")


def about(request):
    return render(request,"mainapp/about.html")

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Profile

def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        if Profile.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already registered")
            return render(request, "mainapp/register.html")

        user = User.objects.create_user(
            username=phone,
            password=password
        )

        Profile.objects.create(
            user=user,
            name=name,
            phone=phone
        )

        messages.success(request, "Account created successfully")
        return redirect("signin")

    return render(request, "mainapp/register.html")

def forgot_password(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        new_password = request.POST.get("password")

        try:
            profile = Profile.objects.get(phone=phone)
            user = profile.user
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password updated successfully")
            return redirect("signin")

        except Profile.DoesNotExist:
            messages.error(request, "Your number is wrong / not registered")

    return render(request, "mainapp/forgot_password.html")

from django.contrib.auth import logout
from django.shortcuts import redirect

def user_logout(request):
    logout(request)
    return redirect("home")


from django.contrib.auth.decorators import login_required
from .models import PromptHistory

@login_required
def user_history(request):
    search = request.GET.get("search", "")

    history = PromptHistory.objects.filter(user=request.user)

    if search:
        history = history.filter(prompt__icontains=search)

    history = history.order_by("-created_at")

    return render(
        request,
        "mainapp/history.html",
        {
            "history": history,
            "search": search
        }
    )

