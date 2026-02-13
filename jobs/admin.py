from django.contrib import admin
from .models import Job
from .forms import JobAdminForm
from django.urls import reverse
from django.utils.html import format_html

from .models import Notification

admin.site.site_header = "Car Service Administration"
admin.site.site_title = "Car Service Admin"
admin.site.index_title = "Welcome to Car Service Dashboard"

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    form = JobAdminForm

    list_display = (
        'appointment',
        'job_type',
        'scheduled_datetime',
        'mechanic',
        'status',
        'print_job_card',
    )

    list_filter = ('job_type', 'status', 'scheduled_datetime')
    search_fields = ('mechanic__username',)
    ordering = ('-id',)

    readonly_fields = ('created_by', 'created_at')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['appointment'].required = True
        return form

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def print_job_card(self, obj):
        if obj.status == 'COMPLETED':
            url = reverse("job_card_pdf", args=[obj.id])

            return format_html(
                '<a class="button" target="_blank" href="{}">Print PDF</a>',
                url
            )
        return "-"
    
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = ("user","appointment", "message", "is_read", "created_at")
    list_filter = ("is_read",)

    def appointment(self, obj):
        return obj.job.appointment if obj.job else "-"

    appointment.short_description = "Car Reg"

admin.site.site_header = "Evoto Car Service"
admin.site.site_title = "Evoto Car Service Admin"
admin.site.index_title = "Evoto Car Service Dashboard"


