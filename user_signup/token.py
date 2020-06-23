from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from rest_framework_simplejwt.tokens import RefreshToken


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                text_type(user.pk) + text_type(timestamp) + text_type(user.is_active) + text_type(user.password)
        )


account_activation_token = TokenGenerator()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
