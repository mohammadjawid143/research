from django import forms
from django.forms import ModelForm
from .models import (
    ResearchProject,
    ResearchTopic,
    Source,
    ResearchNote,
    Keyword,
    ResearchMember
)

# 🔹 فرم پروژه تحقیقاتی
class ResearchProjectForm(ModelForm):
    class Meta:
        model = ResearchProject
        fields = ['title', 'description']
        labels = {
            'title': 'عنوان پروژه',
            'description': 'توضیحات پروژه',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثلاً بررسی تاثیر تکنولوژی در آموزش'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# 🔹 فرم موضوع تحقیق
class ResearchTopicForm(ModelForm):
    class Meta:
        model = ResearchTopic
        fields = ['project', 'title', 'description']
        labels = {
            'project': 'پروژه',
            'title': 'عنوان موضوع',
            'description': 'توضیحات',
        }
        widgets = {
            'project': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثلاً نقش هوش مصنوعی در آموزش'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# 🔹 فرم منبع تحقیق
class SourceForm(ModelForm):
    class Meta:
        model = Source
        fields = ['title', 'author', 'source_type', 'publish_year']
        labels = {
            'title': 'عنوان منبع',
            'author': 'نویسنده / پدیدآور',
            'source_type': 'نوع منبع',
            'publish_year': 'سال انتشار',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'source_type': forms.Select(attrs={'class': 'form-select'}),
            'publish_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثلاً 1403'}),
        }


# 🔹 فرم فیش تحقیقاتی
class ResearchNoteForm(forms.ModelForm):
    keywords = forms.ModelMultipleChoiceField(
        queryset=Keyword.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="کلیدواژه‌ها"
    )

    class Meta:
        model = ResearchNote
        fields = ['topic', 'source', 'title', 'content', 'note_type', 'status', 'keywords']
        labels = {
            'topic': 'موضوع تحقیق',
            'source': 'منبع',
            'title': 'عنوان فیش',
            'content': 'متن فیش',
            'note_type': 'نوع فیش',
            'status': 'وضعیت',
        }
        widgets = {
            'topic': forms.Select(attrs={'class': 'form-select'}),
            'source': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'note_type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


# 🔹 فرم کلیدواژه
class KeywordForm(ModelForm):
    class Meta:
        model = Keyword
        fields = ['name']
        labels = {'name': 'کلیدواژه'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثلاً هوش مصنوعی'}),
        }


# 🔹 فرم اعضای پروژه
class ResearchMemberForm(ModelForm):
    class Meta:
        model = ResearchMember
        fields = ['project', 'user', 'role']
        labels = {
            'project': 'پروژه',
            'user': 'کاربر',
            'role': 'نقش',
        }
        widgets = {
            'project': forms.Select(attrs={'class': 'form-select'}),
            'user': forms.Select(attrs={'class': 'form-select'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'پژوهشگر، نویسنده، ویراستار...'}),
        }
