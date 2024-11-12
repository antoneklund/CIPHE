from django.contrib import admin
from .models import (
    Survey,
    User,
    Page,
    Cluster,
    Article,
    UFQuestion,
    LikertScaleQuestion,
    CharacteristicsQuestion,
    ArticleQuestion,
    TaxonomyQuestion,
)

admin.site.register(Survey)
admin.site.register(User)
admin.site.register(Page)
admin.site.register(Cluster)
admin.site.register(Article)
admin.site.register(UFQuestion)
admin.site.register(LikertScaleQuestion)
admin.site.register(CharacteristicsQuestion)
admin.site.register(ArticleQuestion)
admin.site.register(TaxonomyQuestion)
