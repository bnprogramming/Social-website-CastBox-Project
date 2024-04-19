def make_activate(queryset):
    queryset.update(is_active=True)


def make_deactivate(queryset):
    queryset.update(is_active=False)


class ClassBaseAdmin:
    actions = (make_activate, make_deactivate)
