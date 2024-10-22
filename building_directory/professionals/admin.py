from django.contrib import admin
from .models import Professional, Portfolio, Review, Contract

@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "phone",
        "city",
        "commune",
        "specialization",
        "skill_level",
        "years_of_experience",
        "daily_rate",
        "availability",
        "identity_verified",
        "average_rating",
        "is_available",
    )
    search_fields = ("full_name", "email", "phone", "city", "commune", "specialization")
    list_filter = (
        "city",
        "commune",
        "specialization",
        "skill_level",
        "identity_verified",
        "years_of_experience",
    )
    ordering = ("full_name",)
    readonly_fields = ("average_rating", "is_available")

    def is_available(self, obj):
        return obj.is_available()
    is_available.boolean = True
    is_available.short_description = "Available"

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ("project_title", "professional", "project_description")
    search_fields = ("project_title", "professional__full_name", "project_description")
    list_filter = ("professional",)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('professional', 'user', 'rating', 'comment', 'created_at', 'updated_at')
    search_fields = ('comment', 'professional__full_name', 'user__username')
    list_filter = ('rating', 'created_at', 'professional')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "professional",
        "start_date",
        "end_date",
        "status",
        "payment_status",
        "is_current",
        "can_be_reviewed",
    )
    search_fields = ("user__username", "professional__full_name", "description")
    list_filter = ("status", "payment_status", "professional", "start_date", "end_date")
    ordering = ("-start_date",)
    readonly_fields = ("created_at", "completed_at", "is_current", "can_be_reviewed")

    def is_current(self, obj):
        return obj.is_current
    is_current.boolean = True
    is_current.short_description = "Current"

    def can_be_reviewed(self, obj):
        return obj.can_be_reviewed
    can_be_reviewed.boolean = True
    can_be_reviewed.short_description = "Can be reviewed"

    actions = ['mark_as_completed']

    def mark_as_completed(self, request, queryset):
        for contract in queryset:
            contract.mark_as_completed()
        self.message_user(request, f"{queryset.count()} contract(s) marked as completed.")
    mark_as_completed.short_description = "Mark selected contracts as completed"