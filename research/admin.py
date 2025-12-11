from django.contrib import admin

# Register your models here.
from .models import ResearchProject, ResearchTopic, Source, ResearchNote, Keyword, ResearchMember

admin.site.register(ResearchProject)
admin.site.register(ResearchTopic)
admin.site.register(Source)
admin.site.register(ResearchNote)
admin.site.register(Keyword)
admin.site.register(ResearchMember)