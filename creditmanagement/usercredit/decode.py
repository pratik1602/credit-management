from .models import User
import jwt
from creditmanagement.settings import SECRET_KEY

JWT_ALGORITHM = "HS256"

def get_object(request): 
    gettoken =  request.META.get('HTTP_AUTHORIZATION', None)
    token = gettoken.split(" ", 1)[1]
    user_json = jwt.decode(token, SECRET_KEY, JWT_ALGORITHM )
    id = user_json['user_id']
    getuser = User.objects.get(id=id)   
    return getuser

