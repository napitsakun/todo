from django.template import Library

register = Library()

@register.filter('space_to_underscore')
def convert_space_to_underscore(obj):
	return obj.replace(' ', '_')
