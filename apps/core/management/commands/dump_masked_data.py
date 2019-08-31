from maskpostgresdata import BasePostgresDataMaskingCommand


class Command(BasePostgresDataMaskingCommand):
    """
    Commons Library data masking.

    As all user profiles are public, we default to standard user data masking.

    The only other secret are API auth tokens - which we replace.
    """

    def update_authtoken_token(self, queryset):
        # Can't use .save() - as key is a primary key
        for num, token in enumerate(queryset):
            queryset.filter(key=token.key).update(key='{:040d}'.format(num))
