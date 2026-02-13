from django import forms
from .models import Job
from .utils import time_choices
import datetime

class JobAdminForm(forms.ModelForm):

    job_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Job Date"
    )

    job_time = forms.ChoiceField(
        choices=time_choices(),
        label="Job Time"
    )

    class Meta:
        model = Job
        exclude = ('scheduled_datetime',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate fields when editing
        if self.instance.pk and self.instance.scheduled_datetime:
            self.fields['job_date'].initial = self.instance.scheduled_datetime.date()
            self.fields['job_time'].initial = self.instance.scheduled_datetime.strftime("%H:%M")

    def clean(self):
        cleaned_data = super().clean()

        date = cleaned_data.get('job_date')
        time_str = cleaned_data.get('job_time')

        if date and time_str:
            hour, minute = map(int, time_str.split(":"))
            cleaned_data['scheduled_datetime'] = datetime.datetime.combine(
                date,
                datetime.time(hour, minute)
            )

        return cleaned_data

    def save(self, commit=True):
        self.instance.scheduled_datetime = self.cleaned_data['scheduled_datetime']
        return super().save(commit)
