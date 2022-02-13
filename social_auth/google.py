from google.auth.transport import requests
from google.oauth2 import id_token


class Google:
    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the Google oAUTH2 api to fetch the user info
        """
        try:
            id_info = id_token.verify_oauth2_token(auth_token, requests.Request())

            if "accounts.google.com" in id_info["iss"]:
                return id_info

        except ValueError:
            raise ValueError("The token is either invalid or has expired")
