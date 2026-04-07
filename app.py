"""import streamlit as st

PawPal+ Streamlit Application

A pet care management system that helps owners plan daily tasks.st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

"""

st.title("🐾 PawPal+")

import streamlit as st

from pawpal_system import Owner, Pet, Task, Schedulerst.markdown(

    """

Welcome to the PawPal+ starter app.

def initialize_session_state():

    """Initialize session state for persistent data."""This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,

    if "owner" not in st.session_state:but **it does not implement the project logic**. Your job is to design the system and build it.

        st.session_state.owner = None

    if "pets" not in st.session_state:Use this app as your interactive demo once your backend classes/functions exist.

        st.session_state.pets = {}"""

    if "scheduler" not in st.session_state:)

        st.session_state.scheduler = None

with st.expander("Scenario", expanded=True):

    st.markdown(

def create_owner_section():        """

    """Handle owner creation and configuration."""**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks

    st.subheader("👤 Owner Information")for their pet(s) based on constraints like time, priority, and preferences.

    

    owner_name = st.text_input(You will design and implement the scheduling logic and connect it to this Streamlit UI.

        "Owner name","""

        value=st.session_state.owner.name if st.session_state.owner else "Jordan",    )

        key="owner_name_input"

    )with st.expander("What you need to build", expanded=True):

        st.markdown(

    timezone = st.selectbox(        """

        "Timezone",At minimum, your system should:

        ["UTC", "EST", "CST", "MST", "PST", "GMT", "IST"],- Represent pet care tasks (what needs to happen, how long it takes, priority)

        index=0- Represent the pet and the owner (basic info and preferences)

    )- Build a plan/schedule for a day that chooses and orders tasks based on constraints

    - Explain the plan (why each task was chosen and when it happens)

    availability = st.text_input("""

        "Daily availability window (HH:MM-HH:MM)",    )

        value="08:00-22:00",

        help="When are you available to do pet care tasks?"st.divider()

    )

    st.subheader("Quick Demo Inputs (UI only)")

    if st.button("Create/Update Owner", key="create_owner"):owner_name = st.text_input("Owner name", value="Jordan")

        owner = Owner(owner_name, timezone=timezone, availability_hours=availability)pet_name = st.text_input("Pet name", value="Mochi")

        st.session_state.owner = ownerspecies = st.selectbox("Species", ["dog", "cat", "other"])

        st.session_state.scheduler = Scheduler(owner)

        st.success(f"✓ Owner '{owner_name}' created!")st.markdown("### Tasks")

        st.rerun()st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

    

    return st.session_state.ownerif "tasks" not in st.session_state:

    st.session_state.tasks = []



