import time
import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order


# ─── Q1: Synchronous proof ───────────────────────────────────────────────────
# If signals were async, the sender would NOT block while the receiver sleeps.
# Since it IS synchronous, the total time will include the 2-second sleep.

@receiver(post_save, sender=Order)
def slow_receiver(sender, instance, created, **kwargs):
    if created:
        print(f"[Q1] Receiver started for '{instance.name}' — sleeping 2 seconds...")
        time.sleep(2)
        print(f"[Q1] Receiver finished for '{instance.name}'")


# ─── Q2: Same thread proof ────────────────────────────────────────────────────
# We log the thread ID inside the receiver and compare it to the caller's ID.

@receiver(post_save, sender=Order)
def thread_check_receiver(sender, instance, created, **kwargs):
    if created:
        receiver_thread_id = threading.current_thread().ident
        print(f"[Q2] Receiver thread ID  : {receiver_thread_id}")


# ─── Q3: Same database transaction proof ──────────────────────────────────────
# We write a second record inside the receiver. Then in the management command
# we raise an IntegrityError AFTER the save — rolling back the whole transaction.
# If both records disappear, it confirms the receiver shared the same transaction.

@receiver(post_save, sender=Order)
def transactional_receiver(sender, instance, created, **kwargs):
    if created and instance.name.startswith("txn_test"):
        # Write a second Order inside the signal — same transaction as the save
        Order.objects.create(name=f"signal_created_for_{instance.name}")
        print(f"[Q3] Receiver created a companion Order inside the signal handler")
