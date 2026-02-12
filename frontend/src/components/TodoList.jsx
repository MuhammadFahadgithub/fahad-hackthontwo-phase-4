import React, { useState, useEffect } from 'react';
import { 
  List, 
  ListItem, 
  ListItemText, 
  ListItemSecondaryAction, 
  IconButton, 
  Checkbox, 
  Button, 
  Box,
  Typography
} from '@mui/material';
import { Delete as DeleteIcon, Add as AddIcon } from '@mui/icons-material';

const TodoList = ({ todos, onToggle, onDelete, onAdd }) => {
  const [showAddForm, setShowAddForm] = useState(false);

  return (
    <Box>
      <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
        <Typography variant="h6">Your Todos</Typography>
        <Button 
          variant="contained" 
          startIcon={<AddIcon />}
          onClick={() => setShowAddForm(!showAddForm)}
        >
          Add Todo
        </Button>
      </Box>

      {showAddForm && <TodoForm onAdd={onAdd} onCancel={() => setShowAddForm(false)} />}

      <List>
        {todos && todos.length > 0 ? (
          todos.map((todo) => (
            <TodoItem 
              key={todo.id} 
              todo={todo} 
              onToggle={onToggle} 
              onDelete={onDelete} 
            />
          ))
        ) : (
          <ListItem>
            <ListItemText primary="No todos yet. Add one using the button above!" />
          </ListItem>
        )}
      </List>
    </Box>
  );
};

export default TodoList;