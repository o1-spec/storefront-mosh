from django.shortcuts import render
from django.core.cache import cache
from django.core.mail import send_mail,mail_admins,BadHeaderError,EmailMessage
from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customers
from rest_framework.views import APIView
import logging
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
import requests

logger = logging.getLogger(__name__) #playground.views


class HelloView(APIView):
    # @method_decorator(cache_page(5*60))
    def get(self,request):
        try:
            logger.info('Received the response')
            response = requests.get('https://httpbin.org/delay/2')
            data = response.json()
        except request.ConnectionError:
            logger.critical('httpbin is offline')
            
        return render(request, 'hello.html', {'name': 'Mosh'})
        
    #For function bases views we use cache based decorator, for class base views, we use method decorator 
# def say_hello(request):
    # try:
    #     send_mail('subject', 'message','info@moshbuy.com',['bob@moshbuy.com']) #Study it
    # except BadHeaderError:
    #     pass
    
    ##SENDING EMAILS TO MAIL ADMINS
    # try:
    #     mail_admins('subject', 'message', html_message='') ##Function wont work unless the backend has been
    # except BadHeaderError:
    #     pass
    
    #ATTACHING SOMETHING TO OUR EMAILS
    # try:
    #     message = EmailMessage('subject', 'message', 'from@moshbuy.com', ['john@Moshbuy.com'])
    #     message.attach_file('playground/static/images/luffy.png')
    #     message.send()
    # except BadHeaderError:
    #     pass
    
    # #SENDING TEMPLATED MAIL IN DJANGO USING django-templated-mail
    # try:
    #     message= BaseEmailMessage(
    #         template_name='emails/hello.html',
    #         context={'name': 'Mosh'}
    #     )
    #     message.send(['john@moshbuy.com'])
    # except BadHeaderError:
    #     pass
        
    # notify_customers.delay('')
    # key = 'httpbin_result'
    # if cache.get(key) is None:
    #     response = requests.get('https://httpbin.org/delay/2')
    #     data = response.json()
    #     cache.set(key, data)
    
    
    # response = requests.get('https://httpbin.org/delay/2')
    # data = response.json()
    # #A BETTER WAY TO CACHE
    # return render(request, 'hello.html', {'name': 'Mosh'})
