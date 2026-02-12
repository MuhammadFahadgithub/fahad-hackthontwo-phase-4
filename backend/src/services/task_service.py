from typing import List, Optional
from sqlmodel import Session, select
from ..models.task import Task, TaskCreate, TaskUpdate, TaskRead


class TaskService:
    """
    Service class for handling task-related operations
    """
    
    def create_task(self, session: Session, task_create: TaskCreate) -> TaskRead:
        """
        Create a new task
        """
        task = Task.from_orm(task_create)
        session.add(task)
        session.commit()
        session.refresh(task)
        return TaskRead.from_orm(task)
    
    def get_user_tasks(self, session: Session, user_id: str) -> List[TaskRead]:
        """
        Retrieve all tasks for a specific user
        """
        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(statement).all()
        return [TaskRead.from_orm(task) for task in tasks]
    
    def get_task_by_id(self, session: Session, task_id: str, user_id: str) -> Optional[Task]:
        """
        Retrieve a specific task by ID for a user
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        return session.exec(statement).first()
    
    def update_task(self, session: Session, task_id: str, user_id: str, task_update: TaskUpdate) -> Optional[TaskRead]:
        """
        Update a specific task
        """
        from datetime import datetime
        task = self.get_task_by_id(session, task_id, user_id)
        if not task:
            return None

        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        task.updated_at = datetime.utcnow()  # Update timestamp
        session.add(task)
        session.commit()
        session.refresh(task)
        return TaskRead.from_orm(task)
    
    def delete_task(self, session: Session, task_id: str, user_id: str) -> bool:
        """
        Delete a specific task
        """
        task = self.get_task_by_id(session, task_id, user_id)
        if not task:
            return False
        
        session.delete(task)
        session.commit()
        return True
    
    def complete_task(self, session: Session, task_id: str, user_id: str) -> Optional[TaskRead]:
        """
        Mark a task as complete
        """
        from datetime import datetime
        task = self.get_task_by_id(session, task_id, user_id)
        if not task:
            return None

        task.completed = True
        task.updated_at = datetime.utcnow()  # Update timestamp
        session.add(task)
        session.commit()
        session.refresh(task)
        return TaskRead.from_orm(task)