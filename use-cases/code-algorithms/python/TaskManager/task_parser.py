# task_parser.py
from datetime import datetime, timedelta
from models import Task, TaskPriority


def parse_task_from_text(text):
    """
    Parse free-form text to extract task properties.

    Examples of format it can parse:
    "Buy milk @shopping !2 #tomorrow"
    "Finish report for client XYZ !urgent #friday #work @project"

    Where:
    - Basic text is the task title
    - @tag adds a tag
    - !N sets priority (1=low, 2=medium, 3=high, 4=urgent)
    - !urgent/!high/!medium/!low sets priority by name
    - #date sets a due date
    """
    # Initialize defaults
    title_parts = []
    tags = []
    priority = TaskPriority.MEDIUM  # default priority
    due_date = None
    
    # Split text into tokens (words)
    tokens = text.split()
    
    # Process each token
    for token in tokens:
        if token.startswith('@'):
            # Extract tag (remove @ symbol)
            tag = token[1:]
            if tag:  # only add non-empty tags
                tags.append(tag)
        
        elif token.startswith('!'):
            # Extract priority
            priority_str = token[1:]
            parsed_priority = parse_priority(priority_str)
            if parsed_priority:
                priority = parsed_priority
        
        elif token.startswith('#'):
            # Extract due date
            date_str = token[1:]
            parsed_date = parse_due_date(date_str)
            if parsed_date:
                due_date = parsed_date
        
        else:
            # Regular word - part of title
            title_parts.append(token)
    
    # Reconstruct title from remaining words
    title = ' '.join(title_parts)
    
    # Create and return Task
    task = Task(title, priority=priority, due_date=due_date, tags=tags)
    return task


def parse_priority(priority_str):
    """
    Convert priority string to TaskPriority enum.
    
    Args:
        priority_str: String like "urgent", "4", "high", "3", etc.
    
    Returns:
        TaskPriority enum value or None if invalid
    """
    # Make case-insensitive
    priority_str = priority_str.lower()
    
    # Numeric mapping (1-4)
    priority_map_numeric = {
        '1': TaskPriority.LOW,
        '2': TaskPriority.MEDIUM,
        '3': TaskPriority.HIGH,
        '4': TaskPriority.URGENT
    }
    
    # Name mapping
    priority_map_names = {
        'low': TaskPriority.LOW,
        'medium': TaskPriority.MEDIUM,
        'high': TaskPriority.HIGH,
        'urgent': TaskPriority.URGENT
    }
    
    # Try numeric first, then names
    if priority_str in priority_map_numeric:
        return priority_map_numeric[priority_str]
    elif priority_str in priority_map_names:
        return priority_map_names[priority_str]
    else:
        return None  # Invalid priority, will use default


def parse_due_date(date_str):
    """
    Convert date keyword to actual datetime.
    
    Supported keywords:
    - today: current date at midnight
    - tomorrow: next day at midnight
    - next_week: 7 days from now at midnight
    - monday, tuesday, ..., sunday: next occurrence of that weekday
    - mon, tue, wed, thu, fri, sat, sun: abbreviated weekday names
    
    Args:
        date_str: String representation of date
    
    Returns:
        datetime object at midnight or None if invalid
    """
    date_str = date_str.lower()
    now = datetime.now()
    
    if date_str == 'today':
        return datetime(now.year, now.month, now.day, 0, 0, 0)
    
    elif date_str == 'tomorrow':
        tomorrow = now + timedelta(days=1)
        return datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0)
    
    elif date_str == 'next_week':
        next_week = now + timedelta(days=7)
        return datetime(next_week.year, next_week.month, next_week.day, 0, 0, 0)
    
    # Check if it's a weekday name
    elif date_str in ['monday', 'mon', 'tuesday', 'tue', 'wednesday', 'wed',
                      'thursday', 'thu', 'friday', 'fri', 'saturday', 'sat',
                      'sunday', 'sun']:
        weekday_num = weekday_name_to_number(date_str)
        return get_next_weekday(now, weekday_num)
    
    else:
        return None  # Unrecognized format


def get_next_weekday(current_date, target_weekday):
    """
    Calculate the next occurrence of a specific weekday.
    
    Args:
        current_date: datetime object representing current date/time
        target_weekday: int from 0-6 where 0=Monday, 6=Sunday
    
    Returns:
        datetime object of next occurrence at midnight
    
    Example:
        If today is Thursday (3) and target is Monday (0):
        - Calculate: (0 - 3) % 7 = 4 days ahead
        - Result: Next Monday
        
        If today is Thursday (3) and target is Thursday (3):
        - Calculate: (3 - 3) % 7 = 0, but we add 7
        - Result: Next Thursday (not today)
    """
    current_weekday = current_date.weekday()  # 0=Monday, 6=Sunday
    
    # Calculate days until target weekday
    days_ahead = (target_weekday - current_weekday) % 7
    
    # If target is today, get next week's occurrence instead
    if days_ahead == 0:
        days_ahead = 7
    
    # Add days to current date
    next_date = current_date + timedelta(days=days_ahead)
    
    # Return at midnight (00:00:00)
    return datetime(next_date.year, next_date.month, next_date.day, 0, 0, 0)


def weekday_name_to_number(weekday_name):
    """
    Convert weekday name (full or abbreviated) to number.
    
    Args:
        weekday_name: String like "monday", "mon", "tuesday", etc.
    
    Returns:
        int from 0-6 where 0=Monday, 6=Sunday
    """
    weekday_map = {
        'monday': 0, 'mon': 0,
        'tuesday': 1, 'tue': 1,
        'wednesday': 2, 'wed': 2,
        'thursday': 3, 'thu': 3,
        'friday': 4, 'fri': 4,
        'saturday': 5, 'sat': 5,
        'sunday': 6, 'sun': 6
    }
    
    return weekday_map.get(weekday_name.lower(), 0)  # Default to Monday if not found
