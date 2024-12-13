
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from barangay.decorators import role_required
from django.core.paginator import Paginator
from .forms import *
from datetime import datetime
from django.utils.timezone import now 
import pytz
from django.db.models import Sum, Max
from twilio.rest import Client
from django.http import JsonResponse





def home(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('officials')
    
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Account does not exist')
            return render(request, 'public/home.html', {'page': page})

        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Check user's status and code
            if user.status == 'verified' or user.code == 0:
                if user.lock == 'restricted':
                    logout(request)
                    messages.error(request,'Please Try Again Later.')
                    return redirect('home')
                else:
                    user.log_status = "online"
                    user.save()
                    login(request, user)
                    messages.success(request,'Login succesfully')
                    return redirect('officials')
            else:
                # Save email in session and render a template for email verification
                request.session['unverified_email'] = email
                messages.success(request,'Please Verify your Account')
                return render(request, 'otpverify.html', {'user': user})
        else:
            messages.error(request, 'Username OR password does not exist')
    context = {
        'page': page,
    }
    return render(request,'index.html',context)


def signup(request):
    form = create_account_form()
    if request.method == 'POST':
        form = create_account_form(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            request.session['unverified_email'] =  user.email
            user.username = user.username.lower()
            user.code = int(get_random_string(length=6, allowed_chars='1234567890'))
            user.save()
            
            subject = 'Registration OTP'
            message = f'OTP  {user.code}. Enter this code to complete your registration and do not share to others.'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = user.email
            try:
                send_mail(subject, message, from_email, [to_email], fail_silently=False)
            except Exception as e:
                messages.error(request, f"Error sending email: {e}")
            #login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # for Direct log in after registration
            messages.success(request, 'Account Created Successfully')
            return redirect('verify_email')
        else:
            messages.error(request, 'An error occurred during registration {form.errors}')
    context = {
        'form': form,
    }
    return render(request,'signup.html',context)




def verify_email(request):
    
    if request.method == 'POST':
        otp = request.POST.get("otp")
        email = request.session['unverified_email']

        if not email:
            messages.error(request, 'Email not found in session')
            return redirect('home')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect('home')

        # Perform pattern match on user code
        if str(user.code) == otp:
            user.status = "verified"
            user.code = 0  # Assuming 0 represents the verified status
            user.save()
            messages.info(request, 'Account verified and signed in successfully...')
            subject = 'Account Verification'
            message = f'Congratulations! Your account is now verified. You can now log in. '
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = user.email
            send_mail(subject, message, from_email, [to_email], fail_silently=False)
            request.session.flush()
            messages.success(request, "Account Verified")
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('users')
        else:
            messages.error(request, "Code doesn't match")

    return render(request, 'otpverify.html')



#-


@login_required(login_url='home')
#@role_required(allowed_roles=['1'], redirect_url='users')
def officials(request):
    current_datetime_with_tz = now()
    list_user = User.objects.filter(roles='2', is_superuser=0).count()
    users = request.user
    calibrations_details = get_object_or_404(calibrations,pk=1)
    if request.method == 'POST':
        form = calibrationsform(request.POST, request.FILES, instance=calibrations_details)
        if form.is_valid():
            shop = form.save(commit=False)  
            shop.save()  
            messages.success(request, "Parameters Calibrated")
            return redirect('officials')
        else:
            print(form.errors)  
            messages.error(request, "Please Try Again")
    else:
        form = calibrationsform(instance=calibrations_details)
    context = {
        'users':users,
        'list_user':list_user,
        'form':form,
        'calibrations_details':calibrations_details,
        'current_datetime_with_tz':current_datetime_with_tz
    }
    return render(request, 'barangay/index.html',context)



@login_required(login_url='home')
@role_required(allowed_roles=['1'], redirect_url='users')
def system_users(request):
    users = request.user
    list_user = User.objects.filter(roles='2', is_superuser=0)
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            add_admin = form.save(commit=False)
            roleid = request.POST.get('userrole')
            role_details = user_roles.objects.get(id=roleid)
            raw_password = form.cleaned_data.get('password1')
            request.session['unverified_email'] = add_admin.email
            add_admin.username = add_admin.username.lower()
            add_admin.roles = '2'
            add_admin.userrole = role_details
            add_admin.code = int(get_random_string(length=6, allowed_chars='1234567890'))
            add_admin.save()
            # Send OTP to the user's email
            subject = 'Account Registration'
            message = f'''
                        Hi Good Day , this is safenest, your account has been created by the site administration and
                        here is your credentials.
                        Account Email :{add_admin.email} ,
                        Password: {raw_password} ,
                        Your OTP for Registration is here,  {add_admin.code}. don't share your otp to anyone'''
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = add_admin.email
            send_mail(subject, message, from_email, [to_email], fail_silently=False)

            messages.success(request, 'Account Created Successfully')
            return redirect('system_users')
        else:
            messages.error(request, 'An error occurred during registration')
    else:
        # Initialize the form for GET request
        form = MyUserCreationForm()

    context = {
        'users': users,
        'form': form,
        'list_user':list_user,
    }
    return render(request, 'barangay/users.html', context)




@login_required(login_url='home')
@role_required(allowed_roles=['1'], redirect_url='users')
def user_roles_system(request):
    users = request.user
    roles = user_roles.objects.all()
    if request.method == 'POST':
        form = user_role_form(request.POST, request.FILES)
        if form.is_valid():
            shop = form.save(commit=False)  
            shop.save()  
            messages.success(request, "Roles Added")
            return redirect('user_roles_system')
        else:
            print(form.errors)  
            messages.error(request, "Please Try Again")
    else:
        form = user_role_form()
    context = {
        'users':users,
        'form':form,
        'roles':roles,
       
       
    }
    return render(request, 'barangay/roles.html',context)



@login_required(login_url='home')
@role_required(allowed_roles=['1'], redirect_url='users')
def user_roles_edit(request,pk):
    role_detail = get_object_or_404(user_roles,pk=pk)
    roles = user_roles.objects.all()
    users = request.user
    if request.method == 'POST':
        form = user_role_form(request.POST, request.FILES, instance=role_detail)
        if form.is_valid():
            shop = form.save(commit=False)  
            shop.save()  
            messages.success(request, "Edited Succesfully")
            return redirect('user_roles_system')
        else:
            print(form.errors)  
            messages.error(request, "Please Try Again")
    else:
        form = user_role_form(instance=role_detail)
    context = {
        'users':users,
        'form':form,
        'roles':roles,
       
       
    }
    return render(request, 'barangay/roles.html',context)


@login_required(login_url='home')
@role_required(allowed_roles=['1'], redirect_url='users')
def user_roles_delete(request,pk):
    role_detail = get_object_or_404(user_roles,pk=pk)
    role_detail.delete()
    messages.success(request, "Deleted Succesfully")
    return redirect('user_roles_system')



@login_required(login_url='home')
@role_required(allowed_roles=['1'], redirect_url='users')
def user_system_delete(request,pk):
    role_detail = get_object_or_404(User,pk=pk)
    role_detail.delete()
    messages.success(request, "Deleted Succesfully")
    return redirect('system_users')





@login_required(login_url='home')
def profile_users(request):
    users = request.user
    roles = user_roles.objects.all()
    if request.method == 'POST':
        form = profileform(request.POST, request.FILES,instance=users)
        if form.is_valid():
            pro = form.save(commit=False)  
            pro.save()  
            messages.success(request, "Profile Updated")
            return redirect('profile_users')
        else:
            print(form.errors)  
            messages.error(request, "Please Try Again")
    else:
        form = profileform(instance=users)
    context = {
        'users':users,
        'form':form,
        'roles':roles,
       
       
    }
    return render(request, 'barangay/profile.html',context)





@login_required(login_url='home')
def aboutus(request):
    users = request.user
    context = {
        'users':users,
    }
    return render(request, 'barangay/aboutus.html',context)

@login_required(login_url='home')
@role_required(allowed_roles=['2'], redirect_url='officials')
def users(request):
    users = request.user
    
    context = {
        'users':users,
       
       
    }
    return render(request, 'barangay/roles.html',context)



#-------------------------------------------------------------------


@login_required(login_url='home')
def history(request):
    users = request.user
    
    context = {
        'users':users,
       
       
    }
    return render(request, 'barangay/history.html',context)




@login_required(login_url='home')
def emailalert(request):
    users = request.user
    subject = 'Water Alert'
    message = f'''Lubug ya kame'''
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = users.email
    send_mail(subject, message, from_email, [to_email], fail_silently=False)
    messages.success(request, "Alerted Successfully")
    return redirect('officials')
    

@login_required(login_url='home')
@role_required(allowed_roles=['1'], redirect_url='users')
def twillio(request):
    phone_number = "+639979431921"
    message_text = "Hi Alert, lubug ya kame"

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    
    # Sending SMS
    try:
        message = client.messages.create(
            body="Hello! This is a test message from Django and Twilio.",
            from_=settings.TWILIO_PHONE_NUMBER,  # Your Twilio phone number
            to='+639979431921'  # Recipient's phone number
        )
        
        return JsonResponse({'status': 'success', 'message_sid': message.sid})
    except Exception as e:
        return JsonResponse({'status': 'error', 'error': str(e)})

 


def logoutUser(request):
    user = request.user
    user.log_status = "offline"
    user.save()
    logout(request)
    return redirect('home')


