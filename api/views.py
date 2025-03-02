import os
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import Tier, User, RequestType, Request, RequestImage
from api.serializers import TierSerializer, UserSerializer, RequestTypeSerializer, RequestSerializer, RequestImageSerializer
from api.utils import is_valid_email, is_valid_phone, format_phone, generate_unique_hash
import string

# Create your views here.
class Login(APIView):
    """
    Login User.
    """

    def post(self, request, format=None):
        username = request.data.get("username", "")
        password = request.data.get("password", "")

        if username == "" or password == "":
            return Response({"error_message": "Please Fill All Fields"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.prefetch_related("tier").get(username=username)
        except User.DoesNotExist:
            return Response({"error_message": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not check_password(password, user.password):
            return Response({"error_message": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateAccount(APIView):
    """
    Create User Account.
    """

    def post(self, request, format=None):
        username = request.data.get("username", "").strip()
        password = request.data.get("password", "").strip()
        email = request.data.get("email", "").strip()
        phone = request.data.get("phone", "").strip()

        if username == "" or password == "" or email == "" or phone == "":
            return Response({"error_message": "Please Fill All Fields"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate username
        for char in username:
            if char not in string.ascii_letters + string.digits + "_-":
                return Response({"error_message": "Invalid Username"}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(username) < 4:
            return Response({"error_message": "Username Too Short"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate password
        for char in password:
            if char == " ":
                return Response({"error_message": "Invalid Password"}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(password) < 4:
            return Response({"error_message": "Password Too Short"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not is_valid_email(email):
            return Response({"error_message": "Invalid Email"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not is_valid_phone(phone):
            return Response({"error_message": "Invalid Phone Number"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(username__iexact=username)
            return Response({"error_message": "Username Taken"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            pass
        
        hash = generate_unique_hash(User.objects.values_list("hash", flat=True))

        user = User.objects.create(username=username, password=make_password(password), email=email, phone=format_phone(phone), hash=hash, tier=Tier.objects.get(rank=1))
        user = User.objects.prefetch_related("tier").get(pk=user.pk)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RequestData(APIView):
    """
    Create and Get Requests.
    """

    def get(self, request, format=None):
        hash = request.query_params.get("hash", "").strip()

        if hash == "":
            return Response({"error_message": "Invalid User"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(hash=hash)
        except User.DoesNotExist:
            return Response({"error_message": "Invalid User"}, status=status.HTTP_400_BAD_REQUEST)
        
        requests = Request.objects.prefetch_related('user').prefetch_related('type').prefetch_related('images').filter(closed=None)

        serializer = RequestSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        hash = request.data.get("hash", "").strip()
        title = request.data.get("title", "").strip()
        description = request.data.get("description", "").strip()
        type = request.data.get("type", "") # 0 - Land, 1 - Plants
        email_contact = request.data.get("email_contact", "")
        phone_contact = request.data.get("phone_contact", "")
        images = request.data.get("images", "").strip() # URL-safe BASE64 images separated by * characters

        if hash == "" or title == "" or description == "" or type == "" or email_contact == "" or phone_contact == "":
            return Response({"error_message": "Please Fill All Fields"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(hash=hash)
        except User.DoesNotExist:
            return Response({"error_message": "Invalid User"}, status=status.HTTP_400_BAD_REQUEST)

        request = Request.objects.create(user=user, title=title, description=description, type=RequestType.objects.get(identification_number=type), email_contact=email_contact, phone_contact=phone_contact)

        image_list = images.split("*")

        for image in image_list:
            RequestImage.objects.create(request=request, image=image)
        
        request = Request.objects.prefetch_related('user').prefetch_related('type').prefetch_related('images').get(pk=request.pk)

        serializer = RequestSerializer(request)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetRequestData(APIView):
    """
    Get Requests.
    """

    def get(self, request, format=None):
        hash = request.query_params.get("hash", "").strip()
        id = request.query_params.get("id", "").strip()

        if hash == "" or id == "":
            return Response({"error_message": "Invalid User"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(hash=hash)
        except User.DoesNotExist:
            return Response({"error_message": "Invalid User"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            request = Request.objects.prefetch_related('user').prefetch_related('type').prefetch_related('images').get(id=id)
        except User.DoesNotExist:
            return Response({"error_message": "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RequestSerializer(request)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateRequestData(APIView):
    """
    Update Requests.
    """

    def post(self, request, format=None):
        hash = request.data.get("hash", "").strip()
        id = request.data.get("id", "")
        title = request.data.get("title", "").strip()
        description = request.data.get("description", "").strip()
        type = request.data.get("type", "") # 0 - Land, 1 - Plants
        email_contact = request.data.get("email_contact", "")
        phone_contact = request.data.get("phone_contact", "")
        images = request.data.get("images", "").strip() # URL-safe BASE64 images separated by * characters

        if hash == "" or id == "" or title == "" or description == "" or type == "" or email_contact == "" or phone_contact == "":
            return Response({"error_message": "Please Fill All Fields"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(hash=hash)
        except User.DoesNotExist:
            return Response({"error_message": "Invalid User"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            request = Request.objects.prefetch_related('user').prefetch_related('type').prefetch_related('images').get(id=id)
        except Request.DoesNotExist:
            return Response({"error_message": "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.username != request.user.username:
            return Response({"error_message": "Invalid User"}, status=status.HTTP_400_BAD_REQUEST)

        request.user = user
        request.title = title
        request.description = description
        request.type = RequestType.objects.get(identification_number=type)
        request.email_contact = email_contact
        request.phone_contact = phone_contact
        request.save()

        image_list = images.split("*")

        for image in image_list:
            RequestImage.objects.create(request=request, image=image)
        
        request = Request.objects.prefetch_related('user').prefetch_related('type').prefetch_related('images').get(pk=request.pk)

        serializer = RequestSerializer(request)
        return Response(serializer.data, status=status.HTTP_200_OK)

class HomeData(APIView):
    """
    Get Data Needed For Home Page.
    """

    def get(self, request, format=None):
        hash = request.query_params.get("hash", "").strip()

        if hash == "":
            return Response({"error_message": "Invalid User"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(hash=hash)
        except User.DoesNotExist:
            return Response({"error_message": "Invalid User"}, status=status.HTTP_400_BAD_REQUEST)
        
        requests = Request.objects.prefetch_related('user').prefetch_related('type').prefetch_related('images').all()

        serializer = RequestSerializer(requests.order_by("-created")[:5], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OpenAIData(APIView):
    """
    Get OpenAI key.
    """

    def get(self, request, format=None):
        hash = request.query_params.get("hash", "").strip()

        if hash == "":
            return Response({"error_message": "Invalid User"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(hash=hash)
        except User.DoesNotExist:
            return Response({"error_message": "Invalid User"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"key": os.environ.get("OPEN_AI_SECRET_KEY")}, status=status.HTTP_200_OK)

# @api_view(['POST'])
# def login(request):
#     """
#     Login user.
#     """
#     if request.method == 'GET':
#         all_requests = Request.objects.all()
#         serializer = RequestSerializer(all_requests, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = RequestSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def create_account(request):
#     """
#     Create user.
#     """

#     data = request.data.copy()
#     data["password"] = make_password(request.data["password"])
#     data["hash"] = generate_unique_hash(User.objects.values_list("hash", flat=True))

#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid() and is_valid_email(request.data["email"]) and is_valid_phone(request.data["email"]):
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'POST'])
# def requests(request):
#     """
#     List all requests, or create a new request.
#     """
#     if request.method == 'GET':
#         all_requests = Request.objects.all()
#         serializer = RequestSerializer(all_requests, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = RequestSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)