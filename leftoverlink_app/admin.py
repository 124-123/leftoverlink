from django.contrib import admin
from .models import  CustomUser
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import NGOVerificationRequest

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'date_joined')


@admin.register(NGOVerificationRequest)
class NGOVerificationRequestAdmin(admin.ModelAdmin):
    list_display = ('ngo_name', 'user', 'registration_number', 'is_verified', 'submitted_at')
    list_filter = ('is_verified', 'submitted_at')
    search_fields = ('ngo_name', 'registration_number', 'user__username')

    readonly_fields = (
        'user', 'ngo_name', 'registration_number', 'date_of_registration',
        'address', 'contact_person', 'contact_email', 'contact_phone',
        'registration_certificate', 'certificate_80g', 'certificate_12a',
        'pan_card', 'aadhaar_card', 'annual_report', 'bank_statement',
        'submitted_at'
    )

    actions = ['approve_requests', 'reject_requests']

    def approve_requests(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f"{updated} NGO(s) approved successfully.")
    approve_requests.short_description = "Approve selected NGO requests"

    def reject_requests(self, request, queryset):
        updated = queryset.update(is_verified=False)
        self.message_user(request, f"{updated} NGO(s) rejected successfully.")
    reject_requests.short_description = "Reject selected NGO requests"

    def registration_certificate(self, obj):
        return self._file_link(obj.registration_certificate)

    def certificate_80g(self, obj):
        return self._file_link(obj.certificate_80g)

    def certificate_12a(self, obj):
        return self._file_link(obj.certificate_12a)

    def pan_card(self, obj):
        return self._file_link(obj.pan_card)

    def aadhaar_card(self, obj):
        return self._file_link(obj.aadhaar_card)

    def annual_report(self, obj):
        return self._file_link(obj.annual_report)

    def bank_statement(self, obj):
        return self._file_link(obj.bank_statement)

    def _file_link(self, file_field):
        if file_field:
            if file_field.url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                return format_html(f"<img src='{file_field.url}' width='120' style='border:1px solid #ccc;' />")
            return format_html(f"<a href='{file_field.url}' target='_blank'>View</a>")
        return "No file"
