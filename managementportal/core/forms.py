from django import forms
from .models import Plan

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['title', 'description', 'start_date', 'end_date', 'progress']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }




from .models import Team

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['department_name', 'team_leader', 'members', 'materials', 'machines']
        widgets = {
            'members': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter member names separated by commas'}),
            'materials': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Enter materials separated by commas'}),
            'machines': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Enter machines separated by commas'}),
        }




from .models import Employee, RoleAssignment

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'skills']
        widgets = {
            'skills': forms.Textarea(attrs={'rows':3, 'placeholder':'Enter skills separated by commas'})
        }

class RoleAssignmentForm(forms.ModelForm):
    class Meta:
        model = RoleAssignment
        fields = ['employee', 'role_name', 'project_name', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type':'date'}),
        }




from .models import Message,Task,MoraleBadge

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient_name', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows':3, 'placeholder':'Enter your instructions or motivational message'}),
        }
class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['progress']

class MoraleForm(forms.ModelForm):
    class Meta:
        model = MoraleBadge
        fields = ['employee', 'badge_type']
