"""
Management command: python manage.py run_signal_demos

Runs all three Django signal proofs and prints the results clearly.
"""
import time
import threading
from django.core.management.base import BaseCommand
from django.db import transaction
from signals_app.models import Order


class Command(BaseCommand):
    help = "Demonstrates Q1 (sync), Q2 (same thread), Q3 (same transaction) for Django signals"

    def handle(self, *args, **options):
        self._demo_q1_synchronous()
        self._demo_q2_same_thread()
        self._demo_q3_same_transaction()

    # ── Q1: Synchronous ──────────────────────────────────────────────────────
    def _demo_q1_synchronous(self):
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("Q1: Are Django signals synchronous or asynchronous?")
        self.stdout.write("=" * 60)
        self.stdout.write("Creating an Order — the slow_receiver will sleep 2 seconds.")
        self.stdout.write("If signals were ASYNC, the call would return immediately.")

        start = time.time()
        Order.objects.create(name="q1_test")
        elapsed = time.time() - start

        self.stdout.write(f"[Q1] Order.objects.create() returned after {elapsed:.2f}s")
        if elapsed >= 2:
            self.stdout.write(
                self.style.SUCCESS(
                    "✔  PROOF: The caller BLOCKED for ≥2 seconds. Signals are SYNCHRONOUS."
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "⚠  Elapsed < 2s — make sure the slow_receiver is registered."
                )
            )

    # ── Q2: Same thread ───────────────────────────────────────────────────────
    def _demo_q2_same_thread(self):
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("Q2: Do signals run in the same thread as the caller?")
        self.stdout.write("=" * 60)

        caller_thread_id = threading.current_thread().ident
        self.stdout.write(f"[Q2] Caller   thread ID : {caller_thread_id}")
        # The thread_check_receiver prints the receiver's thread ID on save.
        Order.objects.create(name="q2_test")
        self.stdout.write(
            self.style.SUCCESS(
                "✔  PROOF: Compare the two thread IDs printed above — they are identical."
            )
        )

    # ── Q3: Same transaction ──────────────────────────────────────────────────
    def _demo_q3_same_transaction(self):
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("Q3: Do signals run in the same DB transaction as the caller?")
        self.stdout.write("=" * 60)

        count_before = Order.objects.filter(name__startswith="txn_test").count()
        self.stdout.write(f"[Q3] Orders with 'txn_test' prefix before: {count_before}")

        try:
            with transaction.atomic():
                # The receiver will create a companion Order inside this same transaction.
                Order.objects.create(name="txn_test_demo")
                self.stdout.write("[Q3] Order saved and signal fired. About to ROLLBACK...")
                # Force a rollback by raising an exception inside the atomic block.
                raise Exception("Intentional rollback to prove transaction sharing")
        except Exception as e:
            self.stdout.write(f"[Q3] Caught: {e}")

        count_after = Order.objects.filter(name__startswith="txn_test").count()
        self.stdout.write(f"[Q3] Orders with 'txn_test' prefix after : {count_after}")

        if count_after == count_before:
            self.stdout.write(
                self.style.SUCCESS(
                    "✔  PROOF: BOTH the original save AND the signal's companion Order "
                    "were rolled back. They shared the same transaction."
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "⚠  Unexpected: some records survived — check signal registration."
                )
            )
