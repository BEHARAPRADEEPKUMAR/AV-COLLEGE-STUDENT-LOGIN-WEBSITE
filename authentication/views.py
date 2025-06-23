from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from csproject import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token
from django.contrib.auth import get_user_model
from authentication.backends import RollnoBackend
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model


User = get_user_model() 

# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    if request.method == "POST":
        rollno = request.POST['rollno']
        fname = request.POST.get('fname', '') 
        lname = request.POST.get('lname', '')  
        dateofbirth = request.POST.get('dateofbirth')
        group = request.POST.get('group')
        achievements = request.POST.get('achievements')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1', '')
        pass2 = request.POST.get('pass2')
        photo = request.FILES.get('photo')
        
        if User.objects.filter(rollno=rollno):
            messages.error(request, "Roll Number already exist! Please try some other rollno.")
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('signup')
        
        if len(rollno)>=12:
            messages.error(request, "Rollno must be 12  charcters!!")
            return redirect('index')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('signup')
        
        if not rollno.isalnum():
            messages.error(request, "rollno must be a Number Only!!")
            return redirect('signup')
        
        myuser = User.objects.create_user(
        email=email,
        password=pass1,
        rollno=rollno,
        dateofbirth=dateofbirth,
        group=group,
        achievements=achievements,
        photo=photo)

        myuser.fname = fname
        myuser.lname = lname
        # myuser.is_active = False
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
        # Welcome Email
        subject = "Welcome to AV College-Student Login!! Page"
        message = "Hello " + myuser.fname + "!! \n" + "Welcome to AV COllege Of Arts ,Science and Commerce Hyderabad!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\n Avians Team\n(BSC MECS final Year)"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ Av College - Django Login!!"
        message2 = render_to_string('email_confirmation.html',{
            
            'name': myuser.fname,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()
        
        return redirect('signin')
        
        
    return render(request, "authentication/signup.html")


# def activate(request,uidb64,token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         myuser = User.objects.get(pk=uid)
#     except (TypeError,ValueError,OverflowError,User.DoesNotExist):
#         myuser = None

#     if myuser is not None and generate_token.check_token(myuser,token):
#         myuser.is_active = True
#         # user.profile.signup_confirmation = True
#         myuser.save()
#         login(request,myuser)
#         messages.success(request, "Your Account has been activated!!")
#         return redirect('signin')
#     else:
#         return render(request,'activation_failed.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        myuser.backend = 'authentication.backends.RollnoBackend'
        login(request, myuser)
        messages.success(request, "Your account has been activated!")
        return redirect('signin')

    return render(request, 'authentication/activation_failed.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages



from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def signin(request):
    if request.method == 'POST':
        rollno = request.POST.get('rollno')
        pass1 = request.POST.get('password')  # Corrected the get method

        # Authenticate using rollno as username field
        user = authenticate(request, username=rollno, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.fname  # Corrected attribute name
            return render(request, "authentication/index.html", {"fname": fname})
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('signin')  # Ensure 'signin' is a valid route name

    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('signin')


User = get_user_model()  

def profile(request, rollno):
    user = get_object_or_404(User, rollno=rollno)  
    return render(request, "authentication/profile.html", {"user": user})

def index(request):
    return render(request, "authentication/index.html")

def exam(request):
    return render(request, "authentication/exam.html")


def about(request):
    return render(request, "authentication/about.html")

def notes(request):
    return render(request, "authentication/notes.html")

def feedback(request):
    return render(request, "authentication/feedback.html")