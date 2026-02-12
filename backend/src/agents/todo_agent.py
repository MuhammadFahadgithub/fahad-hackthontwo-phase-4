from typing import Dict, Any, Optional
from sqlmodel import Session
from ..mcp.tools import MCPTaskTools
from ..nlp.processor import NaturalLanguageProcessor
from ..core.logger import app_logger


class TodoAgent:
    """
    AI agent that processes natural language and performs task operations via MCP tools
    """
    
    def __init__(self, session: Session):
        self.session = session
        self.mcp_tools = MCPTaskTools(session)
        self.nlp_processor = NaturalLanguageProcessor()
    
    def process_message(self, user_id: str, message: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a user message and return an appropriate response
        """
        app_logger.log_info(f"Processing message: {message[:50]}...", user_id=user_id)
        
        # For now, we'll just process the message as before
        # In a more advanced implementation, we would retrieve conversation history
        # and use it to provide context to the AI processing
        
        # Process the natural language input
        processed = self.nlp_processor.process_input(message)
        operation = processed.get("operation")
        
        # If operation is unknown, return the message from processor
        if operation == "unknown":
            response_msg = processed.get("message", "I didn't understand that command.")
            app_logger.log_warning(f"NLP processing failed: {response_msg}", user_id=user_id)
            return {
                "response": response_msg,
                "conversation_id": conversation_id,
                "task_operations": [],
                "timestamp": self._get_current_timestamp()
            }
        
        # Execute the appropriate MCP tool based on the operation
        operation_result = self._execute_operation(user_id, operation, processed.get("params", {}))
        
        # Generate response based on operation result
        response = self._generate_response(operation, operation_result)
        
        # Log the operation result
        if operation_result.get("status") == "success":
            app_logger.log_info(f"Operation {operation} succeeded", user_id=user_id, extra={"result": operation_result})
        else:
            app_logger.log_error(f"Operation {operation} failed", user_id=user_id, extra={"result": operation_result})
        
        return {
            "response": response,
            "conversation_id": conversation_id,
            "task_operations": [operation_result],
            "timestamp": self._get_current_timestamp()
        }
    
    def _execute_operation(self, user_id: str, operation: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the appropriate MCP tool based on the operation
        """
        try:
            if operation == "add_task":
                return self.mcp_tools.add_task(user_id, params.get("description"))
            
            elif operation == "list_tasks":
                return self.mcp_tools.list_tasks(user_id)
            
            elif operation == "complete_task":
                # If task_id is provided, use it directly
                if "task_id" in params:
                    return self.mcp_tools.complete_task(user_id, params["task_id"])
                # If description is provided, try to find the task by description
                elif "description" in params:
                    # First, get all user tasks to find the matching one
                    tasks_result = self.mcp_tools.list_tasks(user_id)
                    if tasks_result["status"] == "success":
                        tasks = tasks_result.get("tasks", [])
                        # Find task by description
                        for task in tasks:
                            if params["description"].lower() in task.get("description", "").lower():
                                return self.mcp_tools.complete_task(user_id, task["id"])
                        return {
                            "status": "error",
                            "message": f"No task found matching '{params['description']}'"
                        }
                    else:
                        return {
                            "status": "error",
                            "message": "Could not retrieve tasks to find the one to complete"
                        }
                else:
                    return {
                        "status": "error",
                        "message": "Task ID or description is required to complete a task"
                    }
            
            elif operation == "delete_task":
                # If task_id is provided, use it directly
                if "task_id" in params:
                    return self.mcp_tools.delete_task(user_id, params["task_id"])
                # If description is provided, try to find the task by description
                elif "description" in params:
                    # First, get all user tasks to find the matching one
                    tasks_result = self.mcp_tools.list_tasks(user_id)
                    if tasks_result["status"] == "success":
                        tasks = tasks_result.get("tasks", [])
                        # Find task by description
                        for task in tasks:
                            if params["description"].lower() in task.get("description", "").lower():
                                return self.mcp_tools.delete_task(user_id, task["id"])
                        return {
                            "status": "error",
                            "message": f"No task found matching '{params['description']}'"
                        }
                    else:
                        return {
                            "status": "error",
                            "message": "Could not retrieve tasks to find the one to delete"
                        }
                else:
                    return {
                        "status": "error",
                        "message": "Task ID or description is required to delete a task"
                    }
            
            elif operation == "update_task":
                # If task_id is provided, use it directly
                if "task_id" in params:
                    return self.mcp_tools.update_task(
                        user_id, 
                        params["task_id"], 
                        params.get("description"), 
                        params.get("completed")
                    )
                # If old_description and new_description are provided, try to find by old description
                elif "old_description" in params and "new_description" in params:
                    # First, get all user tasks to find the matching one
                    tasks_result = self.mcp_tools.list_tasks(user_id)
                    if tasks_result["status"] == "success":
                        tasks = tasks_result.get("tasks", [])
                        # Find task by old description
                        for task in tasks:
                            if params["old_description"].lower() in task.get("description", "").lower():
                                return self.mcp_tools.update_task(
                                    user_id, 
                                    task["id"], 
                                    params["new_description"], 
                                    params.get("completed")
                                )
                        return {
                            "status": "error",
                            "message": f"No task found matching '{params['old_description']}'"
                        }
                    else:
                        return {
                            "status": "error",
                            "message": "Could not retrieve tasks to find the one to update"
                        }
                else:
                    return {
                        "status": "error",
                        "message": "Task ID or old/new descriptions are required to update a task"
                    }
            
            else:
                return {
                    "status": "error",
                    "message": f"Unknown operation: {operation}"
                }
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error executing operation: {str(e)}"
            }
    
    def _generate_response(self, operation: str, result: Dict[str, Any]) -> str:
        """
        Generate a human-readable response based on the operation and result
        """
        if result["status"] == "error":
            return f"Sorry, I couldn't perform that action: {result['message']}"
        
        if operation == "add_task":
            if result["status"] == "success":
                return f"I've added the task '{result.get('description', 'unnamed')}' to your list."
        
        elif operation == "list_tasks":
            if result["status"] == "success":
                task_count = result.get("count", 0)
                if task_count == 0:
                    return "You don't have any tasks on your list."
                else:
                    tasks = result.get("tasks", [])
                    task_list = []
                    for i, task in enumerate(tasks, 1):
                        status = "✓" if task.get("completed") else "○"
                        task_list.append(f"{i}. [{status}] {task.get('description', 'unnamed')}")
                    return f"You have {task_count} tasks:\n" + "\n".join(task_list)
        
        elif operation == "complete_task":
            if result["status"] == "success":
                return f"I've marked the task as complete."
        
        elif operation == "delete_task":
            if result["status"] == "success":
                return "I've deleted the task from your list."
        
        elif operation == "update_task":
            if result["status"] == "success":
                return "I've updated the task."
        
        # Default response if we can't generate a specific one
        return result.get("message", "Operation completed.")
    
    def _get_current_timestamp(self) -> str:
        """
        Get current timestamp in ISO format
        """
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"