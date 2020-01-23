from django.contrib import admin
from .models import List
from .forms import ListForm

# Register your models here.
class ListAdmin(admin.TabularInline):
    model = List
    min_num = 1
    max_num = 1
    verbose_name = 'Audience'
    verbose_name_plural = 'Audience'
    can_delete = False
    form = ListForm