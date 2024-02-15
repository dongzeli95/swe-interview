// # from nltk.tokenize import sent_tokenize

// # Your task is to design and implement a meeting scheduler.
// # The scheduler allows users to book time slots for incoming meetings.
// # A meeting occupies one or more consecutive time slots, and never overlaps any other meetings.
// # Initially there are 8 available time slots : 0, 1, 2, ..., 7.

// # The scheduler supports two operations :
// # (A) Scheduling a meeting - Given the meeting duration D (an integer within 1..8), 
// # the scheduler books D consecutive available time slots, or rejects the meeting if there are no such time slots.

// # (B) Canceling a meeting - Given a scheduled meeting, the scheduler frees up all time slots which were booked for this meeting.

// # [2, 1, 3, 4]

// [0, 1, 2, 3, 4, 5..7]
// [2], [3, 5]

// [0, 1], [1, -1] // map key: time, value: 1/-1 start point, end point
// [start]

// [0, 1]
// [2]
// [4, 6]

#include <string>
#include <vector>
#include <iostream>
using namespace std;

class Scheduler {
public:
  int size;
  vector<bool> slots;
  Scheduler(int s) {
    size = s;
    slots = vector<bool>(size, true);
  }

  bool is_room_idle(int start, int duration) {
    for (int i = start; i < start+duration; i++) {
        if (!slots[i]) {
            return false;
        }
    }

    return true;
  }
  string schedule(int duration) {
    for (int i = 0; i < size; i++) {
        if (i+duration > size) break;
        if (is_room_idle(i, duration)) {
            // update slots to busy.
            for (int pos = i; pos < i+duration; pos++) {
                slots[pos] = false;
            }
            return to_string(i) + "#" + to_string(duration);
        }
    }

    return "REJECT";
  }

  pair<int, int> decodeID(string meeting_id) {
    size_t pos = meeting_id.find('#');
    string start = meeting_id.substr(0, pos);
    string dur = meeting_id.substr(pos+1);
    return {stoi(start), stoi(dur)};
  }

  bool cancel(string meeting_id) {
    pair<int, int> p = decodeID(meeting_id);
    for (int i = p.first; i < p.first +p.second; i++) {
        slots[i] = true;
    }

    return true;
  }

  void debug() {
    for (int i = 0; i < slots.size(); i++) {
        cout << slots[i] << " ";
    }
    cout << endl;
  }
};

int main() {
    Scheduler s = Scheduler(8);
// # [2, 1, 3, 4]
    // schedule a meeting duration 2
    string meeting2 = s.schedule(2);
    s.debug();
    // schedule meeting duration 1
    s.schedule(1);
    s.debug();
    // cancel meeting with duration 2
    s.cancel(meeting2);
    s.debug();
    // scheduel meeting duration 3
    s.schedule(3);
    s.debug(); // 110000
    // scheduel meeting duration 4
    string meeting4 = s.schedule(4);
    cout << meeting4 << endl; // Reject

    meeting2 = s.schedule(2);
    s.debug();

    meeting2 = s.schedule(2);
    s.debug();
    // cout << meeting4 << endl; // Reject

    return 0;
}