def create_pet_section():col1, col2, col3 = st.columns(3)

    """Handle pet creation."""with col1:

    if not st.session_state.owner:    task_title = st.text_input("Task title", value="Morning walk")

        st.warning("Please create an owner first.")with col2:

        return    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)

    with col3:

    st.subheader("🐾 Add a New Pet")    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    

    col1, col2 = st.columns(2)if st.button("Add task"):

    with col1:    st.session_state.tasks.append(

        pet_name = st.text_input("Pet name", value="Mochi", key="pet_name_input")        {"title": task_title, "duration_minutes": int(duration), "priority": priority}

    with col2:    )

        species = st.selectbox("Species", ["dog", "cat", "rabbit", "bird", "other"], key="species_select")

    if st.session_state.tasks:

    col3, col4 = st.columns(2)    st.write("Current tasks:")

    with col3:    st.table(st.session_state.tasks)

        age = st.number_input("Age (years)", min_value=0, max_value=50, value=3, key="age_input")else:

    with col4:    st.info("No tasks yet. Add one above.")

        special_needs = st.text_input("Special needs (optional)", value="", key="special_needs_input")

    st.divider()

    if st.button("Add Pet", key="add_pet_btn"):

        pet = Pet(pet_name, species, age=age if age > 0 else None, special_needs=special_needs)st.subheader("Build Schedule")

        st.session_state.owner.add_pet(pet)st.caption("This button should call your scheduling logic once you implement it.")

        st.session_state.pets[pet_name] = pet

        st.success(f"✓ {pet_name} ({species}) added!")if st.button("Generate schedule"):

        st.rerun()    st.warning(

            "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."

    # Display current pets    )

    if st.session_state.owner.get_pets():    st.markdown(

        st.markdown("**Current Pets:**")        """

        for pet in st.session_state.owner.get_pets():Suggested approach:

            col1, col2 = st.columns([3, 1])1. Design your UML (draft).

            with col1:2. Create class stubs (no logic).

                st.write(f"🐾 {pet.name} ({pet.species})" + (f" - {pet.special_needs}" if pet.special_needs else ""))3. Implement scheduling behavior.

            with col2:4. Connect your scheduler here and display results.

                if st.button("Remove", key=f"remove_pet_{pet.name}"):"""

                    st.session_state.owner.remove_pet(pet)    )

                    if pet.name in st.session_state.pets:
                        del st.session_state.pets[pet.name]
                    st.rerun()


def add_task_section():
    """Handle task creation."""
    if not st.session_state.owner or not st.session_state.owner.get_pets():
        st.warning("Please create an owner and at least one pet first.")
        return
    
    st.subheader("📝 Add a Task")
    
    pet_name = st.selectbox(
        "Select pet for this task",
        [p.name for p in st.session_state.owner.get_pets()],
        key="task_pet_select"
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        task_time = st.text_input("Time (HH:MM)", value="10:00", key="task_time_input")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=480, value=30, key="task_duration")
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="task_priority")
    
    col4, col5 = st.columns(2)
    with col4:
        description = st.text_input("Task description", value="Care task", key="task_description")
    with col5:
        frequency = st.selectbox("Frequency", ["one_time", "daily", "weekly"], key="task_frequency")
    
    if st.button("Add Task", key="add_task_btn"):
        try:
            pet = next(p for p in st.session_state.owner.get_pets() if p.name == pet_name)
            task = Task(description, task_time, duration, priority, frequency)
            pet.add_task(task)
            st.success(f"✓ Task '{description}' added to {pet_name}!")
            st.rerun()
        except ValueError as e:
            st.error(f"Invalid time format. Use HH:MM (e.g., 10:30)")


def display_schedule_section():
    """Display the day's schedule."""
    if not st.session_state.owner or not st.session_state.scheduler:
        st.warning("Please create an owner first.")
        return
    
    st.subheader("📋 Today's Schedule")
    
    all_tasks = st.session_state.owner.get_all_tasks(completed=False)
    
    if not all_tasks:
        st.info("No tasks scheduled for today. Add one above!")
        return
    
    scheduler = st.session_state.scheduler
    sorted_tasks = scheduler.sort_by_time(all_tasks)
    
    # Display schedule by pet
    for pet in st.session_state.owner.get_pets():
        pet_tasks = [t for t in sorted_tasks if t.pet_name == pet.name]
        if pet_tasks:
            with st.expander(f"🐾 {pet.name}", expanded=True):
                for task in pet_tasks:
                    col1, col2, col3, col4 = st.columns([2, 2, 3, 1])
                    with col1:
                        st.write(f"**{task.time}**")
                    with col2:
                        priority_colors = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                        st.write(f"{priority_colors.get(task.priority, '⚪')} {task.priority.upper()}")
                    with col3:
                        st.write(task.description)
                    with col4:
                        duration = f"{task.duration_minutes}m"
                        st.write(duration)
    
    # Conflict detection
    st.markdown("---")
    conflicts = scheduler.detect_conflicts(all_tasks)
    if conflicts:
        st.warning("⚠️ **Schedule Conflicts Detected:**")
        for task1, task2 in conflicts:
            st.write(f"• '{task1.description}' ({task1.time}-{task1.get_end_time()}) overlaps with")
            st.write(f"  '{task2.description}' ({task2.time}-{task2.get_end_time()})")
    else:
        st.success("✓ No schedule conflicts detected!")


def display_analytics_section():
    """Display schedule analytics and insights."""
    if not st.session_state.owner or not st.session_state.owner.get_pets():
        return
    
    st.subheader("📊 Analytics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    all_tasks = st.session_state.owner.get_all_tasks()
    incomplete_tasks = st.session_state.owner.get_all_tasks(completed=False)
    completed_tasks = st.session_state.owner.get_all_tasks(completed=True)
    
    with col1:
        st.metric("Total Tasks", len(all_tasks))
    with col2:
        st.metric("Today's Tasks", len(incomplete_tasks))
    with col3:
        st.metric("Completed", len(completed_tasks))
    with col4:
        st.metric("Pets", len(st.session_state.owner.get_pets()))
    
    # Priority breakdown
    if all_tasks:
        st.markdown("**Tasks by Priority:**")
        scheduler = st.session_state.scheduler
        high = len(scheduler.filter_by_priority(all_tasks, "high"))
        medium = len(scheduler.filter_by_priority(all_tasks, "medium"))
        low = len(scheduler.filter_by_priority(all_tasks, "low"))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"🔴 High: {high}")
        with col2:
            st.write(f"🟡 Medium: {medium}")
        with col3:
            st.write(f"🟢 Low: {low}")


