# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from .forms import LostFoundItemForm
# from .models import LostFoundItem
# from django.views.decorators.cache import cache_control
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# from django.conf import settings
# import openai
# import json
# import requests
# from django.utils import timezone  # Import timezone
# from django.utils.timezone import localtime  # Import localtime


# def root_redirect(request):
#     if request.user.is_authenticated:
#         return redirect('home')
#     else:
#         return redirect('login')


# # 🔐 Home view - requires login
# @login_required(login_url='login') 
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def home(request):
#     current_time = timezone.localtime()  # Get the current time in the configured timezone
#     return render(request, 'lostfound/home.html', {'current_time': current_time})


# # 📝 Signup view - blocks logged-in users & auto-logins new users
# def signup(request):
#     if request.user.is_authenticated:
#         return redirect('home')

#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']

#         if User.objects.filter(username=username).exists():
#             messages.error(request, 'Username already exists.')
#             return redirect('signup')

#         user = User.objects.create_user(username=username, email=email, password=password)
#         login(request, user)
#         messages.success(request, 'Account created successfully!')
#         return redirect('home')

#     return render(request, 'lostfound/signup.html')


# # 🔐 Login view - blocks logged-in users from seeing login page again
# def login_view(request):
#     if request.user.is_authenticated:
#         return redirect('home')

#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)

#         if user:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, 'Invalid username or password.')

#     return render(request, 'lostfound/login.html')


# # 🚪 Logout
# @login_required(login_url='login') 
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def logout_view(request):
#     logout(request)
#     return redirect('login')


# # ➕ Add lost/found item
# @login_required(login_url='login') 
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def add_item(request):
#     if request.method == 'POST':
#         form = LostFoundItemForm(request.POST, request.FILES)
#         if form.is_valid():
#             item = form.save(commit=False)
#             item.reported_by = request.user
#             # Removed setting time_reported
#             item.save()
#             messages.success(request, 'Item reported successfully.')
#             return redirect('item_list')
#     else:
#         form = LostFoundItemForm()
#     return render(request, 'lostfound/add_item.html', {'form': form})


# # 📋 View all items
# @login_required(login_url='login') 
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def item_list(request):
#     items = LostFoundItem.objects.all().order_by('-date_reported')
#     return render(request, 'lostfound/item_list.html', {'items': items})


# # 🥡 View lost items only
# @login_required(login_url='login') 
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def lost_items(request):
#     items = LostFoundItem.objects.filter(status='lost').order_by('-date_reported')
#     return render(request, 'lostfound/lost_items.html', {'items': items})


# # 💒 View found items only
# @login_required(login_url='login') 
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def found_items(request):
#     items = LostFoundItem.objects.filter(status='found').order_by('-date_reported')
#     return render(request, 'lostfound/found_items.html', {'items': items})


# # 🤖 AI Chatbot Assistant Endpoint
# @csrf_exempt
# def chatbot_view(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user_message = data.get('message')

#         api_key = settings.GEMINI_API_KEY  # Make sure this is defined in your settings.py
#         url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"

#         headers = {
#             "Content-Type": "application/json"
#         }

#         payload = {
#             "contents": [
#                 {
#                     "parts": [
#                         {"text": f"You are a helpful assistant for a Lost and Found website. Help users report, track, or find items.\nUser: {user_message}"}
#                     ]
#                 }
#             ]
#         }

#         try:
#             response = requests.post(url, headers=headers, json=payload)
#             response.raise_for_status()
#             gemini_reply = response.json()

#             # Extract response text
#             reply_text = gemini_reply['candidates'][0]['content']['parts'][0]['text']
#             return JsonResponse({'reply': reply_text})
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'error': 'Invalid request'}, status=400)
# # 🤖 Chatbot page renderer
# @login_required(login_url='login')
# def chatbot_page(request):
#     return render(request, 'lostfound/chatbot.html')


# @login_required
# def item_list(request):
#     query = request.GET.get('q')
#     if query:
#         items = LostFoundItem.objects.filter(name__icontains=query)
#     else:
#         items = LostFoundItem.objects.all().order_by('-date_reported')
#     return render(request, 'lostfound/item_list.html', {'items': items, 'query': query})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from .forms import LostFoundItemForm
from .models import LostFoundItem
import json
import requests
from django.conf import settings

# Root redirect
def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return redirect('login')


# 🔐 Home view
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    current_time = timezone.localtime()
    return render(request, 'lostfound/home.html', {'current_time': current_time})


# Signup
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not username or not email or not password1 or not password2:
            messages.error(request, "All fields are required.")
            return redirect('signup')
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect('home')
    return render(request, 'lostfound/signup.html')


# Login
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'lostfound/login.html')


# Logout
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_view(request):
    logout(request)
    return redirect('login')


# Add item
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_item(request):
    if request.method == 'POST':
        form = LostFoundItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.reported_by = request.user
            item.save()
            messages.success(request, 'Item reported successfully.')
            return redirect('item_list')
    else:
        form = LostFoundItemForm()
    return render(request, 'lostfound/add_item.html', {'form': form})


# View items
@login_required(login_url='login')
def item_list(request):
    query = request.GET.get('q')
    if query:
        items = LostFoundItem.objects.filter(title__icontains=query)
    else:
        items = LostFoundItem.objects.all().order_by('-date_reported')
    return render(request, 'lostfound/item_list.html', {'items': items, 'query': query})


# Lost items
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def lost_items(request):
    items = LostFoundItem.objects.filter(status='lost').order_by('-date_reported')
    return render(request, 'lostfound/lost_items.html', {'items': items})


# Found items
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def found_items(request):
    items = LostFoundItem.objects.filter(status='found').order_by('-date_reported')
    return render(request, 'lostfound/found_items.html', {'items': items})


# Claim an item
@login_required(login_url='login')
def claim_item(request, item_id):
    item = get_object_or_404(LostFoundItem, id=item_id)

    if item.claimed_by == request.user:
        messages.info(request, f'You have already claimed "{item.title}".')
    elif item.claimed_by is not None:
        messages.warning(request, f'This item has already been claimed by someone else.')
    else:
        item.claimed_by = request.user
        item.save()
        messages.success(request, f'You have claimed the item: {item.title}')

    return redirect('item_list')


# Chatbot endpoint
@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')
        api_key = settings.GEMINI_API_KEY
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [
                {"parts": [{"text": f"You are a helpful assistant for a Lost and Found website. Help users report, track, or find items.\nUser: {user_message}"}]}
            ]
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            gemini_reply = response.json()
            reply_text = gemini_reply['candidates'][0]['content']['parts'][0]['text']
            return JsonResponse({'reply': reply_text})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)


# Chatbot page
@login_required(login_url='login')
def chatbot_page(request):
    return render(request, 'lostfound/chatbot.html')
