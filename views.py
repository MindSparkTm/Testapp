from django.views.generic import DetailView, ListView, UpdateView, CreateView, View
from django.shortcuts import render, redirect, reverse
from .models import SignUp
import random
import sendgrid
import os
from sendgrid.helpers.mail import *
import base64
from django.contrib.sessions.models import Session
from django.http import Http404


from twilio.rest import Client



class usersignup(CreateView):

    def get(self,request):
        return render (request,'registration/register.html')

    def post(self,request):
        model = SignUp
        try:
            mobilenumber = request.POST['mobilenumber']
            email = request.POST['email']
            password = request.POST['password']
            smscode = random.randint(1000, 9999)
            print('smscode', smscode)
            emailcode = random.randint(1000, 9999)
            print('emailcode', emailcode)
            print(mobilenumber, email, password)
            request.session['emailcode'] = emailcode
            request.session['smscode'] = smscode
            request.session['email'] = email
            request.session['mobilenumber'] = mobilenumber
            request.session['password'] = password

            sendemailcode("smartsurajit2008@gmail.com", email, str(emailcode))

            sendsms('+254771621350', "Hey testing code is" + str(smscode))
            # that is the number that is registered in twilio sandbox to receive notifications in trial account
            # sendsms(mobilenumber, "Hey testing code is" + str(smscode))
            # all new numbers has to be registered in twilio sandbox as i am using a trial account or else twilio will give an error

            return redirect('emailverify')


        except Exception:

            raise Http404
            # or
            return redirect('error')







class login(CreateView):

    def get(self,request):
        return render (request,'registration/login.html')

    def post(self,request):
        model = SignUp

        email = request.POST['email']
        password = request.POST['password']
        signup = SignUp.objects.filter(email=email,password=password).values()
        if not signup:
            return redirect('login')
        else:
            print(type(signup))
            for userdetails in signup:
                print('userdetails',userdetails)
                customermobilenumber = userdetails['mobilenumber']
                request.session['email'] = email
                smscode = random.randint(1000, 9999)
                print('smscode', smscode)
                emailcode = random.randint(1000, 9999)
                print('emailcode', emailcode)
                request.session['emailcode'] = emailcode
                request.session['smscode'] = smscode

                sendemailcode("smartsurajit2008@gmail.com", email, str(emailcode))

                sendsms('+254771621350', "Hey testing code is" + str(smscode)) #that is the number that is registered in twilio sandbox to receive notifications in trial account
            #sendsms(customermobilenumber, "Hey testing code is" + str(smscode))
            # all new numbers has to be registered in twilio sandbox as i am using a trial account or else twilio will give an error

            return redirect("loginemailverify")








class emailverification(CreateView):

    def get(self,request):
        if request.session._session:
            return render (request,'registration/emailverification.html')
        else:
            return redirect('usersignup')


    def post(self,request):

        try:
            email_code = str(request.POST['emailcode'])
            session_email_code = str(request.session['emailcode'])
            print(type(email_code))
            print(type(session_email_code))

            if (email_code == session_email_code):
                print('verified')
                return redirect('smsverify')
            else:
                return redirect('emailverify')



        except Exception:
            raise Http404
            return redirect('error')


class loginemailverification(CreateView):

    def get(self,request):
        if request.session._session:
            return render(request, 'registration/emailverification.html')
        else:
            return redirect('usersignup')


    def post(self,request):

        try:

            email_code = str(request.POST['emailcode'])
            session_email_code = str(request.session['emailcode'])
            print(type(email_code))
            print(type(session_email_code))

            if (email_code == session_email_code):
                print('verified')
                return redirect('loginsmsverify')
            else:
                return redirect('loginemailverify')






        except Exception:
            raise Http404
            return redirect('error')







class smsverification(CreateView):
    model = SignUp

    def get(self,request):
        if request.session._session:
            return render(request, 'registration/smsverification.html')
        else:
            return redirect('usersignup')

        return render (request,'registration/smsverification.html')

    def post(self,request):

        try:
            sms_code = str(request.POST['smscode'])
            session_sms_code = str(request.session['smscode'])

            if (sms_code == session_sms_code):
                print('verified sms')
                email_id = str(request.session['email'])
                mobile_number = str(request.session['mobilenumber'])
                password = str(request.session['password'])
                print('email', email_id, mobile_number, password)

                signup = SignUp(email=email_id, mobilenumber=mobile_number, password=password)
                signup.save()

                print('verified.')
                return redirect('success')
            else:
                return redirect('smsverify')

        except Exception:
            raise Http404
            return redirect('error')




class loginsmsverification(CreateView):
    model = SignUp

    def get(self, request):
        if request.session._session:
            return render(request, 'registration/smsverification.html')
        else:
            return redirect('usersignup')

        return render(request, 'registration/smsverification.html')

    def post(self, request):

        try:
            sms_code = str(request.POST['smscode'])
            session_sms_code = str(request.session['smscode'])

            if (sms_code == session_sms_code):
                print('verified sms')



                return redirect('success')

            else:
                return redirect('smsverify')

        except Exception:
            raise Http404
            return redirect('error')


def sendemailcode(sender,recipient,content):

    sg = sendgrid.SendGridAPIClient(apikey="")
    mail = Mail()
    from_email = Email(sender)
    to_email = Email(recipient)
    subject = "Activation link"
    per = Personalization()
    mail.from_email = from_email
    mail.subject = subject
    html_content = Content("text/html", "<html><head>"+content+"</head><body></body></html>")
    plain_content = Content("text/plain", "and easy ")

    ### Add plain content first
    mail.add_content(plain_content)

    ### Add HTML content next
    mail.add_content(html_content)

    per.add_to(to_email)
    mail.add_personalization(per)
    response = sg.client.mail.send.post(request_body=mail.get())
    print('response',response)




def sendsms(recipient,smscode):
    account_sid = ''
    auth_token = ''
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body=smscode,
        from_='+13144622117',
        to=recipient
    )

    print(message.sid)









class successpage(CreateView):

    def get(self,request):
        if request.session._session:
            Session.objects.all().delete()

            return render(request,"registration/success.html")
        else:
            return redirect('usersignup')


class error(CreateView):
    def get(self,request):
        return render(request,'registration/error.html')
