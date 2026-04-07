# PawPal+ (Module 2 Project)

A smart pet care management system that helps busy pet owners organize and prioritize daily pet care tasks using Python-based scheduling algorithms and a modern Streamlit UI.

## 🎯 Project Overview

PawPal+ is designed to solve a real-world problem: pet owners often struggle to keep track of multiple pets' care routines (walks, feedings, medications, grooming, etc.) while balancing their own schedules. This system intelligently organizes tasks, detects conflicts, and provides recommendations.

## 🌟 Key Features

### Core System
- **Owner & Pet Management** - Create owners with timezone and availability preferences, manage multiple pets with special needs
- **Task Scheduling** - Define tasks with time, duration, priority, and frequency (one-time, daily, weekly)
- **Smart Sorting** - Tasks automatically sorted by time or priority
- **Filtering & Search** - Filter tasks by pet, priority level, or completion status
- **Conflict Detection** - Automatically detects overlapping tasks and warns users
- **Recurring Tasks** - Daily/weekly tasks automatically regenerate after completion
- **Available Time Slots** - Find gaps in the schedule for new activities
- **Schedule Summary** - Generate readable daily summaries with analytics

### UI Features
- **Multi-page Dashboard** - Navigation between Setup, Schedule, Tasks, and Analytics
- **Real-time Visualization** - See all pets and tasks organized by owner
- **Task Management** - Add, remove, and mark tasks as complete
- **Conflict Warnings** - Visual alerts for scheduling conflicts
- **Analytics Dashboard** - View statistics on tasks, priorities, and pet information

## 📂 Project Structure

```
pawpal-project/
├── pawpal_system.py      # Core scheduling logic (classes, algorithms)
├── app.py                # Streamlit UI application
├── main.py               # CLI demo script (testing/verification)
├── tests/
│   └── test_pawpal.py    # Automated test suite (31 tests)
├── requirements.txt      # Python dependencies
├── reflection.md         # Project reflection document
└── README.md             # This file
```

## 🏗️ System Architecture

### Classes

**Task**
- Represents a single pet care activity
- Attributes: description, time (HH:MM), duration_minutes, priority, frequency, is_completed
- Methods: mark_complete(), mark_incomplete(), get_priority_value(), get_end_time()

**Pet**
- Represents a pet and manages its tasks
- Attributes: name, species, age, special_needs, tasks[]
- Methods: add_task(), remove_task(), get_tasks(), get_task_count()

**Owner**
- Manages one or more pets and their combined tasks
- Attributes: name, timezone, availability_hours, pets[]
- Methods: add_pet(), remove_pet(), get_all_tasks(), get_task_count()

**Scheduler**
- "Brain" of the system - organizes and manages tasks intelligently
- Methods:
  - `get_today_schedule()` - Sorted list of today's incomplete tasks
  - `sort_by_time()` / `sort_by_priority()` - Ordering algorithms
  - `filter_by_priority()` / `filter_by_pet()` / `filter_by_status()` - Filtering logic
  - `detect_conflicts()` - Finds overlapping tasks
  - `handle_recurring_task()` - Creates next occurrence of recurring tasks
  - `get_available_time_slots()` - Finds free time blocks
  - `get_schedule_summary()` - Human-readable summary

### Algorithmic Features

1. **Sorting by Time** - Uses `datetime.strptime()` with HH:MM format for accurate chronological ordering
2. **Priority-based Sorting** - Converts priority strings to numeric values (high=3, medium=2, low=1) for comparison
3. **Conflict Detection** - Checks task start times against end times (start + duration) to detect overlaps
4. **Time Slot Finding** - Scans availability window and identifies gaps between scheduled tasks
5. **Recurring Task Logic** - When a task is marked complete, automatically creates a new instance for the next occurrence

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup

```bash
# Clone the repository
git clone https://github.com/sohini1728/ai110-module2show-pawpal-starter.git
cd pawpal-project

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Application

**Interactive Streamlit UI:**
```bash
streamlit run app.py
```
Opens at `http://localhost:8501`

**CLI Demo:**
```bash
python main.py
```
Shows a complete demonstration of all system features in the terminal.

## 🧪 Testing PawPal+

The system includes a comprehensive automated test suite with 31 tests covering:
- Task creation and completion
- Pet and owner management
- All sorting and filtering operations
- Conflict detection
- Recurring task logic
- Edge cases (empty schedules, invalid times, etc.)

### Run Tests

```bash
pytest tests/test_pawpal.py -v
```

**Expected Output:** All 31 tests pass ✅

### Test Coverage Areas
- **Task Operations** (5 tests) - Creation, completion, priority values, end time calculation
- **Pet Management** (4 tests) - Adding/removing tasks, filtering by status
- **Owner Management** (4 tests) - Multi-pet task aggregation, filtering
- **Scheduler Core** (14 tests) - Sorting, filtering, conflict detection, recurring tasks
- **Edge Cases** (6 tests) - Empty schedules, invalid formats, boundary conditions

