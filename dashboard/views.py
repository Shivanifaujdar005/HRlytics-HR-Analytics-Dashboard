from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from .forms import AttendanceFileForm, WorkSubmissionFileForm


import pandas as pd
from .models import AttendanceFile
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def attendance_analytics(request):
    latest_file = AttendanceFile.objects.order_by('-uploaded_at').first()
    table_html = None
    summary = None
    chart_data = None

    if latest_file:
        # Read CSV (make sure the uploaded format is .csv or handle Excel as needed)
        file_path = latest_file.file.path
        df = pd.read_csv(file_path)
        
        table_html = df.head(10).to_html(classes='table', index=False)

        # Example summarization: Count present days per employee
        # Suppose your file has columns: Employee, Date, Status (Present/Absent)
        if 'Employee' in df.columns and 'Status' in df.columns:
            present_summary = df[df['Status'] == 'Present'].groupby('Employee').size().reset_index(name='Days_Present')
            summary = present_summary.to_dict(orient='records')
            chart_data = {
                'labels': list(present_summary['Employee']),
                'values': list(present_summary['Days_Present']),
            }

    return render(request, 'dashboard/attendance_analytics.html',
                  {'table_html': table_html, 'summary': summary, 'chart_data': chart_data})


@login_required
def home(request):
    
    return render(request, 'dashboard/home.html', {'profile': profile, })



@login_required
def upload_attendance(request):
    preview_html = None
    show_analytics = False
    message = ""
    if request.method == 'POST':
        form = AttendanceFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            message = "Attendance file uploaded successfully!"

            # Get the uploaded file from the just-saved instance
            file_path = instance.file.path
            try:
                df = pd.read_csv(file_path)
                preview_html = df.head(10).to_html(classes='table', index=False)
                show_analytics = True
            except Exception as e:
                message += " (Preview failed: %s)" % str(e)

            return render(
                request,
                'dashboard/upload_attendance.html',
                {
                    'message': message,
                    'form': AttendanceFileForm(),
                    'preview_html': preview_html,
                    'show_analytics': show_analytics
                }
            )
    else:
        form = AttendanceFileForm()
    return render(request, 'dashboard/upload_attendance.html', {'form': form})

# Similarly repeat for other types:
@login_required
def upload_work_submission(request):
    preview_html = None
    show_analytics = False
    message = ""
    if request.method == 'POST':
        form = WorkSubmissionFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            message = "Work submission uploaded!"
            file_path = instance.file.path
            try:
                import pandas as pd
                df = pd.read_csv(file_path)
                preview_html = df.head(10).to_html(classes='table', index=False)
                show_analytics = True
            except Exception as e:
                message += " (Preview failed: %s)" % str(e)
            return render(
                request,
                'dashboard/upload_work_submission.html',
                {
                    'message': message,
                    'form': WorkSubmissionFileForm(),
                    'preview_html': preview_html,
                    'show_analytics': show_analytics
                }
            )
    else:
        form = WorkSubmissionFileForm()
    return render(request, 'dashboard/upload_work_submission.html', {'form': form})


@login_required
def work_submission_analytics(request):
    from .models import WorkSubmissionFile
    import pandas as pd
    latest_file = WorkSubmissionFile.objects.order_by('-uploaded_at').first()
    table_html, chart_data = None, None

    if latest_file:
        file_path = latest_file.file.path
        df = pd.read_csv(file_path)
        table_html = df.head(10).to_html(classes='table', index=False)

        # Submissions per Employee (Bar)
        bar_df = df.groupby('Employee').size().reset_index(name='Submissions')
        bar_labels = bar_df['Employee'].tolist()
        bar_values = bar_df['Submissions'].tolist()

        # Submissions over Time (Line)
        line_df = df.groupby('Submission Date').size().reset_index(name='DailySubmissions')
        line_labels = line_df['Submission Date'].tolist()
        line_values = line_df['DailySubmissions'].tolist()

        # Hours Spent Distribution (Histogram)
        hist, bin_edges = pd.cut(df['Hours Spent'], bins=5, retbins=True)
        hist_series = hist.value_counts().sort_index()
        hist_labels = [f"{round(bin_edges[i],1)}-{round(bin_edges[i+1],1)}" for i in range(len(bin_edges)-1)]
        hist_values = hist_series.tolist()

        chart_data = {
            'bar_labels': bar_labels,
            'bar_values': bar_values,
            'line_labels': line_labels,
            'line_values': line_values,
            'hist_labels': hist_labels,
            'hist_values': hist_values
        }
    else:
        chart_data = {
            'bar_labels': [],
            'bar_values': [],
            'line_labels': [],
            'line_values': [],
            'hist_labels': [],
            'hist_values': []
        }

    return render(request, 'dashboard/work_submission_analytics.html', {
        'table_html': table_html,
        'chart_data': chart_data
    })



