import React from 'react';
import { 
  ListItem, 
  ListItemText, 
  ListItemSecondaryAction, 
  IconButton, 
  Checkbox 
} from '@mui/material';
import { Delete as DeleteIcon } from '@mui/icons-material';

const TodoItem = ({ todo, onToggle, onDelete }) => {
  const handleToggle = () => {
    onToggle(todo.id);
  };

  const handleDelete = () => {
    onDelete(todo.id);
  };

  return (
    <ListItem key={todo.id} divider>
      <Checkbox
        edge="start"
        checked={todo.completed}
        onChange={handleToggle}
        inputProps={{ 'aria-labelledby': `todo-${todo.id}` }}
      />
      <ListItemText
        id={`todo-${todo.id}`}
        primary={
          <span style={{ 
            textDecoration: todo.completed ? 'line-through' : 'none',
            color: todo.completed ? '#888' : 'inherit'
          }}>
            {todo.title}
          </span>
        }
        secondary={
          <>
            {todo.description && <div>{todo.description}</div>}
            <div>
              <small>Priority: <strong>{todo.priority}</strong></small>
              {todo.due_date && <small>, Due: {new Date(todo.due_date).toLocaleDateString()}</small>}
            </div>
          </>
        }
      />
      <ListItemSecondaryAction>
        <IconButton edge="end" aria-label="delete" onClick={handleDelete}>
          <DeleteIcon />
        </IconButton>
      </ListItemSecondaryAction>
    </ListItem>
  );
};

export default TodoItem;