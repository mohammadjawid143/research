from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    KeywordForm,
    ResearchMemberForm,
    ResearchNoteForm,
    ResearchProjectForm,
    ResearchTopicForm,
    SourceForm,
)
from .models import Keyword, ResearchMember, ResearchNote, ResearchProject, ResearchTopic, Source

User = get_user_model()


def home(request):
    return render(request, "home.html")


# -------------------- پروژه‌ها --------------------
@login_required
def project_list(request):
    projects = ResearchProject.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "research/project_list.html", {"projects": projects})


@login_required
def project_create(request):
    form = ResearchProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        project = form.save(commit=False)
        project.user = request.user
        project.save()
        messages.success(request, "پروژه با موفقیت ثبت شد.")
        return redirect("project_list")
    return render(request, "research/project_form.html", {"form": form})


@login_required
def project_update(request, pk):
    project = get_object_or_404(ResearchProject, pk=pk, user=request.user)
    form = ResearchProjectForm(request.POST or None, instance=project)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "پروژه با موفقیت ویرایش شد.")
        return redirect("project_list")
    return render(request, "research/project_form.html", {"form": form, "project": project})


@login_required
def project_delete(request, pk):
    project = get_object_or_404(ResearchProject, pk=pk, user=request.user)
    if request.method == "POST":
        project.delete()
        messages.success(request, "پروژه حذف شد.")
        return redirect("project_list")
    return render(request, "research/confirm_delete.html", {"object": project})


# -------------------- موضوعات --------------------
@login_required
def topic_list(request):
    topics = (
        ResearchTopic.objects.filter(project__user=request.user)
        .select_related("project")
        .order_by("-created_at")
    )
    return render(request, "research/topic_list.html", {"topics": topics})


@login_required
def topic_create(request):
    form = ResearchTopicForm(request.POST or None)
    form.fields["project"].queryset = ResearchProject.objects.filter(user=request.user)

    if request.method == "POST" and form.is_valid():
        topic = form.save(commit=False)
        if topic.project.user != request.user:
            form.add_error("project", "دسترسی به این پروژه مجاز نیست.")
            messages.error(request, "دسترسی به این پروژه مجاز نیست.")
        else:
            topic.save()
            messages.success(request, "موضوع با موفقیت ثبت شد.")
            return redirect("topic_list")

    return render(request, "research/topic_form.html", {"form": form})


@login_required
def topic_update(request, pk):
    topic = get_object_or_404(ResearchTopic, pk=pk, project__user=request.user)
    form = ResearchTopicForm(request.POST or None, instance=topic)
    form.fields["project"].queryset = ResearchProject.objects.filter(user=request.user)

    if request.method == "POST" and form.is_valid():
        updated_topic = form.save(commit=False)
        if updated_topic.project.user != request.user:
            form.add_error("project", "دسترسی به این پروژه مجاز نیست.")
            messages.error(request, "دسترسی به این پروژه مجاز نیست.")
        else:
            updated_topic.save()
            messages.success(request, "موضوع با موفقیت ویرایش شد.")
            return redirect("topic_list")

    return render(request, "research/topic_form.html", {"form": form, "topic": topic})


@login_required
def topic_delete(request, pk):
    topic = get_object_or_404(ResearchTopic, pk=pk, project__user=request.user)
    if request.method == "POST":
        topic.delete()
        messages.success(request, "موضوع حذف شد.")
        return redirect("topic_list")
    return render(request, "research/confirm_delete.html", {"object": topic})


# -------------------- فیش‌ها --------------------
@login_required
def note_list(request):
    notes = (
        ResearchNote.objects.filter(user=request.user)
        .select_related("topic", "source")
        .prefetch_related("keywords")
        .order_by("-created_at")
    )
    return render(request, "research/note_list.html", {"notes": notes})


@login_required
def note_create(request):
    form = ResearchNoteForm(request.POST or None)
    form.fields["topic"].queryset = ResearchTopic.objects.filter(project__user=request.user)

    if request.method == "POST" and form.is_valid():
        note = form.save(commit=False)
        if note.topic.project.user != request.user:
            form.add_error("topic", "دسترسی به این موضوع تحقیق مجاز نیست.")
            messages.error(request, "دسترسی به این موضوع تحقیق مجاز نیست.")
        else:
            note.user = request.user
            note.save()
            form.save_m2m()
            messages.success(request, "فیش با موفقیت ثبت شد.")
            return redirect("note_list")

    return render(request, "research/note_form.html", {"form": form})