def main():
    """Main Streamlit application."""
    st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")
    
    st.title("🐾 PawPal+")
    st.markdown("**Your smart pet care planning assistant**")
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar for navigation
    page = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Setup", "Schedule", "Tasks", "Analytics"]
    )
    
    if page == "Dashboard":
        st.markdown("---")
        if st.session_state.owner:
            col1, col2 = st.columns([2, 1])
            with col1:
                st.info(f"Welcome back, **{st.session_state.owner.name}**! 👋")
            with col2:
                if st.session_state.owner.get_pets():
                    for pet in st.session_state.owner.get_pets():
                        st.write(f"🐾 {pet.name}")
        else:
            st.info("👈 Start by setting up your profile on the Setup tab!")
        
        display_schedule_section()
        st.markdown("---")
        display_analytics_section()
    
    elif page == "Setup":
        st.markdown("---")
        st.markdown("### Owner Setup")
        create_owner_section()
        
        st.markdown("---")
        st.markdown("### Pet Management")
        create_pet_section()
    
    elif page == "Schedule":
        st.markdown("---")
        if st.session_state.owner:
            st.markdown(f"### {st.session_state.owner.name}'s Pet Care Schedule")
            display_schedule_section()
        else:
            st.warning("Please create an owner first on the Setup tab.")
    
    elif page == "Tasks":
        st.markdown("---")
        st.markdown("### Manage Tasks")
        add_task_section()
        
        st.markdown("---")
        st.subheader("📝 All Tasks")
        if st.session_state.owner and st.session_state.owner.get_all_tasks():
            all_tasks = st.session_state.owner.get_all_tasks()
            scheduler = st.session_state.scheduler
            
            filter_col1, filter_col2 = st.columns(2)
            with filter_col1:
                filter_priority = st.selectbox("Filter by priority", ["all", "high", "medium", "low"])
            with filter_col2:
                filter_status = st.selectbox("Filter by status", ["incomplete", "completed", "all"])
            
            # Apply filters
            filtered_tasks = all_tasks
            if filter_priority != "all":
                filtered_tasks = scheduler.filter_by_priority(filtered_tasks, filter_priority)
            
            if filter_status == "incomplete":
                filtered_tasks = scheduler.filter_by_status(filtered_tasks, False)
            elif filter_status == "completed":
                filtered_tasks = scheduler.filter_by_status(filtered_tasks, True)
            
            # Display filtered tasks
            for task in filtered_tasks:
                with st.container():
                    col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 1])
                    with col1:
                        status = "✅" if task.is_completed else "○"
                        st.write(status)
                    with col2:
                        st.write(f"**{task.pet_name}**")
                    with col3:
                        st.write(task.description)
                    with col4:
                        st.write(f"{task.time} ({task.duration_minutes}m)")
                    with col5:
                        if not task.is_completed:
                            if st.button("✓", key=f"complete_{id(task)}"):
                                scheduler.mark_task_complete(task)
                                st.success("Task completed!")
                                st.rerun()
        else:
            st.info("No tasks yet. Add one in the 'Tasks' section above.")
    
    elif page == "Analytics":
        st.markdown("---")
        display_analytics_section()
        
        if st.session_state.owner and st.session_state.scheduler:
            st.markdown("---")
            st.subheader("⏰ Available Time Slots")
            scheduler = st.session_state.scheduler
            duration = st.slider("Look for slots of at least (minutes)", min_value=15, max_value=120, value=60)
            available_slots = scheduler.get_available_time_slots(duration)
            
            if available_slots:
                st.write(f"Found {len(available_slots)} available slots:")
                for start, end in available_slots:
                    st.write(f"• {start} to {end}")
            else:
                st.info("No available slots found for the specified duration.")


if __name__ == "__main__":
    main()
