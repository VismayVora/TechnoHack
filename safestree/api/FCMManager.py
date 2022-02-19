
import firebase_admin
from firebase_admin import credentials, messaging
from fcm_django.models import FCMDevice
from safestree import settings

cred = credentials.Certificate(settings.cred)
firebase_admin.initialize_app(cred)

def sendPush(title,msg,dataObject):
    device = FCMDevice.objects.all().first()
    message = messaging.Message(
        notification = messaging.Notification(title = title,
        body=msg,),
        data = dataObject,
        )
    response = device.send_message(message)
    print({'message sent'},response)