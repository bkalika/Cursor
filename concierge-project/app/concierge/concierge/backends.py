from django.contrib.auth.backends import ModelBackend

class MyBackend(ModelBackend):
    def authenticate(self, request, **creds):
        # Check the username/password and return a user.
        print(creds)
        return super().authenticate(request, **creds)
