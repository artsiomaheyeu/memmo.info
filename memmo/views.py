from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.http import urlencode

from .forms import MemoForm
from .models import Memo
from .utils import generate_stable_id, compute_content_hash, make_qr_base64

# Главная: ввод текста
def home(request):
    if request.method == "POST":
        form = MemoForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"].strip()
            if not text:
                return render(request, "home.html", {"form": form, "error": "Текст пустой."})

            memo_id = generate_stable_id()
            memo = Memo.objects.create(
                id=memo_id,
                text=text,
                content_hash=compute_content_hash(text),
            )
            return redirect("saved", memo_id=memo.id)
    else:
        form = MemoForm()
    return render(request, "home.html", {"form": form})

# Страница после сохранения: /<id>
def saved(request, memo_id: str):
    memo = get_object_or_404(Memo, pk=memo_id)
    if memo.is_deleted:
        raise Http404("Deleted")

    read_url = request.build_absolute_uri(reverse("read", args=[memo_id]))
    qr_b64 = make_qr_base64(read_url)
    return render(request, "saved.html", {
        "memo": memo,
        "read_url": read_url,
        "qr_b64": qr_b64,
    })

# Страница чтения: /<id>/r
def read(request, memo_id: str):
    memo = get_object_or_404(Memo, pk=memo_id)

    # kill → мягкое удаление
    if "kill" in request.GET:
        memo.is_deleted = True
        memo.save(update_fields=["is_deleted", "updated_at"])
        return render(request, "read.html", {
            "memo": memo,
            "deleted": True,
        })

    # update → перейти в режим редактирования
    if "update" in request.GET:
        return redirect("edit", memo_id=memo.id)

    if memo.is_deleted:
        # 410 Gone — запись удалена
        return render(request, "read.html", {"memo": memo, "gone": True}, status=410)

    return render(request, "read.html", {"memo": memo})

# Редактирование с сохранением ID
def edit(request, memo_id: str):
    memo = get_object_or_404(Memo, pk=memo_id)
    if memo.is_deleted:
        raise Http404("Deleted")

    if request.method == "POST":
        form = MemoForm(request.POST)
        if form.is_valid():
            new_text = form.cleaned_data["text"].strip()
            memo.text = new_text
            memo.version += 1
            memo.content_hash = compute_content_hash(new_text)
            memo.save(update_fields=["text", "version", "content_hash", "updated_at"])
            return redirect("saved", memo_id=memo.id)
    else:
        form = MemoForm(initial={"text": memo.text})

    return render(request, "edit.html", {"form": form, "memo": memo})

# (Опционально) Создать новую запись на основе существующей — новый ID
def fork_new_id(request, memo_id: str):
    memo = get_object_or_404(Memo, pk=memo_id)
    new_id = generate_stable_id()
    Memo.objects.create(
        id=new_id,
        text=memo.text,
        content_hash=compute_content_hash(memo.text),
    )
    return redirect("saved", memo_id=new_id)
