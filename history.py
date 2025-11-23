from django.utils import timezone
from datetime import timedelta

from library.models import Task, SubTask
today = timezone.now()

task = Task.objects.create(
    title="Prepare presentation",
    description="Prepare materials and slides for the presentation",
    status="new",
    deadline=today + timedelta(days=3),
)
task
subtask1 = SubTask.objects.create(
    title="Gather information",
    description="Find necessary information for the presentation",
    status="new",
    deadline=today + timedelta(days=2),
    task=task,
)
subtask1
subtask2 = SubTask.objects.create(
    title="Create slides",
    description="Create presentation slides",
    status="new",
    deadline=today + timedelta(days=1),
    task=task,
)
subtask2
task = Task.objects.get(title="Prepare presentation")
subtasks = task.subtask_set.all().order_by("deadline")

for s in subtasks:
    print(s.title, "→", s.deadline)

task = Task.objects.get(title="Prepare presentation")
subtasks = task.subtasks.all().order_by("created_at")

for s in subtasks:
    print(s.title, "→", s.created_at)
subtasks = task.subtasks.all().order_by("deadline")

for s in subtasks:
    print(s.title, "→", s.deadline)
task = Task.objects.get(title="Prepare presentation")
urgent_subtask = task.subtasks.all().order_by("deadline").first()

print(urgent_subtask.title, "→", urgent_subtask.deadline)
,ЮБ?><":L';l/.,mm][p}{P=-0+_)-09)(*(*&*&^&^%^%$%$#%$##$@!~`\|\|Zzxcm,././>?,
count_subtasks = task.subtasks.count()
print(count_subtasks)
new_subtasks = task.subtasks.filter(status="new")

for s in new_subtasks:
    print(s.title, s.status)
subtask = task.subtasks.get(title="Create slides")
subtask.status = "in_progress"
subtask.save()
print(subtask.title, subtask.status)
subtask_to_delete = task.subtasks.get(title="Gather information")
subtask_to_delete.delete()
new_subtask = task.subtasks.create(
    title="Finalize presentation",
    description="Finish all details and polish slides",
    status="completed",
    deadline=timezone.now() + timedelta(days=3)
)

print(new_subtask, new_subtask.status, new_subtask.deadline)
subtasks = task.subtasks.all().order_by("status", "deadline")

for s in subtasks:
    print(s.title, s.status, s.deadline)
has_completed = task.subtasks.filter(status="completed").exists()
print(has_completed)
%history -f history.py
