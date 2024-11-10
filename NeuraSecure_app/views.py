from django.shortcuts import render
from django.http import JsonResponse
import re
from django.utils.html import strip_tags
from django.template.loader import render_to_string,get_template,select_template
from django.core.mail import EmailMultiAlternatives
from django.db.models import F
from django.utils import timezone
from datetime import datetime
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from .models import *
# from .models import Comment
# from .models import Category
# from .models import UserLike
from django.contrib.auth.models import User
import json
import google.generativeai as genai
import os
from asgiref.sync import sync_to_async
# from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()


api_key = os.getenv("API_KEY")


def query_gemini(prompt):
    """
    Queries the Gemini API with a given prompt to generate a response.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")  # Use the appropriate model version
    
    try:
        # Generate the response from the model
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        error_msg = f"Error occurred: {str(e)}"
        print(e)
        return error_msg


# Check if the key is loaded correctly
if not api_key:
    print("Error: API_KEY not found.")
else:
    # Configure the Gemini API with your API key
    genai.configure(api_key=api_key)


def register(request):
    if request.method=="POST":
        data =json.loads(request.body)
        username = data.get('username')
        if not bool(re.match(r"^[A-Za-z][A-Za-z0-9_]{1,29}$",username)):
            return JsonResponse({'error':'Enter a valid username , Username should contain alphabets and numbers,it should not contain spaces and special characters except underscores'},status =400)
        first_name = data.get('first_name')
        if not bool(re.match(r"^[A-Za-z]{1}[A-Z a-z]{1,15}$",first_name)):
            return JsonResponse({'error':'Enter a valid name, it should not contain numbers'},status =400)
        last_name = data.get('last_name')
        if not bool(re.match(r"^[A-Za-z]{1}[A-Z a-z]{1,10}$",last_name)):
            return JsonResponse({'error':'Enter a valid name, it should not contain numbers'},status =400)
        email = data.get('email')
        if not bool(re.match(r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$",email)):
            return JsonResponse({'error':'Please enter a valid email address'},status = 400)
        password = data.get('password')
        cpassword = data.get('cpassword')
        if not bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",password)):
            return JsonResponse({'error':'password must  contain atleast a special character,a uppercase letter, a lowercase letter,a number and minimum should be of 8 character'},status =400)
        if password != cpassword:
            return JsonResponse({'error':'Password and confirm password do not match'},status = 400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'User already exists!!'},status=400)
        User.objects.create_user(username=username, password=password,first_name = first_name,last_name=last_name,email=email)
        return JsonResponse({'message': 'User created'}, status=201)
    else:
        return JsonResponse({'error':'Invalid Method'},status= 405)
    
def login_user(request):
    if request.method=="POST":
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if username is None:
            return JsonResponse({'error':'Please enter username'},status=400)
        if password is None:
            return JsonResponse({'error':'Please enter password'},status=400)
        user = authenticate(request , username=username, password=password)
        if user is not None:
            login(request, user)
            username = request.user
            
            return JsonResponse({'message':'User successfully logged in!'}, status=200)
        return JsonResponse({'error': 'Invalid credentials'}, status=401)




def login_det(request):
    if request.method =="GET":
        if not request.user.is_authenticated:
            return JsonResponse({'error':'No user is logged in'},status =400)
        user =request.user
        print(user)
        details = User.objects.filter(username = user).values()
        name = details[0]['username']
        return JsonResponse({'user':name},status =200)        
    else:
        return JsonResponse({'error':'Invalid method'},status =405)

    
def logout_user(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({'message':'Logged out!!'},status = 200)
    else:
        return JsonResponse({'error':'Invalid method'},status =405 )
        

def data_insert(request):
    if request.method=="POST":
        data = json.loads(request.body)
        title = data.get('title')
        print(data)
        return JsonResponse({'message':'Data inserted successfully'},status=201)
    return JsonResponse({'error':'Invalid Method'},status =405)
    
    
def list_data(request):
    if request.method == "GET":
        det = Data.objects.all().values('id','title','info','category__name','link','date','content',likes=F('num_likes'))
        return JsonResponse({'list':list(det)},status =200)
    
    else:
        return JsonResponse({'error':'Invalid method'},status =405)
                    
    
def list_cat_data(request):
    if request.method=="GET":
        cat_id = request.GET.get('category_id')
        data = Data.objects.filter(category_id=cat_id).values('title','info','category__name','link','date')
        return JsonResponse(list(data),safe=False)
    else:
        return JsonResponse({"error":"Invalid method"},status =405)


def like_dislike(request):
    if request.method == "PUT":
        if request.user.is_authenticated:
            data = json.loads(request.body)
            post_id = data.get('id')
            # comment_content = data.get('comment')
            if not Data.objects.filter(id=post_id).exists():
                return JsonResponse({'error':'post doesn\'t exists'},status=404)
            like_post, created = UserLike.objects.get_or_create(user=request.user, post_id=post_id, defaults={'is_like':1})
            if not created:
                like_post.is_like = F('is_like')*-1
                like_post.save()
                return JsonResponse({'status':'updated post'})
            return JsonResponse({'status':'like status saved succesfully'})
        return JsonResponse({'error': 'User not authenticated','route':'/login'}, status=401)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
def top_categories(request):
    if request.method == "GET":
        categories = Category.objects.annotate(post_count=Count('data')).order_by('-post_count')[:5]

        category_data = [
            {
                'category_id': category.id,
                'category_name': category.name,
                'post_count': category.post_count
            }
            for category in categories
        ]

        return JsonResponse({'top_categories': category_data}, status=200)

    return JsonResponse({'error': 'Invalid method'}, status=405)

def book_pkg(request):
    if request.method == 'GET':
        data = packages.objects.all().values()
        return JsonResponse({'packages':list(data)})
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            pkg_id = data.get('pkg_id')
            if pkg_id is None or not pkg_id:
                return JsonResponse({'status':'package ID is required'},status=422)
            cat_ids = data.get('cat_id')
            if pkg_id==1 and len(cat_ids)!=1:
                return JsonResponse({'status':'Invalid category ID'},status=422)
            scrp = subscriptions.objects.create(scr_user=request.user, scr_pkg_id=pkg_id)
            for category in cat_ids:
                subscribed_category = subscribed_cat.objects.create(subscription_id=scrp,subscribed_category_id=category)
            return JsonResponse({'status':'subscription added successfully'})
        return JsonResponse({'error': 'User not authenticated','route':'/login'}, status=401)
    return JsonResponse({'status':'Invalid method'}, status=405)
         
def test(request):
    if request.method == 'GET':
        subject = 'Weekly Update Regarding Cyber Security'
        from_email = 'shantanugupta13524@gmail.com'
        recipient_list_1 = list(subscribed_cat.objects.filter(subscribed_category_id=1).values('subscription_id__scr_user__email'))
        email_list_1 = [item['subscription_id__scr_user__email'] for item in recipient_list_1]
        unique_email_list_1 = list(set(email_list_1))
        
        recipient_list_2 = list(subscribed_cat.objects.filter(subscribed_category_id=2).values('subscription_id__scr_user__email'))
        email_list_2 = [item['subscription_id__scr_user__email'] for item in recipient_list_2]
        unique_email_list_2 = list(set(email_list_2))
        
        recipient_list_3 = list(subscribed_cat.objects.filter(subscribed_category_id=3).values('subscription_id__scr_user__email'))
        email_list_3 = [item['subscription_id__scr_user__email'] for item in recipient_list_3]
        unique_email_list_3 = list(set(email_list_3))
        
        recipient_list_4 = list(subscribed_cat.objects.filter(subscribed_category_id=4).values('subscription_id__scr_user__email'))
        email_list_4 = [item['subscription_id__scr_user__email'] for item in recipient_list_4]
        unique_email_list_4 = list(set(email_list_4))

        cat_1_news = Data.objects.filter(category_id=1).order_by('-date').values('title','info')[:5]
        cat_2_news = Data.objects.filter(category_id=2).order_by('-date').values('title','info')[:5]
        cat_3_news = Data.objects.filter(category_id=3).order_by('-date').values('title','info')[:5]
        cat_4_news = Data.objects.filter(category_id=4).order_by('-date').values('title','info')[:5]
        
        html_content1 = render_to_string('html_mail.html')
        
        
        
        # subject, from_email, to = "hello", "shantanugupta13524@gmail.com", "shantanugupta13524@gmail.com"
        # text_content = strip_tags(html_content)
        # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        # msg.attach_alternative(html_content, "text/html")
        # msg.send(fail_silently=True)
        # context = {'message': 'Hello, welcome to my simple Django page!'}
        print(unique_email_list)
        return JsonResponse({'status':'Test'})    

def test2(request):
        html_content = render_to_string('html_mail.html')
        subject, from_email, to = "hello", "shantanugupta13524@gmail.com", "dev241736@gmail.com"
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=True)
        return JsonResponse({'status':'Test'})    

        # context = {'message': 'Hello, welcome to my simple Django page!'}
    
async def chatbot(request):
    if request.method == 'POST':
        print(request.body)
        data = json.loads(request.body)
        query = data.get('message')
        if query is None or not query:
            return JsonResponse({'status': 'Invalid Query'}, status=422)
        
        answer = await sync_to_async(query_gemini)(query)
        print(answer)
        return JsonResponse({'Answer': answer})
        
    




