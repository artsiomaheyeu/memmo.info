# memmo/forms.py
from django import forms

class MemoForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            "id": "memo-text",
            "rows": 18,
            "placeholder": "Paste or type your message / serial numbers…",
            "autofocus": "autofocus",
            "spellcheck": "false",
            "wrap": "off",
            "class": "mono",
        }),
        label="",
    )
