from django.apps import AppConfig


class OperationsConfig(AppConfig):
    name = 'operations'
    verbose_name = '用户操作管理'
    def ready(self):
        import operations.signals