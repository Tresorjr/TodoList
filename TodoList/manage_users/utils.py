import logging
import random
import string
from datetime import timedelta

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import IntegrityError

from .models import OneTimePasscode

logger = logging.getLogger(__name__)
User = get_user_model()

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

def send_otp_email(user):
    try:
        user_id = user.id
        user = User.objects.get(id=user_id)
        logger.info(f"Utilisateur trouvé : {user.email}")

        existing_otp = OneTimePasscode.objects.filter(user=user).first()
        if existing_otp:
            logger.warning(f"Un OTP existe déjà pour l'utilisateur {user.id}. Le code sera remplacé.")
            existing_otp.code = generate_otp()
            existing_otp.expires_at = timezone.now() + timedelta(minutes=1)
            existing_otp.save()
            otp_code = existing_otp.code
        else:
            otp_code = generate_otp()
            otp_instance = OneTimePasscode(
                user=user,
                code=otp_code,
                expires_at=timezone.now() + timedelta(minutes=1)
            )
            otp_instance.save()

        subject = "Code OTP pour la vérification de votre email"
        email_body = render_to_string("otp_email.html", {
            "otp": otp_code,
            "user": user,
            "current_site": "managetodolist.com",
        })

        d_email = EmailMessage(subject, email_body, settings.EMAIL_HOST_USER, [user.email])
        d_email.content_subtype = "html"
        d_email.send(fail_silently=False)

        logger.info(f"OTP envoyé avec succès à {user.email}")
        return True

    except User.DoesNotExist:
        logger.error(f"Utilisateur avec l'ID {user_id} introuvable.")
        return False

    except IntegrityError as e:
        logger.error(f"Erreur d'intégrité de la base de données : {str(e)}")
        return False

    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'OTP : {str(e)}")
        return False  # ou raise e si tu veux voir l'erreur

def send_normal_email(data):
    try:
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            from_email=settings.EMAIL_HOST_USER,
            to=[data['to_email']]
        )
        email.send()
        logger.info(f"Email envoyé avec succès à {data['to_email']}")
        return True
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'email normal : {str(e)}")
        return False
