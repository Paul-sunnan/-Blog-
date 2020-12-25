from django.contrib import admin
from .models import EmailVeriRecord


class EmailAdmin(admin.ModelAdmin):
    list_display = ['code', 'email', 'send_time', 'email_type']
    search_fields = ['code', 'email']
    list_filter = ['send_time', 'exprie_time']


admin.site.register(EmailVeriRecord, EmailAdmin)
