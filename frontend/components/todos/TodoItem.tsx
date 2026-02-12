/**
 * Todo Item component.
 *
 * Displays a single todo with edit and delete actions.
 * Constitution Principle V: Only owner can modify/delete
 */
"use client";

import { useState } from "react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import type { Todo } from "@/lib/api/todos";

interface TodoItemProps {
  todo: Todo;
  onUpdate: (id: number, data: { title?: string; description?: string; completed?: boolean }) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
}

export function TodoItem({ todo, onUpdate, onDelete }: TodoItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(todo.title);
  const [editDescription, setEditDescription] = useState(todo.description || "");
  const [isLoading, setIsLoading] = useState(false);

  const handleToggleComplete = async () => {
    setIsLoading(true);
    try {
      await onUpdate(todo.id, { completed: !todo.completed });
    } catch (error) {
      console.error("Failed to toggle todo:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSaveEdit = async () => {
    if (!editTitle.trim()) return;

    setIsLoading(true);
    try {
      await onUpdate(todo.id, {
        title: editTitle,
        description: editDescription || null,
      });
      setIsEditing(false);
    } catch (error) {
      console.error("Failed to update todo:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancelEdit = () => {
    setEditTitle(todo.title);
    setEditDescription(todo.description || "");
    setIsEditing(false);
  };

  const handleDelete = async () => {
    if (!confirm("Are you sure you want to delete this todo?")) return;

    setIsLoading(true);
    try {
      await onDelete(todo.id);
    } catch (error) {
      console.error("Failed to delete todo:", error);
      setIsLoading(false);
    }
  };

  if (isEditing) {
    return (
      <div className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm">
        <div className="space-y-3">
          <Input
            label="Title"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            disabled={isLoading}
            required
          />
          <Input
            label="Description"
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            disabled={isLoading}
          />
          <div className="flex gap-2">
            <Button
              variant="primary"
              onClick={handleSaveEdit}
              disabled={isLoading || !editTitle.trim()}
              className="flex-1"
            >
              Save
            </Button>
            <Button
              variant="secondary"
              onClick={handleCancelEdit}
              disabled={isLoading}
              className="flex-1"
            >
              Cancel
            </Button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-start gap-3">
        <input
          type="checkbox"
          checked={todo.completed}
          onChange={handleToggleComplete}
          disabled={isLoading}
          className="mt-1 h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
        />
        <div className="flex-1 min-w-0">
          <h3
            className={`text-base font-medium ${
              todo.completed ? "line-through text-gray-500" : "text-gray-900"
            }`}
          >
            {todo.title}
          </h3>
          {todo.description && (
            <p className="mt-1 text-sm text-gray-600">{todo.description}</p>
          )}
          <p className="mt-2 text-xs text-gray-400">
            Created {new Date(todo.created_at).toLocaleDateString()}
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="secondary"
            onClick={() => setIsEditing(true)}
            disabled={isLoading}
            className="text-sm px-3 py-1"
          >
            Edit
          </Button>
          <Button
            variant="danger"
            onClick={handleDelete}
            disabled={isLoading}
            className="text-sm px-3 py-1"
          >
            Delete
          </Button>
        </div>
      </div>
    </div>
  );
}
