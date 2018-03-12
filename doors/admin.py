from django.contrib import admin
from .models import User, Room, KeyCell, LogTable


class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        ("ФИО", {"fields": ["surname", "first_name", "last_name"]}),
        ("Контактные данные", {"fields": ["phone_number", "email"]}),
        ("PIN-код", {"fields": ["pin_code"], "classes": ["collapse"]})
    ]


class RoomAdmin(admin.ModelAdmin):
    fields = [
        "number",
        "floor"
    ]


class KeyCellAdmin(admin.ModelAdmin):
    list_display = ("__str__", "has_key")


class LogAdmin(admin.ModelAdmin):
    list_display = ("get_user", "get_room", "log_time", "event")

    def get_user(self, obj):
        return obj.user.__str__()

    get_user.short_description = "Пользователь"

    def get_room(self, obj):
        return obj.key_ceil.room.number

    get_room.short_description = "Кабинет"


admin.site.register(User, admin_class=UserAdmin)
admin.site.register(Room, admin_class=RoomAdmin)
admin.site.register(KeyCell, admin_class=KeyCellAdmin)
admin.site.register(LogTable, admin_class=LogAdmin)
