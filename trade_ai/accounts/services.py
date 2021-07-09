from django.conf import settings


def is_valid_otp(user_obj, otp=''):
	"""Dummy OTP validation logic, definition will be updated later.

	Args:
		user_obj (object): Object of User model class.
		otp (str): String object entered by end User.

	Returns:
		bool: Returns True, if OTP is valid for given User else False.
	"""
	if not user_obj or not otp:
		return False

	if settings.DEBUG:
		if otp == '6666':
			return True

	return False
