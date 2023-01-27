import re

class User():

    @staticmethod
    def validate(email, password):
        """Validate that a user has an email and password."""
        if not email:
            return 400, 'Missing email'

        email_regex = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
        if not re.fullmatch(email_regex, email):
            return 400, 'Invalid email format'

        if not password:
            return 400, 'Missing password'

        return 200, None