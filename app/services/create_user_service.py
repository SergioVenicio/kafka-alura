from repository.user_repository import UserRepository


class CreateUserService:
    def __init__(self):
        self.repository = UserRepository()

    def create_user(self, user):
        self.repository.create_user(user)

    def get_user_by_email(self, email):
        return self.repository.get_user_by_email(email)