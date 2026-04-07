"""
PawPal+ System - Core scheduling logic for pet care management.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional
from enum import Enum


class TaskFrequency(Enum):
    """Frequency options for recurring tasks."""
    ONE_TIME = "one_time"
    DAILY = "daily"
    WEEKLY = "weekly"


class TaskPriority(Enum):
    """Priority levels for tasks."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class Task:
    """Represents a single pet care task."""
    description: str
    time: str  # Format: "HH:MM"
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    frequency: str = "one_time"  # "one_time", "daily", "weekly"
    is_completed: bool = False
    pet_name: str = ""
    
    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True
    
    def mark_incomplete(self) -> None:
        """Mark this task as incomplete."""
        self.is_completed = False
    
    def get_priority_value(self) -> int:
        """Return numeric priority value for sorting."""
        priority_map = {"low": 1, "medium": 2, "high": 3}
        return priority_map.get(self.priority.lower(), 1)
    
    def get_end_time(self) -> str:
        """Calculate end time based on duration."""
        try:
            start = datetime.strptime(self.time, "%H:%M")
            end = start + timedelta(minutes=self.duration_minutes)
            return end.strftime("%H:%M")
        except ValueError:
            return "Invalid time"
    
    def __str__(self) -> str:
        status = "✓" if self.is_completed else "○"
        return f"{status} {self.time} - {self.description} ({self.duration_minutes}m, {self.priority})"


