from nelsonetworkapi.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def check_user(request):
    try:
        
        uid = request.data.get('uid')

        user = User.objects.filter(uid=uid).first()

        if user:
            data = {
                'userId': user.user_id,
                'userName': user.user_name,
                'password': user.password,
                'email': user.email,
                'role': user.role,
            }
            return Response(data)
        else:
            return Response({'valid': False}, status=404)
    except KeyError:
        return Response({'error': "'uid' key is missing in the request"}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['POST'])
def register_user(request):
    user = User.objects.create(
        user_id=request.data['user_id'],
        username=request.data['username'],
        password=request.data['password'],
        email=request.data['email'],
        role=request.data['role'],
    )

    data = {
        'user_id': user.id,
        'username': user.username,
        'password': user.password,
        'email': user.email,
        'role': user.role,
    }

    return Response(data)
