from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from .models import User, Room, KeyCell, LogTable, Lesson
from .forms import UserAdminChangeForm, UserAdminCreationForm
from .models import DoorsUser


class DoorsUserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    actions = ['action_change_user', ]

    list_display = ("surname", "first_name", "last_name", 'email', 'phone_number', 'is_superuser', 'staff')
    list_filter = ()
    fieldsets = [
        ("ФИО", {"fields": ["surname", "first_name", "last_name"]}),
        ("Контактные данные", {"fields": ["phone_number", "email"]}),
        ("PIN-код", {"fields": ["pin_code"], "classes": ["collapse"]}),
        ("Пароль", {"fields": ["password"], "classes": ["collapse"]}),
        ("Система", {"fields": ["is_superuser", 'staff'], "classes": ["collapse"]})
    ]

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('surname',
                       'first_name',
                       'last_name',
                       'document_number',
                       'phone_number',
                       'pin_code',
                       'email',
                       'password1',
                       'password2',
                       'is_superuser',
                       'staff')
        }),
    )

    search_fields = ()
    ordering = ('surname', 'first_name', 'last_name')
    filter_horizontal = ()

    def action_change_user(modeladmin, request, queryset):
        user = queryset.first()
        return HttpResponseRedirect("%s%s/change" % (request.get_full_path(), user.id))
    action_change_user.short_description = 'Изменить выбранного пользователя'


# class UserAdmin(admin.ModelAdmin):
#     fieldsets = [
#         ("ФИО", {"fields": ["surname", "first_name", "last_name"]}),
#         ("Контактные данные", {"fields": ["phone_number", "email"]}),
#         ("PIN-код", {"fields": ["pin_code"], "classes": ["collapse"]})
#     ]


class RoomAdmin(admin.ModelAdmin):
    fields = [
        "number",
        "floor"
    ]


class KeyCellAdmin(admin.ModelAdmin):
    list_display = ("__str__", "has_key", 'get_user')

    def get_user(self, obj):
        return obj.user_who_get.__str__()

    get_user.short_description = "Кто взял ключ?"


class LogAdmin(admin.ModelAdmin):
    list_display = ("get_user", "get_room", "log_time", "event")

    def get_user(self, obj):
        return obj.user.__str__()

    get_user.short_description = "Пользователь"

    def get_room(self, obj):
        return obj.key_ceil.room.number

    get_room.short_description = "Кабинет"


class LessonAdmin(admin.ModelAdmin):
    list_display = ("__str__", "time_start", 'time_end', 'get_room', 'get_teacher')

    def get_room(self, obj):
        return obj.room.number

    get_room.short_description = "Кабинет"

    def get_teacher(self, obj):
        return obj.teacher

    get_teacher.short_description = 'Преподаватель'


admin.site.register(DoorsUser, admin_class=DoorsUserAdmin)
# admin.site.register(User, admin_class=UserAdmin)
admin.site.register(Room, admin_class=RoomAdmin)
admin.site.register(KeyCell, admin_class=KeyCellAdmin)
admin.site.register(LogTable, admin_class=LogAdmin)
admin.site.register(Lesson, admin_class=LessonAdmin)

admin.site.unregister(Group)
