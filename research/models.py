from django.db import models
from django.conf import settings

# 🔹 پروژه‌ی تحقیقاتی
class ResearchProject(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="projects", verbose_name="مدیر پروژه")
    title = models.CharField(max_length=200, verbose_name="عنوان پروژه")
    description = models.TextField(blank=True, verbose_name="توضیحات پروژه")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "پروژه تحقیقاتی"
        verbose_name_plural = "پروژه‌های تحقیقاتی"


# 🔹 موضوع تحقیق (زیرمجموعه‌ی یک پروژه)
class ResearchTopic(models.Model):
    project = models.ForeignKey(ResearchProject, on_delete=models.CASCADE, related_name="topics", verbose_name="پروژه")
    title = models.CharField(max_length=200, verbose_name="عنوان موضوع")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return f"{self.title} ({self.project.title})"

    class Meta:
        verbose_name = "موضوع تحقیق"
        verbose_name_plural = "موضوعات تحقیق"


# 🔹 منبع تحقیق (کتاب، مقاله، سایت و...)
class Source(models.Model):
    SOURCE_TYPES = [
        ('book', 'کتاب'),
        ('article', 'مقاله'),
        ('website', 'وب‌سایت'),
        ('other', 'سایر'),
    ]

    title = models.CharField(max_length=200, verbose_name="عنوان منبع")
    author = models.CharField(max_length=100, blank=True, verbose_name="نویسنده / پدیدآور")
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES, default='book', verbose_name="نوع منبع")
    publish_year = models.CharField(max_length=10, blank=True, verbose_name="سال انتشار")

    def __str__(self):
        return f"{self.title} ({self.get_source_type_display()})"

    class Meta:
        verbose_name = "منبع تحقیق"
        verbose_name_plural = "منابع تحقیق"


# 🔹 فیش تحقیقاتی
class ResearchNote(models.Model):
    NOTE_TYPES = [
        ('quote', 'نقل قول'),
        ('summary', 'خلاصه'),
        ('idea', 'یادداشت شخصی'),
    ]

    STATUS_CHOICES = [
        ('draft', 'پیش‌نویس'),
        ('final', 'نهایی'),
    ]

    topic = models.ForeignKey(ResearchTopic, on_delete=models.CASCADE, related_name="notes", verbose_name="موضوع")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="کاربر")
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="منبع")
    title = models.CharField(max_length=200, verbose_name="عنوان فیش")
    content = models.TextField(verbose_name="متن فیش")
    note_type = models.CharField(max_length=20, choices=NOTE_TYPES, default='summary', verbose_name="نوع فیش")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="وضعیت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")

    def __str__(self):
        return f"{self.title} ({self.topic.title})"

    class Meta:
        verbose_name = "فیش تحقیقاتی"
        verbose_name_plural = "فیش‌های تحقیقاتی"


# 🔹 برچسب‌ها یا کلیدواژه‌ها برای فیش‌ها
class Keyword(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="کلیدواژه")
    notes = models.ManyToManyField(ResearchNote, related_name="keywords", blank=True, verbose_name="فیش‌ها")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "کلیدواژه"
        verbose_name_plural = "کلیدواژه‌ها"


# 🔹 اعضای همکار در پروژه
class ResearchMember(models.Model):
    project = models.ForeignKey(ResearchProject, on_delete=models.CASCADE, related_name="members", verbose_name="پروژه")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="کاربر")
    role = models.CharField(max_length=50, verbose_name="نقش (مثلاً پژوهشگر، ویراستار،...)")
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ عضویت")

    def __str__(self):
        return f"{self.user.username} در {self.project.title}"

    class Meta:
        verbose_name = "عضو پژوهشی"
        verbose_name_plural = "اعضای پژوهشی"
