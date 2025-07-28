from CustomUser.models import User
from rest_framework_simplejwt.tokens import RefreshToken

def sign_up_service(user_data):
    user_present = User.objects.filter(
        email=user_data['email']).exists()
    if user_present:
        raise Exception('User already exists')
    user = User(username =user_data['email'], email=user_data['email'], name = user_data['name'])
    user.set_password(user_data['password'])
    user.save()

    return user

def login_service(email, password):
    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            print(user.name)
            t= user.generate_token()
            print(t)
            return t
        else:
            raise Exception('Invalid password')
    except User.DoesNotExist:
        raise Exception('User does not exist')