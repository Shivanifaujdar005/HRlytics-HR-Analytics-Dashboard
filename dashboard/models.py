from django.db import models
from django.contrib.auth.models import User

class AttendanceFile(models.Model):
    file = models.FileField(upload_to='attendance_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class WorkSubmissionFile(models.Model):
    file = models.FileField(upload_to='work_submission_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class PerformanceReviewFile(models.Model):
    file = models.FileField(upload_to='performance_review_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class LeaveDataFile(models.Model):
    file = models.FileField(upload_to='leave_data_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class EngagementSurveyFile(models.Model):
    file = models.FileField(upload_to='engagement_survey_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class SkillMatrixFile(models.Model):
    file = models.FileField(upload_to='skill_matrix_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)



class PerformanceReviewFile(models.Model):
    file = models.FileField(upload_to='performance_reviews/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Performance file uploaded on {self.uploaded_at}"
