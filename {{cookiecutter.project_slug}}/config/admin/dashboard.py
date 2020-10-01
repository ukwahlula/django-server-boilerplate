from admin_tools.dashboard import AppIndexDashboard, Dashboard, modules
from django.utils.translation import ugettext_lazy as _


class AdminDashboard(Dashboard):
    def init_with_context(self, context):
        self.children.append(
            modules.Group(
                _("Site management"),
                column=1,
                children=(
                    modules.ModelList(
                        _("User Management"),
                        column=1,
                        models=(
                            "apps.users.models.*",
                            "django.contrib.auth.models.*",
                            "rest_framework.authtoken.models.*",
                        ),
                    ),
                    modules.ModelList(_("Emails"), column=1, models=("apps.email.models.*",)),
                    modules.ModelList(_("Storage"), column=1, models=("apps.storage.models.*",)),
                ),
            )
        )

        self.children.append(modules.RecentActions(_("Recent Actions"), 5, column=2))


class AdminAppIndexDashboard(AppIndexDashboard):
    # we disable title because its redundant with the model list module
    title = ""

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(_("Recent Actions"), include_list=self.get_app_content_types(), limit=5),
        ]
