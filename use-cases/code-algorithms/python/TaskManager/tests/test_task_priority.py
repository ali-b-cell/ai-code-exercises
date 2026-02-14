import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from models import Task, TaskStatus, TaskPriority
from scoring import calculate_task_score, sort_tasks_by_importance, get_top_priority_tasks


class TaskPriorityTest(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.now = datetime.now()
        
        self.low_task = Task("Low Priority Task", priority=TaskPriority.LOW)
        self.medium_task = Task("Medium Priority Task", priority=TaskPriority.MEDIUM)
        self.high_task = Task("High Priority Task", priority=TaskPriority.HIGH)
        self.urgent_task = Task("Urgent Priority Task", priority=TaskPriority.URGENT)
        
        for task in [self.low_task, self.medium_task, self.high_task, self.urgent_task]:
            task.created_at = self.now
            task.updated_at = self.now

    @patch('scoring.datetime')
    def test_calculate_task_score_priority_weights(self, mock_datetime):
        """Test that calculate_task_score correctly applies priority weights."""
        mock_datetime.now.return_value = self.now
        
        low_score = calculate_task_score(self.low_task)
        medium_score = calculate_task_score(self.medium_task)
        high_score = calculate_task_score(self.high_task)
        urgent_score = calculate_task_score(self.urgent_task)
        
        self.assertLess(low_score, medium_score)
        self.assertLess(medium_score, high_score)
        self.assertLess(high_score, urgent_score)

    def test_sort_tasks_by_importance(self):
        """Test that sort_tasks_by_importance correctly sorts tasks."""
        task1 = Task("High Priority", priority=TaskPriority.HIGH)
        task2 = Task("Medium Priority Due Soon", priority=TaskPriority.MEDIUM)
        task2.due_date = datetime.now() + timedelta(days=1)
        
        task3 = Task("Low Priority Overdue", priority=TaskPriority.LOW)
        task3.due_date = datetime.now() - timedelta(days=1)
        
        task4 = Task("Medium Priority Done", priority=TaskPriority.MEDIUM)
        task4.status = TaskStatus.DONE
        
        task5 = Task("Urgent Priority", priority=TaskPriority.URGENT)
        
        tasks = [task1, task2, task3, task4, task5]
        sorted_tasks = sort_tasks_by_importance(tasks)
        
        self.assertEqual("Urgent Priority", sorted_tasks[0].title)

    def test_get_top_priority_tasks(self):
        """Test that get_top_priority_tasks returns correct number of tasks."""
        tasks = [
            Task("Task 1", priority=TaskPriority.MEDIUM),
            Task("Task 2", priority=TaskPriority.HIGH),
            Task("Task 3", priority=TaskPriority.LOW),
            Task("Task 4", priority=TaskPriority.URGENT),
            Task("Task 5", priority=TaskPriority.MEDIUM),
        ]
        
        top_tasks = get_top_priority_tasks(tasks, limit=3)
        self.assertEqual(len(top_tasks), 3)
        self.assertEqual(top_tasks[0].title, "Task 4")


if __name__ == '__main__':
    unittest.main()
