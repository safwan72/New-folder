from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
	message = "Permission denied."

	def has_permission(self, request, view):
		return request.user.admin