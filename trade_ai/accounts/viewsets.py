from datetime import datetime, timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from rest_framework.decorators import action

from trade_ai.accounts.models import User
from trade_ai.accounts.serializers import UserReadOnlySerializer, CreateAccountSerializer, UserSerializer
from trade_ai.base import viewsets, response
from trade_ai.accounts.backends import UserAuthenticationBackend


class UserViewSet(viewsets.TradeAIBaseViewSet):
	"""Viewset to perform CRUD operatios on User table.
	"""
	queryset = User.objects.all()
	serializer_class = UserReadOnlySerializer

	# permission_classes = [UserPermission, ]

	@action(methods=['POST'], detail=False, authentication_classes=[])
	def signup(self, request):
		serializer = CreateAccountSerializer(data=request.data)
		if not serializer.is_valid():
			return response.BadRequest(
				{
					"details": serializer.errors
				}
			)
		serializer.save()
		return response.Ok(
			{
				'data': serializer.data
			}
		)

	@action(methods=['GET', 'PATCH'], detail=True)
	def activate(self, request, pk=None):
		if request.user.is_staff or request.user.is_superuser:
			user = User.objects.get(pk=pk)
			if user:
				if user.is_active:
					return response.BadRequest(
						{
							'detail': 'User already activated'
						}
					)
				user.is_active = True
				user.save(update_fields=['is_active'])
				return response.Ok(
					{
						'data': 'The user id ' + str(user.id) + ' has been activated'
					}
				)
			return response.NotFound(
				{
					'detail': "User not found"
				}
			)
		return response.Forbidden(
			{
				'detail': 'Permission denied'
			}
		)

	@action(methods=['GET', 'PATCH'], detail=True)
	def deactivate(self, request, pk=None):
		if request.user.is_staff or request.user.is_superuser:
			user = User.objects.get(pk=pk)
			if user and user.is_active:
				user.is_active = False
				user.save(update_fields=['is_active'])
				return response.Ok(
					{
						'data': 'The user id ' + str(user.id) + ' has been deactivated'
					}
				)
			return response.NotFound(
				{
					'detail': "User not found or account has been deactivated."
				}
			)
		return response.Forbidden(
			{
				'detail': 'Permission denied'
			}
		)

	@action(methods=['POST'], detail=False, authentication_classes=[])
	@method_decorator(ensure_csrf_cookie)
	def login(self, request):
		"""
		Login using email and password
		"""
		authentication_backend = UserAuthenticationBackend()
		user = authentication_backend.authenticate(
			request=request,
			username=request.data['username'],
			password=request.data['password'])
		try:
			jwt_token = user.fetch_jwt_token()
			responseWithCookie = response.Ok(
				{
					'token': jwt_token
				}
			)
			responseWithCookie.set_cookie(
				'token',
				value=jwt_token,
				samesite='Strict',
				httponly=True,
				max_age=int(
					(
						datetime.now() + timedelta(
								days=settings.JWT_TOKEN_VALIDITY_DAYS
							)
						).timestamp()
					)
				)
			return responseWithCookie
		except AttributeError:
			return response.NotFound(
				{
					'detail': 'Incorrect Username or password'
				}
			)

	@action(methods=['POST'], detail=False, authentication_classes=[])
	@method_decorator(ensure_csrf_cookie)
	def verifyOTP(self, request):
		"""
		Login using email and password
		"""
		authentication_backend = UserAuthenticationBackend()
		user = authentication_backend.authenticate(
			request=request,
			username=request.data['username'],
			password=request.data['otp'],
			via_otp=True
		)
		try:
			jwt_token = user.fetch_jwt_token()
			response_with_cookie = response.Ok(
				{
					'token': jwt_token
				}
			)
			response_with_cookie.set_cookie(
				'token',
				value=jwt_token,
				samesite='Strict',
				httponly=True,
				secure=not settings.DEBUG,
				max_age=int(
						(
							datetime.now() + timedelta(
								days=settings.JWT_TOKEN_VALIDITY_DAYS
							)
						).timestamp()
					)
				)
			return response_with_cookie
		except AttributeError:
			return response.NotFound(
				{
					'detail': 'Incorrect Username or password'
				}
			)

	@action(methods=['GET'], detail=False)
	def logout_all(self, request):
		"""
		The user will be logged out by refreshing the token
		"""
		user = request.user
		user.refresh_jwt_token()
		return response.Ok(
			{
				'data': 'success'
			}
		)

	@action(methods=['GET'], detail=False)
	def logout(self, request):
		"""
		The user will be logged out by deleting the token
		"""
		response_with_cookie = response.Ok(
			{
				'data': 'success'
			}
		)
		response_with_cookie.set_cookie(
			key='token',
			value='',
			samesite='Strict',
			httponly=True,
			secure=not settings.DEBUG)
		return response_with_cookie

	@action(methods=['POST'], detail=True)
	def authorize(self, request, pk=None):
		return response.Ok(
			{
				'response': True
			}
		)

	@action(methods=['GET'], detail=True)
	def read_profile(self, request, pk=None):
		user = User.objects.get(pk=pk)
		if not user:
			return response.NotFound(
				{
					'detail': 'user not found'
				}
			)
		if user.id == request.user.id:
			user_serializer = UserSerializer(user)
			return response.Ok(
				{
					'data': user_serializer.data
				}
			)
		else:
			return response.Forbidden(
				{
					'detail': 'Permission denied'
				}
			)

	@action(methods=['PATCH'], detail=True)
	def edit_profile(self, request, pk=None):
		serializer = UserSerializer(request.user, data=request.data, partial=True)
		if not serializer.is_valid():
			return response.BadRequest(
				{
					'detail': serializer.errors
				}
			)
		serializer.save()
		return response.Ok(
			{
				'data': serializer.data
			}
		)

	@action(methods=['PATCH'], detail=False)
	def update_password(self, request):
		user = request.user
		user_serializer = UserSerializer(user)

		if user_serializer.update_password(request):
			return response.Ok(
				{
					'data': 'success'
				}
			)
		return response.BadRequest(
			{
				'detail': user_serializer.errors_
			}
		)


