from django.apps import AppConfig



class BranchUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'branch_user'

    def ready(self):
        from branch_user import freez
        from branch_user import archive_schedule
        from branch_user import schedule
        print("Starting Scheduler ...")
        schedule.start()
        archive_schedule.start()
        freez.start()
