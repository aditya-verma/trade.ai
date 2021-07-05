from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, ContentType, DELETION
from django.utils.translation import gettext as _


class LoggingMethodMixin:
    """
    Adds methods that log changes made to users' data.
    To use this, subclass it and ModelViewSet, and override _get_logging_user(). Ensure
    that the viewset you're mixing this into has `self.model` and `self.serializer_class`
    attributes.
    """

    def _get_logging_user(self):
        """Return the user of this logged item. Needs overriding in any subclass."""
        raise NotImplementedError

    def extra_data(self, data):
        """Hook to append more data."""
        return {}

    def log(self, operation, instance, message=None):
        if operation == ADDITION:
            action_message = _('Added.')
        if operation == CHANGE:
            action_message = _('Updated')
        if operation == DELETION:
            action_message = _('Deleted')
        if message:
            change_message = 'Changed ' + message
        else:
            change_message = action_message + ' ' + str(instance)
        LogEntry.objects.log_action(
            user_id=self.request.user.id,
            content_type_id=ContentType.objects.get_for_model(instance).pk,
            object_id=instance.pk,
            object_repr=str(instance),
            action_flag=operation,
            change_message=change_message)

    def _log_on_create(self, serializer):
        """Log the up-to-date serializer.data."""
        self.log(operation=ADDITION, instance=serializer.instance)

    def _log_on_update(self, serializer, message=None):
        """Log data from the updated serializer instance."""
        self.log(operation=CHANGE, instance=serializer.instance, message=message)

    def _log_on_destroy(self, instance):
        """Log data from the instance before it gets deleted."""
        self.log(operation=DELETION, instance=instance)
