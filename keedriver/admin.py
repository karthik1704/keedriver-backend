from django.contrib import admin


class CustomAdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["foo"] = "bar"
        print(extra_context)
        return super().index(request, extra_context=extra_context)


admin_site = CustomAdminSite(name="myadmin")
