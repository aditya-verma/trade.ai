import ast

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import authentication, exceptions

from trade_ai.accounts.services import is_valid_otp


UserModel = get_user_model()


class CSRFCheck(CsrfViewMiddleware):
	def _reject(self, request, reason):
		# Return the failure reason instead of an HttpResponse
		return reason


class UserAuthenticationBackend(ModelBackend):
	"""Custom Authentication Backend to allow multiple fields as Username, and
	allow Users to login via OTP."""
	def authenticate(self, request, username=None, password=None, *args, **kwargs):
		try:
			user_obj = UserModel.objects.get(
				Q(email=username) |
				Q(mobile_no=username)
			)
		except UserModel.DoesNotExist:
			return None

		if kwargs.pop('via_otp', False):
			if is_valid_otp(user_obj, password):
				update_last_login(None, user_obj)
				return user_obj
		else:
			if user_obj.check_password(password):
				update_last_login(None, user_obj)
				return user_obj

		return None


class UserJWTAuthenticationBackend(authentication.BaseAuthentication):
	"""Customer JWT Authentication backend to authorize User requests with
		JWT token.
	"""
	jwt_token_prefix = 'Rat'

	def authenticate(self, request, *args, **kwargs):
		try:
			auth_token = request.COOKIES['token'].encode()
		except KeyError:
			raise exceptions.AuthenticationFailed(
				detail='Authentication credentials were not provided.', code='401'
			)

		# if not len(auth_header) == 2:
		# 	raise exceptions.AuthenticationFailed('Invalid Header')
		#
		# if self.jwt_token_prefix.lower() != auth_header[0].lower().decode():
		# 	raise exceptions.AuthenticationFailed(
		# 		'Invalid Authentication token prefix'
		# 	)

		try:
			jwt_token = auth_token.decode()
		except UnicodeError:
			raise exceptions.AuthenticationFailed('Invalid Authentication token', 401)

		return self.authenticate_credentials(request, jwt_token)

	def authenticate_credentials(self, request, token):
		payload = jwt.utils.base64url_decode(
			token.split('.')[1]
		)

		try:
			dict_payload = ast.literal_eval(payload.decode())
		except (SyntaxError, ValueError, UnicodeError):
			raise exceptions.AuthenticationFailed('Invalid encoded Payload', 401)

		user_email = dict_payload.get('email')

		try:
			user_obj = UserModel.objects.get(email=user_email)

			jwt_token_django_secret = f'{user_obj.jwt_token_secret}{settings.SECRET_KEY}'

			jwt.decode(token, jwt_token_django_secret, algorithms=['HS256'])
		except UserModel.DoesNotExist:
			raise exceptions.AuthenticationFailed('Invalid User', 401)
		except jwt.exceptions.InvalidSignatureError:
			raise exceptions.AuthenticationFailed('Invalid token signature', 401)
		except jwt.exceptions.ExpiredSignatureError:
			raise exceptions.AuthenticationFailed('Token expired', 401)

		if not user_obj.is_active:
			return None, 'User account has been deactivated'

		self.enforce_csrf(request)
		return user_obj, None

	def enforce_csrf(self, request):
		"""
		Enforce CSRF validation
		"""
		check = CSRFCheck()
		# populates request.META['CSRF_COOKIE'], which is used in process_view()
		check.process_request(request)
		reason = check.process_view(request, None, (), {})
		if reason:
			# CSRF failed, bail with explicit error message
			raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)
