from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, reverse
from django.views.generic.base import RedirectView

from users import views as users_views

from core.settings import env

if env("CAS_ENABLED"):
    import django_cas_ng.views
else:
    from django.contrib.auth import views as auth_views


if env("CAS_ENABLED"):
    urlpatterns = [
        # CAS authentication views.
        path("login/", django_cas_ng.views.LoginView.as_view(), name="login"),
        path("logout/", django_cas_ng.views.LogoutView.as_view(), name="logout"),
        path("callback/", django_cas_ng.views.CallbackView.as_view(), name="callback"),
    ]
else:
    urlpatterns = [
        # Local authentication views.
        path(
            "login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"
        ),
        path(
            "logout/",
            auth_views.LogoutView.as_view(template_name="users/logout.html"),
            name="logout",
        ),
    ]

# fmt: off
urlpatterns += [
    # Admin interface.
    path("admin/", admin.site.urls),

    # Profiles.
    path("profile/self/", users_views.self, name="self"),
    path("profile/<str:username>/", users_views.profile, name="profile"),

    # Checklists
    path('checklists/', include('checklists.urls', namespace="checklists")),

    # Templates
    path('templates/', include('templates.urls', namespace="templates")),

    # Homepage.
    path("", RedirectView.as_view(url="/checklists/"), name="home"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# fmt:on
