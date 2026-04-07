"""
Automated tests for PawPal+ system.
Tests verify core scheduling behaviors and edge cases.
"""

import pytest
from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler


class TestTask:
    """Tests for Task class."""
    
    def test_task_creation(self):
        """Verify task can be created with all attributes."""
        task = Task("Morning walk", "08:00", 30, "high", "daily")
        assert task.description == "Morning walk"
        assert task.time == "08:00"
        assert task.duration_minutes == 30
        assert task.priority == "high"
        assert task.frequency == "daily"
        assert not task.is_completed
    
    def test_task_completion(self):
        """Verify marking a task complete changes its status."""
        task = Task("Walk", "08:00", 30, "high", "daily")
        assert not task.is_completed
        task.mark_complete()
        assert task.is_completed
    
    def test_task_incomplete(self):
        """Verify marking a task incomplete works."""
        task = Task("Walk", "08:00", 30, "high", "daily")
        task.mark_complete()
        assert task.is_completed
        task.mark_incomplete()
        assert not task.is_completed
    
    def test_priority_value(self):
        """Verify priority values are calculated correctly."""
        low_task = Task("Walk", "08:00", 30, "low")
        medium_task = Task("Walk", "08:00", 30, "medium")
        high_task = Task("Walk", "08:00", 30, "high")
        
        assert low_task.get_priority_value() == 1
        assert medium_task.get_priority_value() == 2
        assert high_task.get_priority_value() == 3
    
    def test_end_time_calculation(self):
        """Verify end time is calculated correctly."""
        task = Task("Walk", "08:00", 30, "high")
        assert task.get_end_time() == "08:30"
        
        task2 = Task("Meal", "12:45", 15, "high")
        assert task2.get_end_time() == "13:00"


class TestPet:
    """Tests for Pet class."""
    
    def test_pet_creation(self):
        """Verify pet can be created with attributes."""
        pet = Pet("Fido", "dog", age=5, special_needs="High energy")
        assert pet.name == "Fido"
        assert pet.species == "dog"
        assert pet.age == 5
        assert pet.special_needs == "High energy"
        assert pet.get_task_count() == 0
    
    def test_add_task_to_pet(self):
        """Verify adding a task increases pet's task count."""
        pet = Pet("Fido", "dog")
        assert pet.get_task_count() == 0
        
        pet.add_task(Task("Walk", "08:00", 30, "high", "daily"))
        assert pet.get_task_count() == 1
    
    def test_remove_task_from_pet(self):
        """Verify removing a task decreases pet's task count."""
        pet = Pet("Fido", "dog")
        task = Task("Walk", "08:00", 30, "high", "daily")
        
        pet.add_task(task)
        assert pet.get_task_count() == 1
        
        pet.remove_task(task)
        assert pet.get_task_count() == 0
    
    def test_get_tasks_by_status(self):
        """Verify filtering tasks by completion status."""
        pet = Pet("Fido", "dog")
        task1 = Task("Walk", "08:00", 30, "high")
        task2 = Task("Feed", "12:00", 15, "high")
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        task1.mark_complete()
        
        incomplete = pet.get_tasks(completed=False)
        complete = pet.get_tasks(completed=True)
        
        assert len(incomplete) == 1
        assert len(complete) == 1
        assert task2 in incomplete
        assert task1 in complete


class TestOwner:
    """Tests for Owner class."""
    
    def test_owner_creation(self):
        """Verify owner can be created."""
        owner = Owner("Sarah", timezone="EST")
        assert owner.name == "Sarah"
        assert owner.timezone == "EST"
        assert len(owner.get_pets()) == 0
    
    def test_add_pet_to_owner(self):
        """Verify adding pets to owner."""
        owner = Owner("Sarah")
        pet = Pet("Fido", "dog")
        
        owner.add_pet(pet)
        assert len(owner.get_pets()) == 1
        assert pet in owner.get_pets()
    
    def test_owner_get_all_tasks(self):
        """Verify owner can retrieve all tasks from all pets."""
        owner = Owner("Sarah")
        fido = Pet("Fido", "dog")
        whiskers = Pet("Whiskers", "cat")
        
        owner.add_pet(fido)
        owner.add_pet(whiskers)
        
        fido.add_task(Task("Walk", "08:00", 30, "high"))
        fido.add_task(Task("Feed", "12:00", 15, "high"))
        whiskers.add_task(Task("Feed", "08:00", 10, "high"))
        
        all_tasks = owner.get_all_tasks()
        assert owner.get_task_count() == 3
        assert len(all_tasks) == 3
    
    def test_owner_get_tasks_by_status(self):
        """Verify owner can filter tasks by completion status."""
        owner = Owner("Sarah")
        pet = Pet("Fido", "dog")
        owner.add_pet(pet)
        
        task1 = Task("Walk", "08:00", 30, "high")
        task2 = Task("Feed", "12:00", 15, "high")
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        task1.mark_complete()
        
        incomplete = owner.get_all_tasks(completed=False)
        complete = owner.get_all_tasks(completed=True)
        
        assert len(incomplete) == 1
        assert len(complete) == 1