**Confidence Level:** ⭐⭐⭐⭐⭐ (5/5) - All core behaviors verified through automated tests

## �� Design Decisions & Tradeoffs

### Design Choice: Time Representation
**Decision:** Store times as strings in "HH:MM" format
**Rationale:** Simple, human-readable, easy to input via UI
**Tradeoff:** Requires parsing for calculations, but acceptable for this scope

### Algorithm: Conflict Detection
**Decision:** Check exact time overlaps (task2.start < task1.end)
**Rationale:** Catches most real conflicts, simple to implement
**Tradeoff:** Doesn't account for buffer time between tasks; acceptable for MVP

### Recurrence Handling
**Decision:** Create new task instance on marking complete, don't modify date
**Rationale:** Keeps original task immutable, simpler logic
**Tradeoff:** Doesn't calculate next day/week; suitable for CLI-first workflow

### Session State Management
**Decision:** Use `st.session_state` for persistent Owner object
**Rationale:** Ensures data survives page refreshes in Streamlit
**Tradeoff:** Data lost on app restart; acceptable for single-session usage

## 📊 How Scheduling Works

1. **Input:** Owner defines availability window (e.g., "08:00-22:00") and creates pets with tasks
2. **Organization:** Scheduler sorts tasks chronologically and by priority
3. **Validation:** System detects conflicts and warns user
4. **Output:** Daily schedule generated with sorted tasks, available time slots, and analytics
5. **Recurrence:** Marked tasks automatically regenerate if recurring

## 🎓 AI-Human Collaboration Insights

### How AI Was Used
- **Design Brainstorming:** Copilot helped design the initial UML structure
- **Code Generation:** Skeleton classes and core logic scaffolded with AI assistance
- **Algorithm Design:** Conflict detection and sorting algorithms developed collaboratively
- **Test Generation:** Pytest suite generated with AI, then verified by human review

### Key Judgment Calls
1. **Rejected:** AI suggested storing times as `datetime` objects - instead used strings for simplicity
2. **Modified:** AI's conflict detection logic was simplified for readability
3. **Verified:** All AI-generated code was tested before integration

### Lessons Learned
- AI excels at scaffolding and pattern generation
- Human judgment critical for design tradeoffs
- Separate chat sessions for different phases kept workflow organized
- "CLI-first" approach validated backend before UI integration

## 📝 Usage Examples

### Example 1: Create Owner and Pets
```python
owner = Owner("Sarah", timezone="EST", availability_hours="08:00-22:00")
fido = Pet("Fido", "dog", age=5)
whiskers = Pet("Whiskers", "cat", age=3)
owner.add_pet(fido)
owner.add_pet(whiskers)
```

### Example 2: Add Tasks and View Schedule
```python
fido.add_task(Task("Morning walk", "08:00", 30, "high", "daily"))
fido.add_task(Task("Breakfast", "08:30", 15, "high", "daily"))

scheduler = Scheduler(owner)
today_schedule = scheduler.get_today_schedule()
print(scheduler.get_schedule_summary())
```

### Example 3: Detect Conflicts
```python
conflicts = scheduler.detect_conflicts(owner.get_all_tasks())
if conflicts:
    for task1, task2 in conflicts:
        print(f"⚠️ {task1.description} overlaps with {task2.description}")
```

### Example 4: Find Available Time
```python
available_slots = scheduler.get_available_time_slots(60)  # Find 60-min slots
for start, end in available_slots:
    print(f"Available: {start} to {end}")
```

## 🐾 Demo Screenshot

The Streamlit app includes:
- **Dashboard Tab:** Quick overview of owner and pets with today's schedule
- **Setup Tab:** Owner and pet creation interface
- **Schedule Tab:** Color-coded tasks with conflict warnings
- **Tasks Tab:** Comprehensive task management with filtering
- **Analytics Tab:** Statistics and available time slot finder

## 🔮 Future Enhancements

- Multi-day scheduling (not just today)
- Task duration preferences (morning vs evening)
- Pet health tracking integration
- Notification system for upcoming tasks
- Mobile app version
- Cloud sync for multi-device access
- AI recommendations for optimal scheduling
- Calendar export (iCal, Google Calendar)

## 📞 Support

For questions or issues:
1. Review the test suite in `tests/test_pawpal.py` for usage examples
2. Run `python main.py` to see a complete CLI demonstration
3. Check docstrings in `pawpal_system.py` for API details
4. Review project reflection in `reflection.md`

## 📄 License

This project is part of CodePath's AI110 course (Spring 2026).

---

**Project Status:** ✅ Complete - All phases implemented, tested, and documented

**Last Updated:** April 7, 2026
