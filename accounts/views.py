from django.shortcuts import render,redirect
from .form import RegistrationForm
from . models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

#varification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            #clean data -> To fetch the data from the request
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number = phone_number
            user.save()
            
            #USER ACIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_varification_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            try:
                send_email.send()
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                activation_url = f"http://{current_site.domain}/accounts/activate/{uid}/{token}/"
                print("\n" + "=" * 65)
                print(f">> NEW USER REGISTERED: {user.email}")
                print(f">> CLICK HERE TO ACTIVATE ACCOUNT:")
                print(f">> {activation_url}")
                print("=" * 65 + "\n")
                messages.success(request, 'Registration successful! Copy or click the activation link shown in your terminal.')
                return redirect('login')
            except Exception as e:
                user.delete()
                messages.error(request, f'Registration failed: Could not send verification email ({e}).')
                return redirect('register')
            
    else:
                
        form = RegistrationForm
        
    context = {
        'form'  : form,
    }
    return render(request,'accounts/register.html',context)

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are logged in.")
            return redirect('home')
        else:
            try:
                account = Account.objects.get(email=email)
                if not account.is_active:
                    messages.error(request, "Your account has not been activated yet. Please check your terminal or email for the activation link.")
                elif not account.check_password(password):
                    messages.error(request, "Incorrect password. Please try again.")
                else:
                    messages.error(request, "Invalid login credentials.")
            except Account.DoesNotExist:
                messages.error(request, f"No account found with email '{email}'. Please sign up first.")
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,'You are logged out.')
    return redirect('login')
  
  
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated. Please log in.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid or expired activation link.')
        return redirect('register')

  