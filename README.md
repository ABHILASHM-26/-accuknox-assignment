# AccuKnox Django Trainee Assignment

## Setup

```bash
pip install django
python manage.py migrate
```

## Running the demos

```bash
# Q1, Q2, Q3 — Django Signals
python manage.py run_signal_demos

# Q4 — Rectangle class
python manage.py run_rectangle_demo
```

---

## Q1 — Are Django signals synchronous or asynchronous?

**Answer: Synchronous.**

`slow_receiver` in `signals_app/signals.py` sleeps for 2 seconds. The management command
measures the time taken by `Order.objects.create()`. The call blocks for ≥ 2 seconds,
proving the caller waits for all receivers to complete before continuing.

**output:**
```
[Q1] Receiver started for 'q1_test' — sleeping 2 seconds...
[Q1] Receiver finished for 'q1_test'
[Q1] Order.objects.create() returned after 2.01s
✔  PROOF: The caller BLOCKED for ≥2 seconds. Signals are SYNCHRONOUS.
```

---

## Q2 — Do Django signals run in the same thread as the caller?

**Answer: Yes.**

`thread_check_receiver` in `signals_app/signals.py` logs `threading.current_thread().ident`.
The management command also logs the caller's thread ID before the save. Both IDs are
identical, confirming the receiver executes in the caller's thread.

**output:**
```
[Q2] Caller   thread ID : 139669712961664
[Q2] Receiver thread ID : 139669712961664
✔  PROOF: Compare the two thread IDs above — they are identical.
```

---

## Q3 — Do Django signals run in the same database transaction as the caller?

**Answer: Yes (by default).**

`transactional_receiver` in `signals_app/signals.py` creates a companion `Order` inside
the signal handler. The management command wraps the original save in `transaction.atomic()`
and then deliberately raises an exception to force a rollback. After the rollback, **neither**
the original Order **nor** the companion Order exists in the database — both were rolled back
together because they shared the same transaction.

**output:**
```
[Q3] Orders with 'txn_test' prefix before: 0
[Q3] Receiver created a companion Order inside the signal handler
[Q3] Order saved and signal fired. About to ROLLBACK...
[Q3] Caught: Intentional rollback to prove transaction sharing
[Q3] Orders with 'txn_test' prefix after : 0
✔  PROOF: BOTH the original save AND the signal's companion Order were rolled back.
```

---

## Q4 — Custom Rectangle class

**File:** `rectangle_app/rectangle.py`

```python
class Rectangle:
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width

    def __iter__(self):
        yield {'length': self.length}
        yield {'width': self.width}
```

**Usage:**
```python
rect = Rectangle(length=10, width=5)
for item in rect:
    print(item)
# {'length': 10}
# {'width': 5}
```
