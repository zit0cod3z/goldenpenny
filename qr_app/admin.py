from django.contrib import admin
from .models import Attendee, Child


@admin.action(description='Import Excel Data')
def import_excel_data(modeladmin, request, queryset):
    # Implementation for file upload and processing can go here
    pass

class AttendeeAdmin(admin.ModelAdmin):
    actions = [import_excel_data]
    list_display = ('name', 'email', 'ticket_type', 'get_children_list',)

    def get_children_list(self, obj):
        children = obj.children.all()  # Get related children
        if children.exists():
            return ", ".join(child.name for child in children)  # Join names with a comma
        return "No Children"  # Display this if no children

    get_children_list.short_description = 'Children'  # Column header name


class ChildAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_user_name',)  # Show child's name and associated user

    def get_user_name(self, obj):
        return obj.attendee.name if obj.attendee else "No Attendee"  # Get the user's name

    get_user_name.short_description = 'Attendee'  # Column header name


admin.site.register(Child, ChildAdmin)  # Register Child with custom admin

admin.site.register(Attendee, AttendeeAdmin)