@login_required
def upload_performance_review(request):
    preview_html = None
    show_analytics = False
    message = ""
    if request.method == 'POST':
        form = PerformanceReviewFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            message = "Performance review uploaded!"
            file_path = instance.file.path
            try:
                import pandas as pd
                df = pd.read_csv(file_path)
                preview_html = df.head(10).to_html(classes='table', index=False)
                show_analytics = True
            except Exception as e:
                message += f" (Preview failed: {str(e)})"
            return render(
                request,
                'dashboard/upload_performance_review.html',
                {
                    'message': message,
                    'form': PerformanceReviewFileForm(),
                    'preview_html': preview_html,
                    'show_analytics': show_analytics
                }
            )
    else:
        form = PerformanceReviewFileForm()
    return render(request, 'dashboard/upload_performance_review.html', {'form': form})


@login_required
def performance_review_analytics(request):
    from .models import PerformanceReviewFile
    import pandas as pd
    latest_file = PerformanceReviewFile.objects.order_by('-uploaded_at').first()
    table_html = None
    chart_data = None

    if latest_file:
        file_path = latest_file.file.path
        df = pd.read_csv(file_path)
        table_html = df.head(10).to_html(classes='table', index=False)

        # Example: Summarization by Employee and Average Score
        score_col = 'Score' if 'Score' in df.columns else None
        bar_labels = df['Employee'].unique().tolist() if 'Employee' in df.columns else []
        if score_col:
            bar_values = [df[df['Employee'] == emp][score_col].mean() for emp in bar_labels]
        else:
            bar_values = [df[df['Employee'] == emp].shape[0] for emp in bar_labels]

        # Reviews Over Time (Line)
        if 'Review Date' in df.columns:
            line_df = df.groupby('Review Date').size().reset_index(name='DailyReviews')
            line_labels = line_df['Review Date'].tolist()
            line_values = line_df['DailyReviews'].tolist()
        else:
            line_labels = []
            line_values = []

        # Score Distribution (Histogram)
        if score_col:
            hist, bin_edges = pd.cut(df[score_col], bins=5, retbins=True)
            hist_series = hist.value_counts().sort_index()
            hist_labels = [f"{round(bin_edges[i],1)}-{round(bin_edges[i+1],1)}" for i in range(len(bin_edges)-1)]
            hist_values = hist_series.tolist()
        else:
            hist_labels = []
            hist_values = []

        chart_data = {
            'bar_labels': bar_labels,
            'bar_values': bar_values,
            'line_labels': line_labels,
            'line_values': line_values,
            'hist_labels': hist_labels,
            'hist_values': hist_values
        }
    else:
        chart_data = {
            'bar_labels': [],
            'bar_values': [],
            'line_labels': [],
            'line_values': [],
            'hist_labels': [],
            'hist_values': []
        }

    return render(request, 'dashboard/performance_review_analytics.html', {
        'table_html': table_html,
        'chart_data': chart_data
    })


@login_required
def upload_leave_data(request):
    if request.method == 'POST':
        form = LeaveDataFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'dashboard/upload_leave_data.html', {'message': 'Leave data uploaded!', 'form': LeaveDataFileForm()})
    else:
        form = LeaveDataFileForm()
    return render(request, 'dashboard/upload_leave_data.html', {'form': form})

@login_required
def upload_engagement_survey(request):
    if request.method == 'POST':
        form = EngagementSurveyFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'dashboard/upload_engagement_survey.html', {'message': 'Engagement survey uploaded!', 'form': EngagementSurveyFileForm()})
    else:
        form = EngagementSurveyFileForm()
    return render(request, 'dashboard/upload_engagement_survey.html', {'form': form})

@login_required
def upload_skill_matrix(request):
    if request.method == 'POST':
        form = SkillMatrixFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'dashboard/upload_skill_matrix.html', {'message': 'Skill matrix uploaded!', 'form': SkillMatrixFileForm()})
    else:
        form = SkillMatrixFileForm()
    return render(request, 'dashboard/upload_skill_matrix.html', {'form': form})



from .forms import *
from .models import *

@login_required
def profile(request):
    profile, created = HRProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = HRProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
    else:
        form = HRProfileForm(instance=profile)
    return render(request, 'dashboard/profile.html', {'form': form, 'profile': profile})

