class User():
    
    @staticmethod
    def validate(email, password):
        """Validate that a user has an email and password."""
        if not email:
            return 400, 'Missing email'

        if not password:
            return 400, 'Missing password'

        return 200, None