from django.contrib import admin

from alias.models import Alias


class AliasAdmin(admin.ModelAdmin):
    list_display = ('id', 'alias', 'target')


admin.site.register(Alias, AliasAdmin)
