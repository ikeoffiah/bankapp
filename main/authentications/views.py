from rest_framework.response import Response
from rest_framework import status
from .models import User
from rest_framework import generics
from .serializers import RegisterSerializer, LoginSerializer
from util.error import Error





class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        error = Error().error(serializer.errors)

        return Response(error, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data=data, context={"request":request})
        if serializer.is_valid():
            email = serializer.data['email']
            user = User.objects.get(email=email)
            name = user.name
            token = user.tokens()

            return Response({
                'name':name,
                'token':token
            }, status=status.HTTP_200_OK)

        error = Error().error(serializer.errors)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)






