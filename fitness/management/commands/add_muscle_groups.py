from django.core.management.base import BaseCommand

from fitness.models import MuscleGroup


muscle_groups = [
    "Chest",
    "Back",
    "Shoulders",
    "Biceps",
    "Triceps",
    "Forearms",
    "Abs",
    "Quads",
    "Hamstrings",
    "Calves",
    "Glutes"
]
def add_muscle_groups():
    for group in muscle_groups:
        MuscleGroup.objects.get_or_create(name=group)
    print("Muscle groups added successfully.")

if __name__ == "__main__":
    add_muscle_groups()

class Command(BaseCommand):
    help = "Add muscle groups to the database"

    def handle(self, *args, **options):
        add_muscle_groups()