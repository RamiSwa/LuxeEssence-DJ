from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import datetime, timedelta

class UserVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Include the user's primary key and activation status to generate the hash
        return f"{user.pk}{timestamp}{user.is_active}"

    def is_token_expired(self, token_creation_time, expiration_minutes=5):
        # Convert the token creation time from string to datetime
        token_time = datetime.fromtimestamp(token_creation_time)
        current_time = datetime.now()
        # Return True if the token is older than expiration_minutes
        return (current_time - token_time) > timedelta(minutes=expiration_minutes)

# Instantiate the generator for use
user_tokenizer_generate = UserVerificationTokenGenerator()
