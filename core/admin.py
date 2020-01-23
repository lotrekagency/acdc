from django.contrib import admin
from .models import Project, Connection, Customer, Request
from mailchimp.admin import ListAdmin as MailchimpListAdmin


admin.site.index_title = 'Welcome to Campaign Service'


def regenerate_token(modeladmin, request, queryset):
    queryset.filter(proj_type='AC').update(token=Project.generate_token())


regenerate_token.short_description = "Regenerate project token"


class CustomerAdmin(admin.TabularInline):
    model = Customer
    extra = 0
    readonly_fields = ('external_id', 'email', 'active_id',)


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
        MailchimpListAdmin
    ]
    search_fields = ['name', 'slug']
    list_display = ['name', 'slug', 'token', 'proj_type']
    readonly_fields = ('slug', 'token')

    actions = [regenerate_token, 'really_delete_selected']

    def get_actions(self, request):
        actions = super(ProjectAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def really_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()

        if queryset.count() == 1:
            message_bit = "1 project entry was"
        else:
            message_bit = "%s project entries were" % queryset.count()
        self.message_user(request, "%s successfully deleted." % message_bit)
    really_delete_selected.short_description = "Delete selected entries"

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProjectAdmin, self).get_form(request, obj, **kwargs)
        return form

    class Media:
        js = ('/static/admin/js/project_admin.js', )

admin.site.register(Project, ProjectAdmin)
admin.site.register(Request, RequestAdmin)