# Me ViewSet
class MeViewSet(viewsets.TradeAIBaseViewSet):
	"""Viewset to perform CRUD operatios on User table.
	"""
	queryset = User.objects.all()
	serializer_class = UserReadOnlySerializer

	# permission_classes = [UserPermission, ]

	@action(methods=['GET', 'PATCH'], detail=False)
	def deactivate(self, request):
		user = request.user
		if user and user.is_active:
			user.is_active = False
			user.save(update_fields=['is_active'])
			return response.Ok(
				{
					'data': 'The user id ' + str(user.id) + ' has been deactivated'
				}
			)
		return response.NotFound(
			{
				'detail': "User not found or account has been deactivated."
			}
		)

	@action(methods=['GET'], detail=False)
	def read_profile(self, request):
		if request.user.is_authenticated:
			user_serializer = UserSerializer(request.user)
			return response.Ok(
				{
					'data': user_serializer.data
				}
			)
		else:
			return response.Forbidden(
				{
					'detail': 'Permission denied'
				}
			)

	@action(methods=['PATCH'], detail=False)
	def edit_profile(self, request):
		if not request.user.is_authenticated:
			return response.Forbidden(
				{
					'detail': 'Permission denied'
				}
			)
		serializer = UserSerializer(request.user, data=request.data, partial=True)
		if not serializer.is_valid():
			return response.BadRequest(
				{
					'detail': serializer.errors
				}
			)
		serializer.save()
		return response.Ok(
			{
				'data': serializer.data
			}
		)

	@action(methods=['PATCH'], detail=False)
	def update_password(self, request):
		user = request.user
		user_serializer = UserSerializer(user)

		if user_serializer.update_password(request):
			return response.Ok(
				{
					'data': 'new password updated'
				}
			)
		return response.BadRequest(
			{
				'detail': user_serializer.errors_
			}
		)
