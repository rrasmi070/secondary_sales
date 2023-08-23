from django.apps import AppConfig


class MasterConfig(AppConfig):
    name = 'master'


    def ready(self):
        from master import schedule
        print("Starting Scheduler ...")
        from master import surya_api_schdule
        surya_api_schdule.start()
        schedule.start()