import profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings



def createprofile(sender,instance,created,**kwargs):
    userobj=instance
    if created:
        profile = Profile.objects.create(
            user=userobj,
            name=userobj.username,
            username=userobj.username,
            email=userobj.email,
        )
        print('profile is created for this user')

        subject = "welcome to developer's web application"
        message = "we are glad you are here"

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )

def deleteUser(sender,instance,**kwargs):
    profile = instance
    userobj = profile.user
    userobj.delete()
    print('user also deleted')


def updateUser(sender,instance,created,**kwargs):
    if created == False :
        profile = instance
        user = profile.user
        user.first_name = profile.name
        user.email = profile.email
        user.username = profile.username
        user.save()
        print('User Record Updated')



post_save.connect(updateUser,sender=Profile)
post_save.connect(createprofile, sender=User)
#post_delete.connect(deleteUser, sender=Profile)        