from django import forms


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            css = widget.attrs.get("class", "")
            if isinstance(widget, (forms.CheckboxInput, forms.ClearableFileInput)):
                widget.attrs["class"] = f"{css} form-check-input".strip()
            else:
                widget.attrs["class"] = f"{css} form-control".strip()
            if field.help_text:
                widget.attrs.setdefault("aria-describedby", f"help-{id(field)}")
