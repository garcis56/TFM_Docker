from django.contrib.auth import logout as do_logout
from django.contrib.auth import login as do_login
from django.contrib.auth import authenticate, update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, PasswordChangeForm

from .forms import SignUpForm
from .forms import EditProfileForm
from .forms import ContactForm
from .tokens import account_activation_token
from .models import Profile

import smtplib
import time


def home(request):
    #profile = Profile.objects.all()
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        if 'search_home' in request.GET:
            search_term = request.GET.get('search_home')
            #profile = Profile.objects.filter(email__icontains="noemi")#raw('SELECT * FROM auth_user WHERE email LIKE 'noemi%'') #filter(email__icontains=search_term)
            print("sth searched")
            #print(profile.email)
        #print(request.user.profile.objects.raw('SELECT * FROM auth_user WHERE email LIKE '%noemi%''))
        return render(request, 'home.html')
    # En otro caso redireccionamos al login
    return redirect('/tfm/login')


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.location = form.cleaned_data.get('location')
            # user can't login until link confirmed
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            # subject = 'Please Activate Your Account'
            send_mail(user.profile.email, user, current_site.domain)
            # load a template like get_template() 
            # and calls its render() method immediately.
            # message = render_to_string('activation_request.html', {
            #    'user': user,
            #    'domain': current_site.domain,
            #    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #    # method will generate a hash value with user related data
            #    'token': account_activation_token.make_token(user),
            # })
            # user.email_user(subject, message)
            return redirect('/tfm/activation_sent/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def contact(request):
    print("contact entered****")
    if request.method == 'POST':
        print("contact post entered****")
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get('subject')
            comment = form.cleaned_data.get('comment')
            user = request.user
            email = request.user.email
            send_mail_contact(subject, comment, user, email)
            return redirect('/tfm/home/')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def send_mail(mail, user, domain):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('no.reply.dotty@gmail.com', 'tpfkrxztqzbplguj')
    subject = 'Please Activate Your Account'
    body = render_to_string('activation_request.html', {
        'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        # method will generate a hash value with user related data
        'token': account_activation_token.make_token(user),
    })

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        mail,
        mail,
        msg
    )

    print('HEY, ACTIVATION EMAIL HAS BEEN SENT!')
    server.quit()


def send_mail_contact(subjectMessage, message, user, emailUser):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('no.reply.dotty@gmail.com', 'tpfkrxztqzbplguj')
    subject = "Contact Form"
    email = 'no.reply.dotty@gmail.com'
    body = render_to_string('contact_email.html', {
        'subject': subjectMessage,
        'message': message,
        'user': user,
        'email': emailUser
    })

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(email, email, msg)
    server.quit()
    print('HEY, CONTACT EMAIL HAS BEEN SENT!')
    return redirect('/tfm/home/')


def login(request):
    # Creamos el formulario de autenticación vacío
    form = AuthenticationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/tfm/home')

    # Si llegamos al final renderizamos el formulario
    return render(request, 'login.html', {'form': form})


def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/tfm/login/')


def activation_sent_view(request):
    return render(request, 'activation_sent.html')


def about_view(request):
    return render(request, 'about.html')


def contact_view(request):
    return render(request, 'contact.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true 
        user.is_active = True
        # set signup_confirmation true
        user.profile.signup_confirmation = True
        user.save()
        do_login(request, user)
        return redirect('/tfm/home')
    else:
        return render(request, 'activation_invalid.html')


def view_profile(request):
    args = {'user': request.user}
    return render(request, 'profile.html', args)


def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/tfm/profile')

    else:
        form = EditProfileForm(instance=request.user)
    args = {'form': form}
    return render(request, 'edit_profile.html', args)


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/tfm/profile')
        else:
            return redirect('tfm/change-password')

    else:
        form = PasswordChangeForm(user=request.user)
    args = {'form': form}
    return render(request, 'change_password.html', args)


def hard_skills_view(request):
    return render(request, 'hard_skills.html')


def soft_skills_view(request):
    return render(request, 'soft_skills.html')


def events_view(request):
    return render(request, 'events.html')


def languages_view(request):
    return render(request, 'languages.html')


def sports_view(request):
    return render(request, 'sports.html')

# def password_reset(request):
#    
#    return 0
#
# def password_reset_done(request):
#    
#    return 0
#
# def password_reset_confirm(request):
#    
#    return 0
