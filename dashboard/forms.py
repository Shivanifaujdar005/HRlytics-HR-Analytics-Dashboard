from django import forms
from .models import AttendanceFile, WorkSubmissionFile
from .models import *

class AttendanceFileForm(forms.ModelForm):
    class Meta:
        model = AttendanceFile
        fields = ['file']

class WorkSubmissionFileForm(forms.ModelForm):
    class Meta:
        model = WorkSubmissionFile
        fields = ['file']

class PerformanceReviewFileForm(forms.ModelForm):
    class Meta:
        model = PerformanceReviewFile
        fields = ['file']

class LeaveDataFileForm(forms.ModelForm):
    class Meta:
        model = LeaveDataFile
        fields = ['file']

class EngagementSurveyFileForm(forms.ModelForm):
    class Meta:
        model = EngagementSurveyFile
        fields = ['file']

class SkillMatrixFileForm(forms.ModelForm):
    class Meta:
        model = SkillMatrixFile
        fields = ['file']