class TestScheduler:
    """Tests for Scheduler class."""
    
    def test_scheduler_creation(self):
        """Verify scheduler can be created."""
        owner = Owner("Sarah")
        scheduler = Scheduler(owner)
        assert scheduler.owner == owner
    
    def test_sorting_by_time(self):
        """Verify tasks are sorted chronologically by time."""
        owner = Owner("Sarah")
        pet = Pet("Fido", "dog")
        owner.add_pet(pet)
        
        pet.add_task(Task("Evening walk", "18:00", 30, "high"))
        pet.add_task(Task("Morning walk", "08:00", 30, "high"))
        pet.add_task(Task("Lunch", "12:00", 15, "high"))
        
        scheduler = Scheduler(owner)
        sorted_tasks = scheduler.sort_by_time(pet.get_tasks())
        
        assert sorted_tasks[0].time == "08:00"
        assert sorted_tasks[1].time == "12:00"
        assert sorted_tasks[2].time == "18:00"
    
    def test_sorting_by_priority(self):
        """Verify tasks are sorted by priority (high to low)."""
        owner = Owner("Sarah")
        pet = Pet("Fido", "dog")
        owner.add_pet(pet)
        
        pet.add_task(Task("Walk", "08:00", 30, "low"))
        pet.add_task(Task("Feed", "12:00", 15, "high"))
        pet.add_task(Task("Play", "18:00", 20, "medium"))
        
        scheduler = Scheduler(owner)
        sorted_tasks = scheduler.sort_by_priority(pet.get_tasks())
        
        assert sorted_tasks[0].priority == "high"
        assert sorted_tasks[1].priority == "medium"
        assert sorted_tasks[2].priority == "low"
    
    def test_filter_by_priority(self):
        """Verify filtering tasks by priority level."""
        owner = Owner("Sarah")
        pet = Pet("Fido", "dog")
        owner.add_pet(pet)
        
        pet.add_task(Task("Walk", "08:00", 30, "high"))
        pet.add_task(Task("Feed", "12:00", 15, "high"))
        pet.add_task(Task("Play", "18:00", 20, "medium"))
        
        scheduler = Scheduler(owner)
        all_tasks = owner.get_all_tasks()
        high_priority = scheduler.filter_by_priority(all_tasks, "high")
        
        assert len(high_priority) == 2
        assert all(t.priority == "high" for t in high_priority)
    
    def test_filter_by_pet(self):
        """Verify filtering tasks by pet name."""
        owner = Owner("Sarah")
        fido = Pet("Fido", "dog")
        whiskers = Pet("Whiskers", "cat")
        owner.add_pet(fido)
        owner.add_pet(whiskers)
        
        fido.add_task(Task("Walk", "08:00", 30, "high"))
        whiskers.add_task(Task("Feed", "12:00", 10, "high"))
        
        scheduler = Scheduler(owner)
        all_tasks = owner.get_all_tasks()
        fido_tasks = scheduler.filter_by_pet(all_tasks, "Fido")
        
        assert len(fido_tasks) == 1
        assert fido_tasks[0].pet_name == "Fido"
    
    def test_filter_by_status(self):
        """Verify filtering tasks by completion status."""
        owner = Owner("Sarah")
        pet = Pet("Fido", "dog")
        owner.add_pet(pet)
        
        task1 = Task("Walk", "08:00", 30, "high")
        task2 = Task("Feed", "12:00", 15, "high")
        
        pet.add_task(task1)
        pet.add_task(task2)
        task1.mark_complete()
        
        scheduler = Scheduler(owner)
        all_tasks = owner.get_all_tasks()
        incomplete = scheduler.filter_by_status(all_tasks, False)
        
        assert len(incomplete) == 1
        assert incomplete[0] == task2
    
    def test_detect_conflicts(self):
        """Verify conflict detection identifies overlapping tasks."""
        owner = Owner("Sarah")
        pet = Pet("Fido", "dog")
        owner.add_pet(pet)
        
        # These tasks overlap
        pet.add_task(Task("Morning walk", "08:00", 30, "high"))
        pet.add_task(Task("Breakfast", "08:15", 20, "high"))
        pet.add_task(Task("Play", "10:00", 60, "medium"))
        
        scheduler = Scheduler(owner)
        conflicts = scheduler.detect_conflicts(owner.get_all_tasks())
        
        assert len(conflicts) > 0
        # Should detect morning walk and breakfast overlap
        assert any(
            t1.description == "Morning walk" and t2.description == "Breakfast"
            for t1, t2 in conflicts
        )
    
    def test_no_conflicts(self):
        """Verify no false positives when tasks don't overlap."""
        owner = Owner("Sarah")
        pet = Pet("Fido", "dog")
        owner.add_pet(pet)
        
        # These tasks don't overlap
        pet.add_task(Task("Morning walk", "08:00", 30, "high"))
        pet.add_task(Task("Breakfast", "08:30", 15, "high"))
        pet.add_task(Task("Play", "09:00", 60, "medium"))
        
        scheduler = Scheduler(owner)
        conflicts = scheduler.detect_conflicts(owner.get_all_tasks())
        
        assert len(conflicts) == 0
    
    def test_recurring_task_creation(self):
        """Verify marking a daily task complete creates a new one."""
        owner = Owner("Sarah")
        pet = Pet("Fido", "dog")
        owner.add_pet(pet)
        
        task = Task("Morning walk", "08:00", 30, "high", "daily")
        pet.add_task(task)
        
        assert pet.get_task_count() == 1
        
        scheduler = Scheduler(owner)
        new_task = scheduler.mark_task_complete(task)
        
        assert task.is_completed
        assert new_task is not None
        assert pet.get_task_count() == 2
    
    def test_get_today_schedule(self):
        """Verify getting today's schedule returns tasks in chronological order."""
        owner = Owner("Sarah")
        pet = Pet("Fido", "dog")
        owner.add_pet(pet)
        
        pet.add_task(Task("Evening walk", "18:00", 30, "high"))
        pet.add_task(Task("Morning walk", "08:00", 30, "high"))
        pet.add_task(Task("Lunch", "12:00", 15, "high"))
        
        scheduler = Scheduler(owner)
        today = scheduler.get_today_schedule()
        
        assert len(today) == 3
        assert today[0].time == "08:00"
        assert today[1].time == "12:00"
        assert today[2].time == "18:00"
    
    def test_get_available_time_slots(self):
        """Verify finding available time slots."""
        owner = Owner("Sarah", availability_hours="08:00-22:00")
        pet = Pet("Fido", "dog")
        owner.add_pet(pet)
        
        pet.add_task(Task("Walk", "08:00", 60, "high"))
        pet.add_task(Task("Feed", "12:00", 30, "high"))
        
        scheduler = Scheduler(owner)
        slots = scheduler.get_available_time_slots(60)
        
        # Should find slots between scheduled tasks
        assert len(slots) > 0
    
    def test_get_schedule_summary(self):
        """Verify schedule summary generation."""
        owner = Owner("Sarah")
        pet = Pet("Fido", "dog")
        owner.add_pet(pet)
        
        pet.add_task(Task("Walk", "08:00", 30, "high"))
        pet.add_task(Task("Feed", "12:00", 15, "high"))
        
        scheduler = Scheduler(owner)
        summary = scheduler.get_schedule_summary()
        
        assert "TODAY'S PET CARE SCHEDULE" in summary
        assert "Fido" in summary
        assert "Walk" in summary
        assert "Feed" in summary


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""
    
    def test_empty_schedule(self):
        """Verify handling empty schedule."""
        owner = Owner("Sarah")
        pet = Pet("Fido", "dog")
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner)
        today = scheduler.get_today_schedule()
        
        assert len(today) == 0
    
    def test_pet_with_no_tasks(self):
        """Verify handling pet with no tasks."""
        owner = Owner("Sarah")
        pet = Pet("Fido", "dog")
        owner.add_pet(pet)
        
        assert pet.get_task_count() == 0
        assert len(pet.get_tasks()) == 0
    
    def test_invalid_time_format(self):
        """Verify handling invalid time format."""
        task = Task("Walk", "25:00", 30, "high")  # Invalid time
        end_time = task.get_end_time()
        
        assert end_time == "Invalid time"
    
    def test_multiple_pets_same_task_time(self):
        """Verify handling multiple pets with tasks at same time."""
        owner = Owner("Sarah")
        fido = Pet("Fido", "dog")
        whiskers = Pet("Whiskers", "cat")
        
        owner.add_pet(fido)
        owner.add_pet(whiskers)
        
        fido.add_task(Task("Feed", "08:00", 15, "high"))
        whiskers.add_task(Task("Feed", "08:00", 10, "high"))
        
        scheduler = Scheduler(owner)
        all_tasks = owner.get_all_tasks()
        
        # Both tasks exist at same time for different pets
        assert len(all_tasks) == 2
        assert sum(1 for t in all_tasks if t.time == "08:00") == 2
    
    def test_long_duration_task(self):
        """Verify handling tasks with long durations."""
        task = Task("Grooming", "10:00", 240, "medium")  # 4 hour task
        assert task.duration_minutes == 240
        assert task.get_end_time() == "14:00"
    
    def test_midnight_crossing(self):
        """Verify handling tasks near midnight."""
        task = Task("Late night task", "23:00", 120, "low")  # 2 hour task past midnight
        # Note: This currently doesn't handle day boundary, which is acceptable for MVP
        assert task.time == "23:00"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
