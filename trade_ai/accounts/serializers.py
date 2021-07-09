from trade_ai.accounts.models import User
from trade_ai.base.serializers import (TradeAIBaseModelSerializer)
from rest_framework.serializers import ValidationError


class UserSerializer(TradeAIBaseModelSerializer):
	class Meta:
		model = User
		exclude = ['password', 'jwt_token_secret']
		read_only_fields = ['email', 'mobile_no']
		extra_kwargs = {
			'password': {
				'write_only': True
			}
		}

	def update_password(self, request, raise_exception=False):
		user = request.user
		if user.check_password(request.data['old_password']):
			if request.data['new_password'] != request.data['old_password']:
				if request.data['new_password'] == request.data['confirm_password']:
					user.set_password(request.data['new_password'])
					user.save(update_fields=['password'])
					return True
				if raise_exception:
					raise ValidationError('new password and confirm password does not match')
				self.errors_ = {
					'new_password': 'new password and confirm password does not match',
					'confirm_password': 'new password and confirm password does not match'
				}
				return False
			self.errors_ = {
				'old_password': 'new password and old password are same',
				'new_password': 'new password and old password are same'
			}
			return False
		if raise_exception:
			raise ValidationError('old password do not match')
		self.errors_ = {'old_password': 'old password do not match'}
		return False


class UserReadOnlySerializer(TradeAIBaseModelSerializer):
	class Meta:
		model = User
		exclude = ['password', 'jwt_token_secret']
		read_only_fields = [field.name for field in model._meta.get_fields()]


class CreateAccountSerializer(TradeAIBaseModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'email', 'mobile_no', 'password']
		extra_kwargs = {
			'password': {
				'write_only': True
			}
		}

	def create(self, validated_data):
		user = User.objects.create(
			email=validated_data['email'],
			mobile_no=validated_data['mobile_no']
		)
		user.set_password(validated_data['password'])
		user.save()
		return user
