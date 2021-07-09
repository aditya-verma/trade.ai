from django.contrib import admin, messages
from django.utils.translation import ngettext


class TradeAIBaseAdmin(admin.ModelAdmin):
	"""Base Admin class for TradeAI admin pages.
	"""

	def undelete(self, request, queryset):
		updated = queryset.update(delete_flag=False)
		self.message_user(request, ngettext(
			'%d object was successfully restored.',
			'%d objects were successfully restored.',
			updated,
		) % updated, messages.SUCCESS)

	undelete.short_description = "Restore deleted objects"

	actions = ['undelete']

	def delete_model(self, request, obj):
		obj.delete_flag = True
		obj.save()
