from django.db import models

class Memo(models.Model):
    # Устойчивый «хэш»-ID: короткий, URL-safe
    id = models.CharField(primary_key=True, max_length=22, editable=False)
    text = models.TextField()
    is_deleted = models.BooleanField(default=False)
    version = models.PositiveIntegerField(default=1)  # для истории
    content_hash = models.CharField(max_length=64, blank=True, default="")  # SHA256 от текста (информационно)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

