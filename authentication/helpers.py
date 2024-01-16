from django.http import JsonResponse

import os
import uuid
import random
import string
import jwt
import datetime

secret_key = '98f1ebfb9b92fbc29e5a2ae52cbe112badafec8ac53e82d84a531e2b87d13e1c4a2814299bbca4ead05793ab336310327b8293b72688dbe34c310888024e0105'

def require_access_token(view_func):
    def _wrapped_view(request, *args, **kwargs):
        token = request.session.get('token')  # Change this to how you store your token
        if token:
            try:
                payload = jwt.decode(token, secret_key, algorithms=['HS256'])
                # You can perform additional checks on the payload if needed
                return view_func(request, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                # Handle expired token
                return JsonResponse({'error': 'Token has expired'}, status=401)
            except jwt.DecodeError:
                # Handle invalid token
                return JsonResponse({'error': 'Invalid token'}, status=401)
        else:
            # Handle missing token (e.g., redirect to the login page)
            return JsonResponse({'error': 'Token required'}, status=401)
    return _wrapped_view

def generate_otp(digit):
    otp = ''
    digits = string.digits
    for d in range(digit):
        otp += str(random.randint(1, len(digits)-1))
    return otp


def custom_file_name(instance, filename):
    """
    This function will create unique name for file
    """
    # Get the file's extension
    ext = filename.split('.')[-1]

    # Generate a unique name for the file
    unique_filename = f"{uuid.uuid4().hex}.{ext}"

    # Return the new file path
    return os.path.join(f'{instance.DIR_NAME}/', unique_filename)

def textLower(text):
    """
    This function will convert string into a lowercase
    """
    try:
        if not isinstance(text, str):
            raise TypeError("Input is not a string")
        return text.lower()
    except TypeError as e:
        return str(e)
    

def generate_password(length=8, include_digits=True, include_special_chars=True):
    """
    Function will generate 8 or more digit password
    """
    characters = string.ascii_letters
    if include_digits:
        characters += string.digits
    if include_special_chars:
        characters += '@_#*'

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def create_jwt_token(email):
    payload = {
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=10), 
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

def decode_jwt_token(token):
    payload = jwt.decode(token, secret_key, algorithms=['HS256'])
    return payload


def get_latest_pics(model, field_name, limit=12):
    # Retrieve the first 'limit' items ordered by the specified field in descending order
    return model.objects.order_by(f'-{field_name}')[:limit]