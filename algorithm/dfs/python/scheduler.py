"""Meeting Scheduler.

Design a meeting scheduler that books D consecutive available time slots or
rejects the request, and can cancel a previously scheduled meeting by id.

Approaches:
    1. Scheduler: linear scan over a boolean slot array.
       - schedule(D): O(N * D) worst case scan for a free window.
       - cancel(id):  O(D) to free the booked slots.
       - Space:       O(N) for the slot array.
"""

from typing import Tuple


class Scheduler:
    def __init__(self, s: int) -> None:
        self.size = s
        self.slots = [True] * s  # True == idle/free

    def is_room_idle(self, start: int, duration: int) -> bool:
        for i in range(start, start + duration):
            if not self.slots[i]:
                return False
        return True

    def schedule(self, duration: int) -> str:
        for i in range(self.size):
            if i + duration > self.size:
                break
            if self.is_room_idle(i, duration):
                # mark slots as busy
                for pos in range(i, i + duration):
                    self.slots[pos] = False
                return f"{i}#{duration}"
        return "REJECT"

    def decodeID(self, meeting_id: str) -> Tuple[int, int]:
        pos = meeting_id.find('#')
        start = meeting_id[:pos]
        dur = meeting_id[pos + 1:]
        return int(start), int(dur)

    def cancel(self, meeting_id: str) -> bool:
        start, dur = self.decodeID(meeting_id)
        for i in range(start, start + dur):
            self.slots[i] = True
        return True

    def debug(self) -> None:
        print(" ".join("1" if x else "0" for x in self.slots))


if __name__ == "__main__":
    s = Scheduler(8)
    # [2, 1, 3, 4]
    # schedule a meeting duration 2
    meeting2 = s.schedule(2)
    s.debug()
    # schedule meeting duration 1
    s.schedule(1)
    s.debug()
    # cancel meeting with duration 2
    s.cancel(meeting2)
    s.debug()
    # schedule meeting duration 3
    s.schedule(3)
    s.debug()  # 110000
    # schedule meeting duration 4
    meeting4 = s.schedule(4)
    print(meeting4)  # REJECT

    meeting2 = s.schedule(2)
    s.debug()

    meeting2 = s.schedule(2)
    s.debug()
