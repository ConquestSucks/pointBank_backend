from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, TicketSerializer, LoginSerializer
from .models import User, Ticket

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login = serializer.validated_data['login']
        password = serializer.validated_data['password']
        user = authenticate(login=login, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data,
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class TicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer

    def get_queryset(self):
        from_location = self.request.query_params.get('from_location', None)
        to_location = self.request.query_params.get('to_location', None)
        departure_date = self.request.query_params.get('departure_date', None)
        
        if from_location and to_location and departure_date:
            queryset = Ticket.objects.filter(from_location=from_location, to_location=to_location, departure__date=departure_date)
        else:
            queryset = Ticket.objects.none()
        
        return queryset

