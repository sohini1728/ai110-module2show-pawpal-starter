"""
PawPal+ Demo Script - CLI demonstration of the scheduling system.
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    """Run a demonstration of the PawPal+ system."""
    
    print("\n" + "=" * 50)
    print("🐾 PawPal+ System Demo")
    print("=" * 50 + "\n")
    
    # Create an owner
    print("1️⃣  Creating owner...")
    owner = Owner("Sarah", availability_hours="08:00-22:00")
    print(f"   ✓ Owner created: {owner.name}\n")
    
    # Create pets
    print("2️⃣  Creating pets...")
    fido = Pet("Fido", "dog", age=5, special_needs="Needs daily exercise")
    whiskers = Pet("Whiskers", "cat", age=3)
    owner.add_pet(fido)
    owner.add_pet(whiskers)
    print(f"   ✓ Added: {fido}")
    print(f"   ✓ Added: {whiskers}\n")
    
    # Add tasks to Fido
    print("3️⃣  Adding tasks to Fido...")
    fido.add_task(Task("Morning walk", "08:00", 30, "high", "daily"))
    fido.add_task(Task("Breakfast", "08:30", 15, "high", "daily"))
    fido.add_task(Task("Midday walk", "12:00", 20, "medium", "daily"))
    fido.add_task(Task("Lunch", "12:30", 15, "high", "daily"))
    fido.add_task(Task("Evening walk", "18:00", 30, "high", "daily"))
    fido.add_task(Task("Dinner", "18:30", 15, "high", "daily"))
    fido.add_task(Task("Playtime", "19:00", 45, "medium", "daily"))
    print(f"   ✓ Added {fido.get_task_count()} tasks\n")
    
    # Add tasks to Whiskers
    print("4️⃣  Adding tasks to Whiskers...")
    whiskers.add_task(Task("Breakfast", "08:00", 10, "high", "daily"))
    whiskers.add_task(Task("Lunch", "12:00", 10, "high", "daily"))
    whiskers.add_task(Task("Dinner", "18:00", 10, "high", "daily"))
    whiskers.add_task(Task("Litter box check", "09:00", 5, "medium", "daily"))
    whiskers.add_task(Task("Playtime", "20:00", 20, "medium", "daily"))
    print(f"   ✓ Added {whiskers.get_task_count()} tasks\n")
    
    # Create scheduler
    print("5️⃣  Creating scheduler...")
    scheduler = Scheduler(owner)
    print(f"   ✓ Scheduler initialized for {owner.name}\n")
    
    # Display today's schedule
    print("6️⃣  Displaying today's schedule (sorted by time)...\n")
    print(scheduler.get_schedule_summary())
    
    # Show tasks sorted by priority
    print("\n7️⃣  Tasks sorted by priority (High → Medium → Low)...\n")
    all_tasks = owner.get_all_tasks()
    priority_sorted = scheduler.sort_by_priority(all_tasks)
    print("High Priority Tasks:")
    for task in scheduler.filter_by_priority(priority_sorted, "high"):
        print(f"  {task}")
    print("\nMedium Priority Tasks:")
    for task in scheduler.filter_by_priority(priority_sorted, "medium"):
        print(f"  {task}")
    
    # Detect conflicts
    print("\n8️⃣  Checking for task conflicts...\n")
    conflicts = scheduler.detect_conflicts(all_tasks)
    if conflicts:
        print("⚠️  CONFLICTS FOUND:")
        for task1, task2 in conflicts:
            print(f"  • '{task1.description}' ({task1.time}-{task1.get_end_time()}) overlaps with")
            print(f"    '{task2.description}' ({task2.time}-{task2.get_end_time()})")
    else:
        print("✓ No conflicts detected. Schedule looks good!")
    
    # Test recurring task logic
    print("\n9️⃣  Testing recurring task logic...\n")
    print(f"Current task count: {fido.get_task_count()}")
    morning_walk = fido.get_tasks()[0]  # Get first task (morning walk)
    print(f"Marking '{morning_walk.description}' as complete...")
    new_task = scheduler.mark_task_complete(morning_walk)
    print(f"New recurring task created: {new_task}")
    print(f"Updated task count: {fido.get_task_count()}\n")
    
    # Show available time slots
    print("🔟  Finding available time slots for a 60-minute activity...\n")
    available = scheduler.get_available_time_slots(60)
    if available:
        print("Available time slots:")
        for start, end in available:
            print(f"  • {start} to {end}")
    else:
        print("No large time slots available.")
    
    # Summary statistics
    print("\n" + "=" * 50)
    print("📊 Summary Statistics")
    print("=" * 50)
    print(f"Owner: {owner.name}")
    print(f"Pets: {len(owner.get_pets())}")
    print(f"Total tasks: {owner.get_task_count()}")
    print(f"Incomplete tasks: {len(owner.get_all_tasks(completed=False))}")
    print(f"Completed tasks: {len(owner.get_all_tasks(completed=True))}")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
