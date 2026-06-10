"""
Custom Python Class — Rectangle

Requirements:
  1. Requires length (int) and width (int) to initialize.
  2. Instances are iterable.
  3. Iteration yields {'length': <value>} first, then {'width': <value>}.
"""


class Rectangle:
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width

    def __iter__(self):
        # Yield length dict first, then width dict — as specified
        yield {'length': self.length}
        yield {'width': self.width}


# ── Quick demo (also run via: python manage.py run_rectangle_demo) ─────────────
if __name__ == '__main__':
    rect = Rectangle(length=10, width=5)
    print("Iterating over Rectangle(length=10, width=5):")
    for item in rect:
        print(item)
