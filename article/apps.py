from django.apps import AppConfig

class ArticleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'article'

    def ready(self):
        from django.db.utils import OperationalError, ProgrammingError

        try:
            from .models import TechStack

            techs = ['Java', 'Python', 'PHP', 'Ruby', 'C++', 'HTML', 'CSS', 'JavaScript', 'React']

            for t in techs:
               TechStack.objects.get_or_create(name=t)

        except (OperationalError, ProgrammingError):
            pass