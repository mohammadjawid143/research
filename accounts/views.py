from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required



from .forms import UserForm
from .utils import send_verification_email
from .models import User

# Create your views here.



def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'شما هم‌اکنون وارد حساب خود شده‌اید!')
        return redirect('home') 
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # hash password
            user.save()
            
            #Send verification email
            mail_subject = 'فعالسازی حساب کاربری'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request,  'حساب کاربری شما با موفقیت ثبت شد!')
            return redirect('registerUser')  # or another page
        else:
            print(form.errors)
    else:
        form = UserForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/registeruser.html', context)


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'تبریک! حساب کاربری شما فعال شد.')
        return redirect('home')
    else:
        messages.error(request, 'لینک فعال‌سازی نامعتبر است.')
        return redirect('home')
    

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'شما قبلاً وارد شده‌اید!')
        return redirect('home')    

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # استفاده درست از username=email
        user = auth.authenticate(username=email, password=password)
        
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                messages.success(request, 'با موفقیت وارد شدید.')
                return redirect('home')
            else:
                messages.error(request, 'حساب شما هنوز فعال نشده است. لطفاً ایمیل خود را بررسی کنید.')
                return redirect('login')
        else:
            messages.error(request, 'ایمیل یا رمز عبور اشتباه است.')
            return redirect('login')

    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'با موفقیت از حساب کاربری خارج شدید.')
    return redirect('login')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            
            #send reset password email
            mail_subject = 'بازنشانی رمز عبور'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, 'لینک بازنشانی رمز عبور به ایمیل شما ارسال شد.')
            return redirect('login')
        else:
            messages.error(request, 'حساب کاربری با این ایمیل وجود ندارد.')
            return redirect('forgot_password')
            
    return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    # Validate the user by decoding the token 
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'لطفاً رمز عبور جدید خود را تعیین کنید.')
        return redirect('reset_password')
    else:
        messages.error(request, 'این لینک منقضی شده است.')
        return redirect('home')

    return 

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            
            messages.success(request, 'رمز عبور با موفقیت تغییر کرد.')
            return redirect('login')
        else:
            messages.error(request, 'رمزهای وارد شده یکسان نیستند!')
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')
