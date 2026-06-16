
from src.services.users.export_csv import export_users_csv
from src.services.users.import_csv import import_users_csv


class UserServices:
    export_users_csv = staticmethod(export_users_csv)
    import_users_csv = staticmethod(import_users_csv)


user_service = UserServices()
