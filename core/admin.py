from django.contrib import admin
from .models import Project, Connection, Customer, Request


admin.site.index_title = 'Welcome to Campaign Service'


def regenerate_token(modeladmin, request, queryset):
    queryset.update(token=Project.generate_token())


regenerate_token.short_description = "Regenerate project token"


class CustomerAdmin(admin.TabularInline):
    model = Customer
    extra = 0
    readonly_fields = ('external_id', 'email', 'active_id',)

    # def has_add_permission(self, request, obj=None):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False


class ConnectionAdmin(admin.TabularInline):
    model = Connection
    extra = 0
    readonly_fields = ('active_id',)


class RequestAdmin(admin.ModelAdmin):
    model = Request
    list_display = ['project', 'category', 'email', 'datetime']
    readonly_fields = ('project', 'category', 'payload', 'datetime', 'email')


class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        ConnectionAdmin,
        CustomerAdmin
    ]
    search_fields = ['name', 'slug']
    list_display = ['name', 'slug', 'token']
    readonly_fields = ('slug', 'token')

    actions = [regenerate_token]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Request, RequestAdmin)
