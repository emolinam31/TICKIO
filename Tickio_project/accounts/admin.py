from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Asistente, Organizador

class AsistenteInline(admin.StackedInline):
    model = Asistente
    can_delete = False

class OrganizadorInline(admin.StackedInline):
    model = Organizador
    can_delete = False

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'tipo', 'is_staff', 'is_active')
    list_filter = ('tipo', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Información Personal', {'fields': ('nombre', 'first_name', 'last_name')}),
        ('Permisos', {'fields': ('tipo', 'is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'nombre', 'password1', 'password2', 'tipo', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'username', 'nombre')
    ordering = ('email',)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        if obj.tipo == 'asistente':
            return [AsistenteInline(self.model, self.admin_site)]
        return [OrganizadorInline(self.model, self.admin_site)]

class AsistenteAdmin(admin.ModelAdmin):
    list_display = ('get_email', 'get_nombre')
    search_fields = ('customuser__correo', 'customuser__nombre')

    def get_email(self, obj):
        return obj.customuser.email
    get_email.short_description = 'Correo Electrónico'

    def get_nombre(self, obj):
        return obj.customuser.nombre
    get_nombre.short_description = 'Nombre'

class OrganizadorAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'get_email', 'get_nombre')
    search_fields = ('empresa', 'customuser__email', 'customuser__nombre')

    def get_email(self, obj):
        return obj.customuser.correo
    get_email.short_description = 'Correo'

    def get_nombre(self, obj):
        return obj.customuser.nombre
    get_nombre.short_description = 'Nombre'

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Asistente, AsistenteAdmin)
admin.site.register(Organizador, OrganizadorAdmin)
