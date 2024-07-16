from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from . models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from . tokens import account_activation_token
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from . utils import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.template.loader import render_to_string
# Create your views here.
@login_required(login_url='login')
@cache_control(must_revalidate=True)
def home(request):
	return render(request,"index.html")



def login_view(request):
	if request.user.is_authenticated:
		return redirect('home')
	if request.method=="POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username = username,password = password)

		
		if user is not None:
			if not user.email_verified:
				messages.error(request,"Verify your email address")
				return redirect('login')
			
			login(request,user)
			messages.success(request,"Login Successfull")
			return redirect('home')
		else:
			messages.success(request,"Invalid username or password")
  
	return render(request,'login.html')

@cache_control(must_revalidate=True)
def signup_view(request):
	if request.user.is_authenticated:
		return redirect('home')
	
	if request.method=="POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		email = request.POST.get('email')
		
		confirmpassword = request.POST.get('confirmpassword')

		if User.objects.filter(username=username).exists() or User.objects.filter(email = email).exists():
			messages.error(request,"Username or email already exists")
			return redirect('signup')
		
		if password != confirmpassword:
			messages.error(request,"Password do not match")
			return redirect('signup')
		
		user = User(username = username,email=email)

		user.set_password(password)
		
		
		user.save()
		domain = get_current_site(request).domain
		
		send_mail(user,domain)
		

		messages.success(request,"Verfication email send to your email id")


		return redirect('login')


	return render(request,"signup.html")



login_required(login_url='home')
def logout_app(request):
	logout(request)
	messages.success(request,"User logout Successful")
	return redirect('login')

def activate(request,uid,token):
	try:
		uid = force_str(urlsafe_base64_decode(uid))
		user = User.objects.get(pk=uid)
	except (TypeError,ValueError,OverflowError,User.DoesNotExist):
		user = None

	if user is not None and account_activation_token.check_token(user,token):
		user.email_verified = True
		user.save()
		messages.success(request,"Email Verification Successfull")
		return redirect('login')
	
	else:
		messages.error(request,"Invalid verification url")
		return redirect('login')
	
@login_required(login_url='login')
@cache_control(must_revalidate=True)
def About(request):
	if not request.user.is_superuser:
		messages.error(request,"Not Authorized!")
		return redirect('home')
	return render(request,'about.html')

@login_required(login_url='login')
@cache_control(must_revalidate=True)
def Admin_page(request):
	if not request.user.is_superuser:
		messages.error(request,"Not Authorized!")
		return redirect('home')
	context = {
		'users':User.objects.all().order_by('email_verified','is_superuser')
	}
	return render(request,'adminPanel/admin.html',context)


def search(request):
	if not request.user.is_superuser:
		messages.error(request,"Not Authorized!")
		return redirect('home')
	users = User.objects.all().order_by('email_verified','is_superuser')
	if request.method=="GET":
		query = request.GET.get('query')
		users = User.objects.filter(username__icontains = query).order_by('email_verified','is_superuser')
	context = {
		'users':users
	}
	html_string = render_to_string('adminPanel/searchResult.html',context)
	return JsonResponse({'html':html_string})
	
@login_required(login_url='login')
@cache_control(must_revalidate=True)
def delete_user(request,id):
	if not request.user.is_superuser:
		messages.error(request,"Not Authorized!")
		return redirect('home')
	user = User.objects.get(id=id)
	user.delete()
	messages.success(request,"User deleted successfully")
	return redirect('admin_page')

@login_required(login_url='login')
@cache_control(must_revalidate=True)
def create_user(request):
	if not request.user.is_superuser:
		messages.error(request,"Not Authorized!")
		return redirect('home')
	if request.method == "POST":
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')
		verify = request.POST.get('verify')
		superuser = request.POST.get('superuser')

		if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
			messages.error(request,"Username or email exists already")
			return redirect('create_user')

		user = User(username=username,email=email)
		user.set_password(password)
		user.email_verified = True if verify else False
		user.is_superuser = True if superuser else False
		user.is_staff = True if superuser else False
		user.save()
		messages.success(request,"User created successfully")
		return redirect('admin_page')
	return render(request,'adminPanel/create-user.html')

def edit_user(request,id):
	if not request.user.is_superuser:
		messages.error(request,"Not Authorized!")
		return redirect('home')

	user = User.objects.get(id=id)
	if request.method=="POST":
		username = request.POST.get('username')
		email = request.POST.get('email')
		user.username = username
		user.email = email
		user.save()
		messages.success(request,"User saved successfully")
		return redirect('admin_page')

		
	context = {
		'e_user':user
	}
	return render(request,"adminPanel/edit-user.html",context)


def verify(request,id):
	if not request.user.is_superuser:
		messages.error(request,"Not Authorized!")
		return redirect('home')
	user = User.objects.get(id=id)
	domain = get_current_site(request).domain
		
	send_mail(user,domain)
	messages.success(request,'Mail send successfully')

	return redirect('admin_page')