@dataclass
class Pet:
    """Represents a pet and their care tasks."""
    name: str
    species: str  # "dog", "cat", "rabbit", etc.
    age: Optional[int] = None
    special_needs: str = ""
    tasks: List[Task] = field(default_factory=list)
    
    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        task.pet_name = self.name
        self.tasks.append(task)
    
    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet."""
        if task in self.tasks:
            self.tasks.remove(task)
    
    def get_tasks(self, completed: Optional[bool] = None) -> List[Task]:
        """Get all tasks, optionally filtered by completion status."""
        if completed is None:
            return self.tasks
        return [t for t in self.tasks if t.is_completed == completed]
    
    def get_task_count(self) -> int:
        """Return the number of tasks for this pet."""
        return len(self.tasks)
    
    def __str__(self) -> str:
        return f"{self.name} ({self.species}) - {len(self.tasks)} tasks"


@dataclass
class Owner:
    """Represents a pet owner and manages their pets."""
    name: str
    timezone: str = "UTC"
    pets: List[Pet] = field(default_factory=list)
    availability_hours: str = "08:00-22:00"  # Default availability window
    
    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)
    
    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner."""
        if pet in self.pets:
            self.pets.remove(pet)
    
    def get_pets(self) -> List[Pet]:
        """Get all pets owned by this owner."""
        return self.pets
    
    def get_all_tasks(self, completed: Optional[bool] = None) -> List[Task]:
        """Get all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks(completed=completed))
        return all_tasks
    
    def get_task_count(self) -> int:
        """Return total number of tasks across all pets."""
        return sum(pet.get_task_count() for pet in self.pets)
    
    def __str__(self) -> str:
        return f"{self.name} ({len(self.pets)} pets, {self.get_task_count()} total tasks)"


class Scheduler:
    """Organizes and manages pet care tasks."""
    
    def __init__(self, owner: Owner):
        """Initialize scheduler with an owner."""
        self.owner = owner
    
    def get_today_schedule(self) -> List[Task]:
        """Get all tasks for today, sorted by time."""
        all_tasks = self.owner.get_all_tasks(completed=False)
        return self.sort_by_time(all_tasks)
    
    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks chronologically by time (HH:MM format)."""
        try:
            return sorted(tasks, key=lambda t: datetime.strptime(t.time, "%H:%M"))
        except ValueError:
            return tasks
    
    def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority (high to low), then by time."""
        return sorted(
            tasks,
            key=lambda t: (-t.get_priority_value(), datetime.strptime(t.time, "%H:%M"))
        )
    
    def filter_by_priority(self, tasks: List[Task], priority: str) -> List[Task]:
        """Filter tasks by priority level."""
        return [t for t in tasks if t.priority.lower() == priority.lower()]
    
    def filter_by_pet(self, tasks: List[Task], pet_name: str) -> List[Task]:
        """Filter tasks by pet name."""
        return [t for t in tasks if t.pet_name == pet_name]
    
    def filter_by_status(self, tasks: List[Task], completed: bool) -> List[Task]:
        """Filter tasks by completion status."""
        return [t for t in tasks if t.is_completed == completed]
    
    def detect_conflicts(self, tasks: List[Task]) -> List[tuple]:
        """Detect tasks that overlap in time."""
        conflicts = []
        sorted_tasks = self.sort_by_time(tasks)
        
        for i in range(len(sorted_tasks)):
            for j in range(i + 1, len(sorted_tasks)):
                task1 = sorted_tasks[i]
                task2 = sorted_tasks[j]
                
                try:
                    time1 = datetime.strptime(task1.time, "%H:%M")
                    time2 = datetime.strptime(task2.time, "%H:%M")
                    end1 = time1 + timedelta(minutes=task1.duration_minutes)
                    
                    # Check if task2 starts before task1 ends
                    if time2 < end1:
                        conflicts.append((task1, task2))
                except ValueError:
                    pass
        
        return conflicts
    
    def handle_recurring_task(self, task: Task) -> Optional[Task]:
        """Create a new task for the next occurrence of a recurring task."""
        if task.frequency.lower() == "daily":
            new_task = Task(
                description=task.description,
                time=task.time,
                duration_minutes=task.duration_minutes,
                priority=task.priority,
                frequency=task.frequency,
                pet_name=task.pet_name
            )
            return new_task
        elif task.frequency.lower() == "weekly":
            new_task = Task(
                description=task.description,
                time=task.time,
                duration_minutes=task.duration_minutes,
                priority=task.priority,
                frequency=task.frequency,
                pet_name=task.pet_name
            )
            return new_task
        return None
    
    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Mark a task complete and create a recurring task if applicable."""
        task.mark_complete()
        
        # If task is recurring, create a new one for next occurrence
        new_task = self.handle_recurring_task(task)
        if new_task:
            # Find the pet and add the new task
            for pet in self.owner.get_pets():
                if pet.name == task.pet_name:
                    pet.add_task(new_task)
                    break
        
        return new_task
    
    def get_available_time_slots(self, duration_minutes: int) -> List[tuple]:
        """Find available time slots in the owner's availability window."""
        all_tasks = self.get_today_schedule()
        
        # Parse availability window (e.g., "08:00-22:00")
        try:
            parts = self.owner.availability_hours.split("-")
            start_time = datetime.strptime(parts[0], "%H:%M")
            end_time = datetime.strptime(parts[1], "%H:%M")
        except (ValueError, IndexError):
            start_time = datetime.strptime("08:00", "%H:%M")
            end_time = datetime.strptime("22:00", "%H:%M")
        
        available_slots = []
        current = start_time
        
        for task in all_tasks:
            task_start = datetime.strptime(task.time, "%H:%M")
            if current < task_start:
                available_slots.append((
                    current.strftime("%H:%M"),
                    task_start.strftime("%H:%M")
                ))
            current = datetime.strptime(task.get_end_time(), "%H:%M")
        
        if current < end_time:
            available_slots.append((
                current.strftime("%H:%M"),
                end_time.strftime("%H:%M")
            ))
        
        return available_slots
    
    def get_schedule_summary(self) -> str:
        """Generate a human-readable summary of today's schedule."""
        schedule = self.get_today_schedule()
        conflicts = self.detect_conflicts(schedule)
        
        summary = "📋 TODAY'S PET CARE SCHEDULE\n"
        summary += "=" * 40 + "\n"
        
        if not schedule:
            summary += "No tasks scheduled for today.\n"
            return summary
        
        current_pet = None
        for task in schedule:
            if task.pet_name != current_pet:
                current_pet = task.pet_name
                summary += f"\n🐾 {current_pet}:\n"
            
            summary += f"  {str(task)}\n"
        
        if conflicts:
            summary += "\n⚠️  CONFLICTS DETECTED:\n"
            for task1, task2 in conflicts:
                summary += f"  • {task1.description} and {task2.description} overlap\n"
        
        return summary
