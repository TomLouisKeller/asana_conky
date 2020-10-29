# any sane programming language would have a much easier way to do this, but here we are
# admitted, asana is also a cripple with its due_on and due_at rather than just storing a date and a time
from datetime import datetime


class Task:

    def __init__(self, id, name: str, due_on: str, due_at: str):
        self.id = id
        self.name = name

        if due_at is not None:  # remove the Z at the end of the iso string
            due_at = due_at[:-1]

        self.due_date = None
        self.due_time = None

        if due_on is not None and due_at is not None:
            if datetime.fromisoformat(due_on).strftime("%y-%d-%m") != datetime.fromisoformat(due_at).strftime("%y-%d-%m"):
                raise("due_on and due_at are not on the same date! what now?")
            else:
                self.due_date = datetime.fromisoformat(due_at).date()
                self.due_time = datetime.fromisoformat(due_at).time()
        elif due_on is not None:
            self.due_date = datetime.fromisoformat(due_on).date()
        elif due_at is not None:
            self.due_date = datetime.fromisoformat(due_at).date()
            self.due_time = datetime.fromisoformat(due_at).time()

    def __lt__(self, other):
        if self.due_time is not None and other.due_time is not None:
            if self.due_date == other.due_date:
                return self.due_time < other.due_time
            else:
                return self.due_date < other.due_date
        elif self.due_date is not None and other.due_date is not None:
            if self.due_date == other.due_date:
                if self.due_time is not None:
                    return True
                else:
                    return False
            else:
                return self.due_date < other.due_date
        elif self.due_date is not None or self.due_time is not None:
            return True
        elif other.due_date is not None or other.due_time is not None:
            return False
        else:
            return self.name < other.name
