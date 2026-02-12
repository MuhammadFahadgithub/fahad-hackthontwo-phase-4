/**
 * Todo List component.
 *
 * Displays all todos for the authenticated user with create/edit/delete functionality.
 * Constitution Principle IV: Only shows user's own todos
 */
"use client";

import { useState, useEffect } from "react";
import { TodoItem } from "./TodoItem";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { fetchTodos, createTodo, updateTodo, deleteTodo, type Todo, type TodoCreate, type TodoUpdate } from "@/lib/api/todos";

export function TodoList() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [newTitle, setNewTitle] = useState("");
  const [newDescription, setNewDescription] = useState("");

  useEffect(() => {
    loadTodos();
  }, []);

  const loadTodos = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await fetchTodos();
      setTodos(data);
    } catch (err) {
      setError("Failed to load todos");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreate = async () => {
    if (!newTitle.trim()) return;

    setIsLoading(true);
    setError(null);
    try {
      const todoData: TodoCreate = {
        title: newTitle,
        description: newDescription || undefined,
        completed: false,
      };
      const newTodo = await createTodo(todoData);
      setTodos([newTodo, ...todos]);
      setNewTitle("");
      setNewDescription("");
      setIsCreating(false);
    } catch (err) {
      setError("Failed to create todo");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleUpdate = async (id: number, data: TodoUpdate) => {
    try {
      const updatedTodo = await updateTodo(id, data);
      setTodos(todos.map((todo) => (todo.id === id ? updatedTodo : todo)));
    } catch (err) {
      setError("Failed to update todo");
      console.error(err);
      throw err;
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await deleteTodo(id);
      setTodos(todos.filter((todo) => todo.id !== id));
    } catch (err) {
      setError("Failed to delete todo");
      console.error(err);
      throw err;
    }
  };

  if (isLoading && todos.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-600">Loading todos...</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-3">
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}

      {/* Create Todo Form */}
      {isCreating ? (
        <div className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm">
          <h3 className="text-lg font-medium text-gray-900 mb-3">Create New Todo</h3>
          <div className="space-y-3">
            <Input
              label="Title"
              value={newTitle}
              onChange={(e) => setNewTitle(e.target.value)}
              disabled={isLoading}
              required
              placeholder="What needs to be done?"
            />
            <Input
              label="Description"
              value={newDescription}
              onChange={(e) => setNewDescription(e.target.value)}
              disabled={isLoading}
              placeholder="Add more details (optional)"
            />
            <div className="flex gap-2">
              <Button
                variant="primary"
                onClick={handleCreate}
                disabled={isLoading || !newTitle.trim()}
                className="flex-1"
              >
                Create
              </Button>
              <Button
                variant="secondary"
                onClick={() => {
                  setIsCreating(false);
                  setNewTitle("");
                  setNewDescription("");
                }}
                disabled={isLoading}
                className="flex-1"
              >
                Cancel
              </Button>
            </div>
          </div>
        </div>
      ) : (
        <Button
          variant="primary"
          onClick={() => setIsCreating(true)}
          className="w-full"
        >
          + Add New Todo
        </Button>
      )}

      {/* Todo List */}
      {todos.length === 0 && !isCreating ? (
        <div className="text-center py-12 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
          <p className="text-gray-600 mb-2">No todos yet</p>
          <p className="text-sm text-gray-500">Click "Add New Todo" to get started</p>
        </div>
      ) : (
        <div className="space-y-3">
          {todos.map((todo) => (
            <TodoItem
              key={todo.id}
              todo={todo}
              onUpdate={handleUpdate}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}

      {/* Stats */}
      {todos.length > 0 && (
        <div className="pt-4 border-t border-gray-200">
          <div className="flex justify-between text-sm text-gray-600">
            <span>Total: {todos.length}</span>
            <span>Completed: {todos.filter((t) => t.completed).length}</span>
            <span>Active: {todos.filter((t) => !t.completed).length}</span>
          </div>
        </div>
      )}
    </div>
  );
}
