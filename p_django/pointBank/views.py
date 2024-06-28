from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError 
from .serializers import UserSerializer, TicketSerializer, LoginSerializer
from .models import User, Ticket
import random
from scripts import mail

locations = [
    "Самара",
    "Бузулук",
    "Оренбург",
    "Колтубановский",
    "Тоцкое",
    "Сорочинск"
]

@api_view(['GET'])
def autocomplete(request):
    query = request.GET.get('query', '')

    suggestions = [location for location in locations if query.lower() in location.lower()]

    return Response(suggestions)

@api_view(['POST'])
def send_code(request):
    email = request.data.get('email', '')
    if not email:
        return Response({'error': 'No email provided'}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User with this email does not exist'}, status=404)

    code = "".join(random.sample("123456789", 4))
    user.lastCode = code
    user.save()

    mail.send_ya_mail([email], f'Ваш код подтверждения {code}')
    
    return Response({'message': 'Confirmation code sent'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def check_code(request):
    email = request.data.get('email', '')
    code = request.data.get('code', '')

    if not email or not code:
        return Response({'error': 'Email and code are required'}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User with this email does not exist'}, status=404)

    if user.lastCode == code:
        user.isEmailConfirmed = True
        user.save()
        return Response({'message': 'Email confirmed successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid code'}, status=400)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        login = serializer.validated_data['login']
        password = serializer.validated_data['password']
        user = authenticate(request, login=login, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data,
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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

class BuyTicketView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        ticket_id = request.data.get('ticket_id')
        if not ticket_id:
            return Response({"error": "Ticket ID is required"}, status=400)
        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found"}, status=404)

        request.user.tickets.add(ticket)
        return Response({"message": "Билет успешно забронирован"}, status=200)

class UserTicketsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        tickets = user.tickets.all()
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status=200)
