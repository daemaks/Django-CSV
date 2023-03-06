from django import forms

from .models import Column, DataSchema


class DataSchemaForm(forms.ModelForm):
    class Meta:
        model = DataSchema
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["class"] = "form-control"


class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = [
            "name",
            "type",
            "order",
            "range_start",
            "range_end",
            "sentences",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["class"] = "form-control"
        self.fields["type"].widget.attrs["class"] = "form-control"
        self.fields["order"].widget.attrs["class"] = "form-control"
        self.fields["range_start"].widget.attrs["class"] = "form-control"
        self.fields["range_end"].widget.attrs["class"] = "form-control"
        self.fields["sentences"].widget.attrs["class"] = "form-control"

    def clean(self):
        cleaned_data = super().clean()
        type = cleaned_data.get("type")

        if type == "integer":
            range_start = cleaned_data.get("range_start")
            range_end = cleaned_data.get("range_end")

            if range_start is None or range_end is None:
                raise forms.ValidationError(
                    "Please provide range for integer field."
                )
            elif range_start > range_end:
                raise forms.ValidationError(
                    "Range start should be less than or equal to range end."
                )

        return cleaned_data


ColumnFormSet = forms.formset_factory(ColumnForm, extra=3)
ModelColumnFormSet = forms.modelformset_factory(Column, form=ColumnForm)
