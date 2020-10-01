try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from admin_tools.menu import Menu, items
from django.utils.translation import ugettext_lazy as _


class AdminMenu(Menu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.children += [
            items.MenuItem(_("Dashboard"), reverse("admin:index")),
            items.Bookmarks(),
            items.AppList(_("Site Management")),
        ]
