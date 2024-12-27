from time import sleep
# from storefront.celery import celery
from celery import shared_task

#@celery.task #With this approach, our plaugrounds app wont be independent but dependent on the storefront app
@shared_task
def notify_customers(message):
    print('Sending 10k emails')
    print(message)
    sleep(10)
    print('Email successfully sent!')