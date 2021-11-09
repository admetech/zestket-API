from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from server.communication.providers.telegram import TelegramService
from server.utlities import (
    CommunicationUtilites,
)

import random
import string

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class GenerateUserOTP(APIView):
    """Generate the OTP

    Generate a 4 digit otp for the user to authenticate itself

    """
    @swagger_auto_schema(manual_parameters=[])
    def post(self, request):
        try:
            phone = request.POST.get("phone")
            if phone is not None and (len(phone) >= 10) and phone.isdigit():
                # if phone number is present
                
                #  generate the OTP
                otp = ''.join(random.choice(string.digits) for i in range(4))

                try:
                    # get the user details on based on phone number
                    user_detail = get_user_model().objects.get(phone=phone)

                except get_user_model().DoesNotExist as e:
                    # if user doesn't exist
                    user_detail = get_user_model()(
                        phone   = phone,
                    )
                
                finally:
                    # set the otp as password
                    user_detail.set_password(otp)
                    
                    # save the user new password
                    user_detail.save()

                    if settings.DEV or settings.DEBUG:
                        # sent the OTP to the telegram bot 
                        TelegramService.send_message(
                            TelegramService,
                            text = f'OTP Requested : {phone} : {otp}'
                        )
                    else:
                        # send the OTP via SMS to the user
                        sent_otp = CommunicationUtilites.SendSMS(
                            CommunicationUtilites,
                            message = f'login otp is {otp}',
                            phoneNumber = f"+91{phone}",
                        )

                return Response({"success": True}, status=202)
            
            return Response({"success": False, "error": f'phone number is needed' }, status=400)

        except Exception as e:
            return Response({"success": False, "error": f'{e}' }, status=400)

        return Response({"success": False }, status=405)
