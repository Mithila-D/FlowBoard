from django.db import models

# Create your models here.


from django.db import models

class Plan(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    progress = models.IntegerField(default=0)  # percentage

    def __str__(self):
        return self.title


class Team(models.Model):
    department_name = models.CharField(max_length=200)
    team_leader = models.CharField(max_length=100)
    members = models.TextField(help_text="Comma separated names of team members")
    materials = models.TextField(blank=True, help_text="Comma separated materials")
    machines = models.TextField(blank=True, help_text="Comma separated machines")

    def __str__(self):
        return self.department_name



class Employee(models.Model):
    name = models.CharField(max_length=100)
    skills = models.TextField(help_text="Comma separated skills")

    def __str__(self):
        return self.name

class RoleAssignment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    role_name = models.CharField(max_length=100)
    project_name = models.CharField(max_length=100)
    deadline = models.DateField()

    def __str__(self):
        return f"{self.employee.name} - {self.role_name}"







# -----
class Message(models.Model):
    recipient_name = models.CharField(max_length=100, help_text="Team member or team name")
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recipient_name} - {self.sent_at.strftime('%Y-%m-%d %H:%M')}"

from django.db import models

class EmployeeDirecting(models.Model):
    name = models.CharField(max_length=100)
    fields = ['name'] 

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateField()
    progress = models.IntegerField(default=0)
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

class MoraleBadge(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    badge_type = models.CharField(max_length=50)
    awarded_at = models.DateTimeField(auto_now_add=True)