@login_required
def note_update(request, pk):
    note = get_object_or_404(ResearchNote, pk=pk, user=request.user)
    form = ResearchNoteForm(request.POST or None, instance=note)
    form.fields["topic"].queryset = ResearchTopic.objects.filter(project__user=request.user)

    if request.method == "POST" and form.is_valid():
        updated_note = form.save(commit=False)
        if updated_note.topic.project.user != request.user:
            form.add_error("topic", "دسترسی به این موضوع تحقیق مجاز نیست.")
            messages.error(request, "دسترسی به این موضوع تحقیق مجاز نیست.")
        else:
            updated_note.user = request.user
            updated_note.save()
            form.save_m2m()
            messages.success(request, "فیش با موفقیت ویرایش شد.")
            return redirect("note_list")

    return render(request, "research/note_form.html", {"form": form, "note": note})


@login_required
def note_delete(request, pk):
    note = get_object_or_404(ResearchNote, pk=pk, user=request.user)
    if request.method == "POST":
        note.delete()
        messages.success(request, "فیش حذف شد.")
        return redirect("note_list")
    return render(request, "research/confirm_delete.html", {"object": note})


# -------------------- منابع --------------------
@login_required
def source_list(request):
    sources = Source.objects.all().order_by("-id")
    return render(request, "research/source_list.html", {"sources": sources})


@login_required
def source_create(request):
    form = SourceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "منبع با موفقیت ثبت شد.")
        return redirect("source_list")
    return render(request, "research/source_form.html", {"form": form})


@login_required
def source_update(request, pk):
    source = get_object_or_404(Source, pk=pk)
    form = SourceForm(request.POST or None, instance=source)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "منبع با موفقیت ویرایش شد.")
        return redirect("source_list")
    return render(request, "research/source_form.html", {"form": form, "source": source})


@login_required
def source_delete(request, pk):
    source = get_object_or_404(Source, pk=pk)
    if request.method == "POST":
        source.delete()
        messages.success(request, "منبع حذف شد.")
        return redirect("source_list")
    return render(request, "research/confirm_delete.html", {"object": source})


# -------------------- کلیدواژه‌ها --------------------
@login_required
def keyword_list(request):
    keywords = Keyword.objects.all().order_by("name")
    return render(request, "research/keyword_list.html", {"keywords": keywords})


@login_required
def keyword_create(request):
    form = KeywordForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "کلیدواژه با موفقیت ثبت شد.")
        return redirect("keyword_list")
    return render(request, "research/keyword_form.html", {"form": form})


@login_required
def keyword_update(request, pk):
    keyword = get_object_or_404(Keyword, pk=pk)
    form = KeywordForm(request.POST or None, instance=keyword)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "کلیدواژه با موفقیت ویرایش شد.")
        return redirect("keyword_list")
    return render(request, "research/keyword_form.html", {"form": form, "keyword": keyword})


@login_required
def keyword_delete(request, pk):
    keyword = get_object_or_404(Keyword, pk=pk)
    if request.method == "POST":
        keyword.delete()
        messages.success(request, "کلیدواژه حذف شد.")
        return redirect("keyword_list")
    return render(request, "research/keyword_confirm_delete.html", {"keyword": keyword})


# -------------------- اعضای پروژه --------------------
@login_required
def member_list(request):
    members = (
        ResearchMember.objects.filter(project__user=request.user)
        .select_related("project", "user")
        .order_by("-joined_at")
    )
    return render(request, "research/member_list.html", {"members": members})


@login_required
def member_create(request):
    form = ResearchMemberForm(request.POST or None)
    form.fields["project"].queryset = ResearchProject.objects.filter(user=request.user)
    form.fields["user"].queryset = User.objects.all().order_by("username")

    if request.method == "POST" and form.is_valid():
        member = form.save(commit=False)
        if member.project.user != request.user:
            form.add_error("project", "دسترسی به این پروژه مجاز نیست.")
            messages.error(request, "دسترسی به این پروژه مجاز نیست.")
        else:
            member.save()
            messages.success(request, "عضو جدید ثبت شد.")
            return redirect("member_list")

    return render(request, "research/member_form.html", {"form": form})


@login_required
def member_update(request, pk):
    member = get_object_or_404(ResearchMember, pk=pk, project__user=request.user)
    form = ResearchMemberForm(request.POST or None, instance=member)
    form.fields["project"].queryset = ResearchProject.objects.filter(user=request.user)
    form.fields["user"].queryset = User.objects.all().order_by("username")

    if request.method == "POST" and form.is_valid():
        updated_member = form.save(commit=False)
        if updated_member.project.user != request.user:
            form.add_error("project", "دسترسی به این پروژه مجاز نیست.")
            messages.error(request, "دسترسی به این پروژه مجاز نیست.")
        else:
            updated_member.save()
            messages.success(request, "اطلاعات عضو ویرایش شد.")
            return redirect("member_list")

    return render(request, "research/member_form.html", {"form": form, "member": member})


@login_required
def member_delete(request, pk):
    member = get_object_or_404(ResearchMember, pk=pk, project__user=request.user)
    if request.method == "POST":
        member.delete()
        messages.success(request, "عضو حذف شد.")
        return redirect("member_list")
    return render(request, "research/confirm_delete.html", {"object": member})
