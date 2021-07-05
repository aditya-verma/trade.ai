from rest_framework import exceptions, mixins, viewsets


class TradeAIBaseViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	def initial(self, request, *args, **kwargs):
		if not self._is_request_authorized(request):
			raise exceptions.PermissionDenied(detail='Unauthorized request')

		super().initial(request, *args, **kwargs)

	def _is_request_authorized(self, request, *args, **kwargs):
		"""Dummy logic to authenticate request source and authorize valid
		   requests.

		Args:
			request (object): Django WSGI request object.
		Returns:
			bool: Returns True, if APP-ID and API-SECRET-KEY are valid else
				  False.
		"""
		return True
