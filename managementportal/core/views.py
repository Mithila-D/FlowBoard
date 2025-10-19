from django.shortcuts import render, redirect, get_object_or_404
from .models import Plan
from .forms import PlanForm

def home(request):
    return render(request, 'core/home.html')

# def planning(request):
#     plans = Plan.objects.all().order_by('start_date')
    
#     if request.method == 'POST':
#         if 'add_plan' in request.POST:   
#             form = PlanForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 return redirect('planning')
#         elif 'delete_plan' in request.POST:   
#             name_to_delete = request.POST.get('plan_name')
#             plan = Plan.objects.filter(title=name_to_delete).first()
#             if plan:
#                 plan.delete()
#                 return redirect('planning')
#     else:
#         form = PlanForm()

#     return render(request, 'core/planning.html', {'form': form, 'plans': plans})




from django.shortcuts import render, redirect
from .models import Plan
from .forms import PlanForm

def planning(request):
    plans = Plan.objects.all().order_by('start_date')

    if request.method == 'POST':
        # Add a new plan
        if 'add_plan' in request.POST:
            form = PlanForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('planning')
        # Delete a plan
        elif 'delete_plan' in request.POST:
            plan_name = request.POST.get('plan_name')
            plan = Plan.objects.filter(title=plan_name).first()
            if plan:
                plan.delete()
                return redirect('planning')
    else:
        form = PlanForm()  # Ensure form is always initialized

    return render(request, 'core/planning.html', {'form': form, 'plans': plans})

















# from .models import Team
# from .forms import TeamForm

# def organizing(request):
#     teams = Team.objects.all()
#     if request.method == 'POST':
#         if 'add_team' in request.POST:
#             form = TeamForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 return redirect('organizing')
#         elif 'delete_team' in request.POST:
#             name_to_delete = request.POST.get('team_name')
#             team = Team.objects.filter(department_name=name_to_delete).first()
#             if team:
#                 team.delete()
#                 return redirect('organizing')
#     else:
#         form = TeamForm()
#     return render(request, 'core/organizing.html', {'form': form, 'teams': teams})



from django.shortcuts import render, redirect
from .models import Team
from .forms import TeamForm

def organizing(request):
    teams = Team.objects.all()
    if request.method == 'POST':
        if 'add_team' in request.POST:
            form = TeamForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('organizing')
        elif 'delete_team' in request.POST:
            name_to_delete = request.POST.get('team_name')
            team = Team.objects.filter(department_name=name_to_delete).first()
            if team:
                team.delete()
                return redirect('organizing')
    else:
        form = TeamForm()
    return render(request, 'core/organizing.html', {'form': form, 'teams': teams})















from .models import Employee, RoleAssignment
from .forms import EmployeeForm, RoleAssignmentForm

def staffing(request):
    employees = Employee.objects.all()
    assignments = RoleAssignment.objects.all()

    if request.method == 'POST':
        if 'add_employee' in request.POST:
            emp_form = EmployeeForm(request.POST)
            if emp_form.is_valid():
                emp_form.save()
                return redirect('staffing')
        elif 'assign_role' in request.POST:
            role_form = RoleAssignmentForm(request.POST)
            if role_form.is_valid():
                role_form.save()
                return redirect('staffing')
        elif 'delete_employee' in request.POST:
            name_to_delete = request.POST.get('employee_name')
            emp = Employee.objects.filter(name=name_to_delete).first()
            if emp:
                emp.delete()
                return redirect('staffing')
    else:
        emp_form = EmployeeForm()
        role_form = RoleAssignmentForm()

    return render(request, 'core/staffing.html', {
        'emp_form': emp_form,
        'role_form': role_form,
        'employees': employees,
        'assignments': assignments
    })




















from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Task, Employee, Plan, MoraleBadge

def directing(request):
    # Auto-delete completed tasks
    Task.objects.filter(progress=100).delete()

    employees = Employee.objects.all()
    plans = Plan.objects.all()
    tasks = Task.objects.all()

    if request.method == "POST":
        # Add new task from selected plan
        if "add_task" in request.POST:
            plan_id = request.POST.get("plan_id")
            employee_id = request.POST.get("employee_id")
            plan = get_object_or_404(Plan, id=plan_id)
            emp = Employee.objects.filter(id=employee_id).first() if employee_id else None

            # Create task from plan details
            Task.objects.create(
                title=plan.title,
                description=plan.description,
                deadline=plan.end_date,
                progress=plan.progress,
                assigned_to=emp,
            )
            return redirect("directing")

        # Update task progress
        if "update_task" in request.POST:
            task_id = request.POST.get("task_id")
            progress = int(request.POST.get("progress"))
            task = get_object_or_404(Task, id=task_id)
            task.progress = progress
            task.save()

            # Also update corresponding Plan progress
            try:
                plan = Plan.objects.get(title=task.title)
                plan.progress = progress
                plan.save()
            except Plan.DoesNotExist:
                pass

            return redirect("directing")

        # Delete task
        if "delete_task" in request.POST:
            task_id = request.POST.get("task_id")
            Task.objects.filter(id=task_id).delete()
            return redirect("directing")

        # Award badge
        if "award_badge" in request.POST:
            employee_id = request.POST.get("employee_id")
            badge_type = request.POST.get("badge_type")
            emp = get_object_or_404(Employee, id=employee_id)
            MoraleBadge.objects.create(employee=emp, badge_type=badge_type, awarded_at=timezone.now())
            return redirect("directing")

        # Delete badge
        if "delete_badge" in request.POST:
            badge_id = request.POST.get("badge_id")
            MoraleBadge.objects.filter(id=badge_id).delete()
            return redirect("directing")

    context = {
        "employees": employees,
        "plans": plans,
        "tasks": tasks,
        "morale_badges": MoraleBadge.objects.all(),
    }
    return render(request, "core/directing.html", context)






















from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Task

def controlling(request):
    # Handle task progress updates
    if request.method == "POST":
        if "update_task" in request.POST:
            task_id = request.POST.get("task_id")
            progress = int(request.POST.get("progress"))
            task = Task.objects.get(id=task_id)
            task.progress = progress
            task.save()
            return redirect("controlling")
    
    # Fetch all tasks
    tasks = Task.objects.all().order_by('deadline')
    
    # Determine overdue tasks
    today = timezone.now().date()
    overdue_tasks = [task for task in tasks if task.deadline < today and task.progress < 100]
    
    return render(request, "core/controlling.html", {
        "tasks": tasks,
        "overdue_tasks": overdue_tasks,
        "today": today  
    })
