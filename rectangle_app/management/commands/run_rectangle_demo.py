from django.core.management.base import BaseCommand
from rectangle_app.rectangle import Rectangle


class Command(BaseCommand):
    help = "Demonstrates the custom Rectangle class"

    def handle(self, *args, **options):
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("Rectangle class demo")
        self.stdout.write("=" * 60)

        rect = Rectangle(length=10, width=5)
        self.stdout.write(f"Created: Rectangle(length=10, width=5)")
        self.stdout.write("Iterating:")
        for item in rect:
            self.stdout.write(f"  {item}")

        self.stdout.write("\nAnother example — Rectangle(length=7, width=3):")
        for item in Rectangle(length=7, width=3):
            self.stdout.write(f"  {item}")

        self.stdout.write(self.style.SUCCESS("\n✔  Rectangle class works correctly!"))
