"""
Override jtw_payload_handler method
"""
import jwt
from datetime import datetime, timedelta

from django.conf import settings
from itsdangerous import URLSafeTimedSerializer


def _generate_jwt_token(pk):
    """
    Generates a JSON Web Token that stores this user's ID and has an expiry
    date set to 60 days into the future. But, now it is set to 1 hour.
    """
    dt = datetime.now() + timedelta(seconds=3600)

    token = jwt.encode({
        'id': pk,
        'exp': int(dt.strftime('%s'))
    }, settings.SECRET_KEY, algorithm='HS256')

    return token.decode('utf-8')


SECRET_KEY = 'testing_key'
ACCOUNT_CONFIRMATION_SECRET_KEY_SALT = 'salt-for-confirm-account-mirenta'


def generate_confirm_account_email_token(email):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt=ACCOUNT_CONFIRMATION_SECRET_KEY_SALT)


def confirm_token_for_account_confirmation(token, expiration=7200):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=ACCOUNT_CONFIRMATION_SECRET_KEY_SALT,
            max_age=expiration
        )
    except:
        return False
    return email
