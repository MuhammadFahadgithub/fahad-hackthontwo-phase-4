import re
from typing import Dict, Any, Optional
from enum import Enum


class TaskOperation(Enum):
    ADD = "add_task"
    LIST = "list_tasks"
    COMPLETE = "complete_task"
    DELETE = "delete_task"
    UPDATE = "update_task"


class NaturalLanguageProcessor:
    """
    Processes natural language input to determine appropriate task operations
    """
    
    def __init__(self):
        # Patterns for identifying operations
        self.patterns = {
            TaskOperation.ADD: [
                r"add\s+(a\s+)?task\s+to\s+(.+)",
                r"create\s+(a\s+)?task\s+to\s+(.+)",
                r"make\s+(a\s+)?task\s+to\s+(.+)",
                r"add\s+(.+)",
                r"create\s+(.+)",
                r"i\s+need\s+to\s+(.+)",
                r"don't\s+forget\s+to\s+(.+)"
            ],
            TaskOperation.LIST: [
                r"show\s+(me\s+)?my\s+tasks?",
                r"list\s+(me\s+)?my\s+tasks?",
                r"what\s+do\s+i\s+need\s+to\s+do",
                r"what\s+are\s+(my\s+)?tasks?",
                r"display\s+(me\s+)?my\s+tasks?",
                r"view\s+(me\s+)?my\s+tasks?",
                r"see\s+(me\s+)?my\s+tasks?",
                r"show\s+(all\s+)?tasks?",
                r"list\s+(all\s+)?tasks?"
            ],
            TaskOperation.COMPLETE: [
                r"complete\s+task\s+(\d+)",
                r"mark\s+task\s+(\d+)\s+as\s+complete",
                r"finish\s+task\s+(\d+)",
                r"done\s+with\s+task\s+(\d+)",
                r"complete\s+(.+)",
                r"mark\s+(.+)\s+as\s+complete",
                r"finish\s+(.+)",
                r"i\s+finished\s+(.+)",
                r"i\s+completed\s+(.+)"
            ],
            TaskOperation.DELETE: [
                r"delete\s+task\s+(\d+)",
                r"remove\s+task\s+(\d+)",
                r"delete\s+(.+)",
                r"remove\s+(.+)",
                r"get\s+rid\s+of\s+(.+)",
                r"cancel\s+(.+)"
            ],
            TaskOperation.UPDATE: [
                r"change\s+task\s+(\d+)\s+to\s+(.+)",
                r"update\s+task\s+(\d+)\s+to\s+(.+)",
                r"modify\s+task\s+(\d+)\s+to\s+(.+)",
                r"change\s+(.+)\s+to\s+(.+)",
                r"update\s+(.+)\s+to\s+(.+)",
                r"rename\s+(.+)\s+to\s+(.+)"
            ]
        }
    
    def process_input(self, user_input: str) -> Dict[str, Any]:
        """
        Process natural language input and return the appropriate operation and parameters
        """
        user_input = user_input.strip()
        if not user_input:
            return {
                "operation": "unknown",
                "params": {"original_input": user_input},
                "message": "Empty input received. Please provide a command."
            }
        
        user_input_lower = user_input.lower()
        
        # Check each operation type
        for operation, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.search(pattern, user_input_lower)
                if match:
                    groups = match.groups()
                    
                    if operation == TaskOperation.ADD:
                        # Extract task description
                        if len(groups) >= 1:
                            description = groups[-1].strip()
                            if not description:
                                return {
                                    "operation": "unknown",
                                    "params": {"original_input": user_input},
                                    "message": "Task description cannot be empty. Please provide a valid task to add."
                                }
                            return {
                                "operation": operation.value,
                                "params": {"description": description}
                            }
                    
                    elif operation == TaskOperation.LIST:
                        # No additional params needed
                        return {
                            "operation": operation.value,
                            "params": {}
                        }
                    
                    elif operation == TaskOperation.COMPLETE:
                        # Check if it's by ID or description
                        if len(groups) >= 1 and groups[0].isdigit():
                            task_id = groups[0]
                            if not task_id:
                                return {
                                    "operation": "unknown",
                                    "params": {"original_input": user_input},
                                    "message": "Task ID is required to complete a task."
                                }
                            return {
                                "operation": operation.value,
                                "params": {"task_id": task_id}
                            }
                        else:
                            # Complete by description
                            description = groups[0].strip() if groups and groups[0] else user_input_lower.replace("complete", "").replace("mark", "").replace("as complete", "").replace("finish", "").replace("i finished", "").replace("i completed", "").strip()
                            if not description:
                                return {
                                    "operation": "unknown",
                                    "params": {"original_input": user_input},
                                    "message": "Task description is required to complete a task."
                                }
                            return {
                                "operation": operation.value,
                                "params": {"description": description}
                            }
                    
                    elif operation == TaskOperation.DELETE:
                        # Check if it's by ID or description
                        if len(groups) >= 1 and groups[0].isdigit():
                            task_id = groups[0]
                            if not task_id:
                                return {
                                    "operation": "unknown",
                                    "params": {"original_input": user_input},
                                    "message": "Task ID is required to delete a task."
                                }
                            return {
                                "operation": operation.value,
                                "params": {"task_id": task_id}
                            }
                        else:
                            # Delete by description
                            description = groups[0].strip() if groups and groups[0] else user_input_lower.replace("delete", "").replace("remove", "").replace("get rid of", "").replace("cancel", "").strip()
                            if not description:
                                return {
                                    "operation": "unknown",
                                    "params": {"original_input": user_input},
                                    "message": "Task description is required to delete a task."
                                }
                            return {
                                "operation": operation.value,
                                "params": {"description": description}
                            }
                    
                    elif operation == TaskOperation.UPDATE:
                        # Extract task ID and new description
                        if len(groups) >= 2 and groups[0].isdigit():
                            task_id = groups[0]
                            new_description = groups[1].strip()
                            if not task_id:
                                return {
                                    "operation": "unknown",
                                    "params": {"original_input": user_input},
                                    "message": "Task ID is required to update a task."
                                }
                            if not new_description:
                                return {
                                    "operation": "unknown",
                                    "params": {"original_input": user_input},
                                    "message": "New task description is required to update a task."
                                }
                            return {
                                "operation": operation.value,
                                "params": {
                                    "task_id": task_id,
                                    "description": new_description
                                }
                            }
                        else:
                            # Update by description - extract old and new descriptions
                            if len(groups) >= 2:
                                old_description = groups[0].strip()
                                new_description = groups[1].strip()
                                if not old_description or not new_description:
                                    return {
                                        "operation": "unknown",
                                        "params": {"original_input": user_input},
                                        "message": "Both old and new task descriptions are required for update."
                                    }
                                return {
                                    "operation": operation.value,
                                    "params": {
                                        "old_description": old_description,
                                        "new_description": new_description
                                    }
                                }
        
        # If no pattern matched, return a default response
        return {
            "operation": "unknown",
            "params": {"original_input": user_input},
            "message": "I didn't understand that command. Try phrases like 'add a task to buy groceries' or 'show my tasks'."
        }
    
    def extract_task_id_from_description(self, description: str, user_tasks: list) -> Optional[str]:
        """
        Helper method to extract task ID when only description is provided
        """
        # Look for the task by description in the user's tasks
        for task in user_tasks:
            if description.lower() in task.get('description', '').lower():
                return task.get('id')
        return None