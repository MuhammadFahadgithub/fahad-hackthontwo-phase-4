from typing import Dict, Any
from ..services.task_service import TaskService
from ..models.task import TaskCreate, TaskUpdate
from sqlmodel import Session


class MCPTaskTools:
    """
    MCP (Model Context Protocol) tools for task operations
    """
    
    def __init__(self, session: Session):
        self.session = session
        self.task_service = TaskService()
    
    def add_task(self, user_id: str, description: str) -> Dict[str, Any]:
        """
        MCP tool to add a new task
        """
        try:
            # Validate inputs
            if not user_id:
                return {
                    "status": "error",
                    "message": "User ID is required to add a task"
                }
            
            if not description or not description.strip():
                return {
                    "status": "error",
                    "message": "Task description cannot be empty"
                }
            
            # Truncate description if too long (based on model validation)
            if len(description) > 500:
                description = description[:500]
            
            task_create = TaskCreate(user_id=user_id, description=description.strip())
            task = self.task_service.create_task(self.session, task_create)
            
            if task:
                return {
                    "status": "success",
                    "task_id": task.id,
                    "description": task.description,
                    "message": f"Task '{task.description}' added successfully"
                }
            else:
                return {
                    "status": "error",
                    "message": "Failed to create task"
                }
        except ValueError as ve:
            return {
                "status": "error",
                "message": f"Validation error: {str(ve)}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to add task: {str(e)}"
            }
    
    def list_tasks(self, user_id: str) -> Dict[str, Any]:
        """
        MCP tool to list all tasks for a user
        """
        try:
            # Validate inputs
            if not user_id:
                return {
                    "status": "error",
                    "message": "User ID is required to list tasks"
                }
            
            tasks = self.task_service.get_user_tasks(self.session, user_id)
            
            return {
                "status": "success",
                "tasks": [
                    {
                        "id": task.id,
                        "description": task.description,
                        "completed": task.completed
                    } for task in tasks
                ],
                "count": len(tasks),
                "message": f"Retrieved {len(tasks)} tasks"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to list tasks: {str(e)}"
            }
    
    def complete_task(self, user_id: str, task_id: str) -> Dict[str, Any]:
        """
        MCP tool to mark a task as complete
        """
        try:
            # Validate inputs
            if not user_id:
                return {
                    "status": "error",
                    "message": "User ID is required to complete a task"
                }
            
            if not task_id:
                return {
                    "status": "error",
                    "message": "Task ID is required to complete a task"
                }
            
            task = self.task_service.complete_task(self.session, task_id, user_id)
            if task:
                return {
                    "status": "success",
                    "task_id": task.id,
                    "message": f"Task '{task.description}' marked as complete"
                }
            else:
                return {
                    "status": "error",
                    "message": f"Task with ID '{task_id}' not found or you don't have permission to modify it"
                }
        except ValueError as ve:
            return {
                "status": "error",
                "message": f"Validation error: {str(ve)}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to complete task: {str(e)}"
            }
    
    def delete_task(self, user_id: str, task_id: str) -> Dict[str, Any]:
        """
        MCP tool to delete a task
        """
        try:
            # Validate inputs
            if not user_id:
                return {
                    "status": "error",
                    "message": "User ID is required to delete a task"
                }
            
            if not task_id:
                return {
                    "status": "error",
                    "message": "Task ID is required to delete a task"
                }
            
            success = self.task_service.delete_task(self.session, task_id, user_id)
            if success:
                return {
                    "status": "success",
                    "task_id": task_id,
                    "message": "Task deleted successfully"
                }
            else:
                return {
                    "status": "error",
                    "message": f"Task with ID '{task_id}' not found or you don't have permission to delete it"
                }
        except ValueError as ve:
            return {
                "status": "error",
                "message": f"Validation error: {str(ve)}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to delete task: {str(e)}"
            }
    
    def update_task(self, user_id: str, task_id: str, description: str = None, completed: bool = None) -> Dict[str, Any]:
        """
        MCP tool to update a task
        """
        try:
            # Validate inputs
            if not user_id:
                return {
                    "status": "error",
                    "message": "User ID is required to update a task"
                }
            
            if not task_id:
                return {
                    "status": "error",
                    "message": "Task ID is required to update a task"
                }
            
            if description is None and completed is None:
                return {
                    "status": "error",
                    "message": "At least one field (description or completed status) must be provided to update a task"
                }
            
            # Validate description length if provided
            if description and len(description) > 500:
                return {
                    "status": "error",
                    "message": "Task description is too long (max 500 characters)"
                }
            
            # Prepare update data
            update_data = {}
            if description is not None:
                update_data["description"] = description.strip() if description else description
            if completed is not None:
                update_data["completed"] = completed
            
            task_update = TaskUpdate(**update_data)
            task = self.task_service.update_task(self.session, task_id, user_id, task_update)
            
            if task:
                return {
                    "status": "success",
                    "task_id": task.id,
                    "message": f"Task updated successfully"
                }
            else:
                return {
                    "status": "error",
                    "message": f"Task with ID '{task_id}' not found or you don't have permission to update it"
                }
        except ValueError as ve:
            return {
                "status": "error",
                "message": f"Validation error: {str(ve)}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to update task: {str(e)}"
            }