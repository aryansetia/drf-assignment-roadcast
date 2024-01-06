from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomUserSerializer  
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication 
from .models import CustomUser
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.decorators import throttle_classes
from rest_framework.throttling import UserRateThrottle



@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    # Use the custom user serializer to validate and create a new user
    serializer = CustomUserSerializer(data=request.data)
    
    if serializer.is_valid():
        # Create a new user
        user = serializer.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    else:
        # Return validation errors if the serializer is not valid
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    # Check if the user exists
    try:
        user = get_user_model().objects.get(email=email)
    except get_user_model().DoesNotExist:
        return Response({'error': 'User does not exist. Please sign up first.'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the provided password is correct
    if user.check_password(password):
        # Generate and return JWT token
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Login successful',
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }, status=status.HTTP_200_OK)
    else:
        # Incorrect password
        return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def search_users(request):
    query = request.GET.get('query')
    # Exact email match
    exact_email_user = CustomUser.objects.filter(email__iexact=query).first()
    if exact_email_user:
        serializer = CustomUserSerializer(exact_email_user)
        return Response(serializer.data, status=status.HTTP_200_OK) 

    # Partial name match
    name_users = CustomUser.objects.filter(name__icontains=query)

    page = request.GET.get('page', 1)
    paginator = Paginator(name_users, 10)  # Show 10 users per page

    try:
        paginated_users = paginator.page(page)
    except PageNotAnInteger:
        paginated_users = paginator.page(1)
    except EmptyPage:
        paginated_users = paginator.page(paginator.num_pages)

    serializer = CustomUserSerializer(paginated_users, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def manage_friend_request(request):
    data = request.data
    user_email = data.get('user_email', '')
    action = data.get('action', '')

    from_user = request.user.profile
    to_user = get_object_or_404(CustomUser, email=user_email)

    if action == 'accept':
        # Accept friend request
        if to_user not in from_user.friend_requests_received.all():
            return Response({'error': 'No friend request to accept.'}, status=status.HTTP_400_BAD_REQUEST)

        from_user.friends.add(to_user)
        to_user.profile.friends.add(from_user.user)
        from_user.friend_requests_received.remove(to_user)
        to_user.profile.friend_requests_sent.remove(from_user.user)

        return Response({'message': 'Friend request accepted successfully.'}, status=status.HTTP_200_OK)

    elif action == 'reject':
        # Reject friend request
        if to_user not in from_user.friend_requests_received.all():
            return Response({'error': 'No friend request to reject.'}, status=status.HTTP_400_BAD_REQUEST)

        from_user.friend_requests_received.remove(to_user)
        to_user.profile.friend_requests_sent.remove(from_user.user)

        return Response({'message': 'Friend request rejected successfully.'}, status=status.HTTP_200_OK)

    else:
        return Response({'error': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])  # Add UserRateThrottle for rate limiting
def list_friends(request):
    user_profile = request.user.profile

    # Get the list of friends
    friends = user_profile.friends.all()

    # Serialize the list of friends
    serializer = CustomUserSerializer(friends, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def pending_requests(request): 
    user_profile = request.user.profile 

    requests = user_profile.friend_requests_received.all()

    serializer = CustomUserSerializer(requests, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def send_request(request): 
    data = request.data 
    user_email = data.get('email', '')

    from_user = request.user.profile
    to_user = get_object_or_404(CustomUser, email=user_email)
    
    if from_user.user == to_user:
        return Response({'error': 'Cannot send friend request to yourself.'}, status=status.HTTP_400_BAD_REQUEST)

    if to_user in from_user.friends.all():
        return Response({'error': 'User is already your friend.'}, status=status.HTTP_400_BAD_REQUEST)

    if to_user in from_user.friend_requests_sent.all():
        return Response({'error': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if to_user in from_user.friend_requests_received.all():
        return Response({'error': f"{to_user} is already in your pending friend requests, please accept the request from there to add!"})
    
    from_user.friend_requests_sent.add(to_user)
    to_user.profile.friend_requests_received.add(from_user.user)

    return Response({'message': 'Friend request sent successfully.'}, status=status.HTTP_200_OK)