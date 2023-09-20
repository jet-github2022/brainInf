from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Blog
from .models import Contact
from django.db.models import Q
from .models import Subscribers
from . forms import SubscribersForm, MailMessageForm, CommentForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
# from . tokens import generate_token
from mydate import settings


def home(request):
    if 'q' in request.GET:
        q = request.GET['q']
        # posts = Blog.objects.filter(title__icontains=q)
        multiple_q = Q(Q(title__icontains=q))
        posts = Blog.objects.filter(multiple_q) 
    else:
        posts = Blog.objects.all()
    return render(request, 'info/home.html', {'posts': posts})


def blog(request, pk):
    posts = Blog.objects.get(id=pk)

    comments = posts.comments.filter(status=True)

    user_comment = None

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.posts = posts
            user_comment.save()
            return HttpResponseRedirect('/')
    else:
        comment_form = CommentForm()
    return render(request, 'info/blogs.html', {'posts': posts,
                                               'comment': user_comment,
                                               'comments': comments,
                                               'comment_form': comment_form, },
                  )


def about(request):
    return render(request, 'info/about.html')


def contact(request):
    if request.method == "POST":
        contact = Contact()
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact.name = name
        contact.email = email
        contact.number = number
        contact.subject = subject
        contact.message = message
        contact.save()

        messages.success(request,"Thanks For Contacting Me!")
        return redirect('contact')
    return render(request, 'info/contact.html')


def signUp(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist")
            return redirect('signup')

        if User.objects.filter(email=email):
            messages.error(request, "Email already taken")
            return redirect('signup')

        if len(username) > 10:
            messages.error(request, "Username must not be more than 10 characters")

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match")

        if not username.isalnum():
            messages.error(request, "Username must be alpha-numeric")
            return redirect('signup')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()

        messages.success(request, f"new account created: we sent you confirmation email, please confirm to activate your account" )

        # welcome email
        subject = "welcome Jet"
        message = "Hello" + myuser.first_name + "!! \n" + "welcome to Jet \n confirm your email to activate your account"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email address confirmation Email

        # current_site = get_current_site(request)
        # email_subject = "Confirm your email @ Jetreyict!!"
        # message2 = render_to_string("info/activate_account.html", {
        #     'name': myuser.first_name,
        #     'domain': current_site.domain,
        #     'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
        #     'token': generate_token.make_token(myuser),
        # })
        # email = EmailMessage(
        #     email_subject,
        #     message2,
        #     settings.EMAIL_HOST_USER,
        #     [myuser.email],
        # )
        # email.fail_silently = True
        # email.send()


        return redirect('login')
    return render(request, 'info/signup.html')


def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = auth.authenticate(username=username, password=pass1)

        if user is not None:
            auth.login(request, user)
            fname = user.first_name
            return redirect('/', {'fname': fname})
        else:
            messages.error(request, 'information Invalid')
            return redirect('login')
    else:
        return render(request, 'info/login.html')


def logoutUser(request):
    auth.logout(request)
    return redirect('/')


def news(request):
    if request.method == 'POST':
        form = SubscribersForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subscription Successful')
            return redirect('news')
    else:
        form = SubscribersForm()
    context = {
        'form': form,
    }
    return render(request, 'info/mail_letter.html', context)


def mail(request):
    # emails = Subscribers.objects.all()
    # df = read_frame(emails, fieldnames=['email'])
    # mail_list = df['email'].values.tolist()
    if request.method == 'POST':
        form = MailMessageForm(request.POST)
        if form.is_valid():
            form.save()
            title = form.cleaned_data.get('title')
            message = form.cleaned_data.get('message')
            # send_mail(
            #     'Testing message',
            #     'here is the testing message for test',
            #     'pythondjango95@gmail.com',
            #     ['jetreyict@gmail.com'],
            #
            #     # mail_list,
            #     fail_silently=False,
            # ),
            messages.success(request, 'Message Sent!')
            return redirect('mail')
    else:
        form = MailMessageForm()
    context = {
        'form': form,
    }
    return render(request, 'info/mail.html', context)

#
# def activate(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         myuser = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         myuser = None
#
#     if myuser is not None and generate_token.check_token(myuser, token):
#         myuser.is_active = True
#         myuser.save()
#         auth.login(request, myuser)
#         return redirect('/')
#     else:
#         return render(request, 'info/activation_fail.html')

# Create your views here.
