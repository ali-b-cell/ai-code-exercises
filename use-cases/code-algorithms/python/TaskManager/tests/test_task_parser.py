import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from models import TaskPriority
from parser import parse_task_from_text, get_next_weekday


class TaskParserTest(unittest.TestCase):
    def test_parse_basic_task(self):
        """Test parsing a basic task with no special markers."""
        task = parse_task_from_text("Buy milk")
        
        self.assertEqual(task.title, "Buy milk")
        self.assertEqual(task.priority, TaskPriority.MEDIUM)
        self.assertIsNone(task.due_date)
        self.assertEqual(task.tags, [])

    def test_parse_task_with_priority_number(self):
        """Test parsing a task with numeric priority markers."""
        task = parse_task_from_text("Buy milk !1")
        self.assertEqual(task.title, "Buy milk")
        self.assertEqual(task.priority, TaskPriority.LOW)
        
        task = parse_task_from_text("Buy milk !2")
        self.assertEqual(task.title, "Buy milk")
        self.assertEqual(task.priority, TaskPriority.MEDIUM)
        
        task = parse_task_from_text("Buy milk !3")
        self.assertEqual(task.title, "Buy milk")
        self.assertEqual(task.priority, TaskPriority.HIGH)
        
        task = parse_task_from_text("Buy milk !4")
        self.assertEqual(task.title, "Buy milk")
        self.assertEqual(task.priority, TaskPriority.URGENT)

    def test_parse_task_with_priority_name(self):
        """Test parsing a task with named priority markers."""
        task = parse_task_from_text("Buy milk !low")
        self.assertEqual(task.title, "Buy milk")
        self.assertEqual(task.priority, TaskPriority.LOW)
        
        task = parse_task_from_text("Buy milk !medium")
        self.assertEqual(task.title, "Buy milk")
        self.assertEqual(task.priority, TaskPriority.MEDIUM)
        
        task = parse_task_from_text("Buy milk !high")
        self.assertEqual(task.title, "Buy milk")
        self.assertEqual(task.priority, TaskPriority.HIGH)
        
        task = parse_task_from_text("Buy milk !urgent")
        self.assertEqual(task.title, "Buy milk")
        self.assertEqual(task.priority, TaskPriority.URGENT)

    def test_parse_task_with_tags(self):
        """Test parsing a task with tags."""
        task = parse_task_from_text("Buy milk @shopping @groceries")
        
        self.assertEqual(task.title, "Buy milk")
        self.assertIn("shopping", task.tags)
        self.assertIn("groceries", task.tags)
        self.assertEqual(len(task.tags), 2)

    def test_parse_complex_task(self):
        """Test parsing a complex task with multiple markers."""
        task = parse_task_from_text("Buy milk @shopping @groceries !urgent #tomorrow")
        
        self.assertEqual(task.title, "Buy milk")
        self.assertEqual(task.priority, TaskPriority.URGENT)
        self.assertIn("shopping", task.tags)
        self.assertIn("groceries", task.tags)
        self.assertEqual(len(task.tags), 2)
        self.assertIsNotNone(task.due_date)


if __name__ == '__main__':
    unittest.main()
