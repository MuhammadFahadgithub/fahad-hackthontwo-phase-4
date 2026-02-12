/**
 * Task detail page.
 *
 * Shows full details of a single task.
 * Maps to User Story 4: View Single Task Details
 */
"use client";

import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { useAuth } from "@/lib/auth/AuthProvider";
import { apiGet, apiPut, apiDelete } from "@/lib/api/client";
import type { Todo } from "@/lib/api/todos";

export default function TaskDetailPage() {
  const router = useRouter();
  const params = useParams();
  const { isAuthenticated, isLoading: authLoading } = useAuth();
  const [task, setTask] = useState<Todo | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const taskId = params?.id as string;

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push("/login");
      return;
    }

    if (isAuthenticated && taskId) {
      loadTask();
    }
  }, [isAuthenticated, authLoading, taskId]);

  const loadTask = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await apiGet<Todo>(`/api/v1/todos/${taskId}`);
      setTask(data);
    } catch (err: any) {
      setError(err.message || "Failed to load task");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleToggleComplete = async () => {
    if (!task) return;

    try {
      const updated = await apiPut<Todo>(`/api/v1/todos/${task.id}`, {
        completed: !task.completed,
      });
      setTask(updated);
    } catch (err: any) {
      setError(err.message || "Failed to update task");
    }
  };

  const handleDelete = async () => {
    if (!task) return;
    if (!confirm("Are you sure you want to delete this task?")) return;

    try {
      await apiDelete(`/api/v1/todos/${task.id}`);
      router.push("/tasks");
    } catch (err: any) {
      setError(err.message || "Failed to delete task");
    }
  };

  if (authLoading || isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <p className="text-gray-600">Loading...</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card className="max-w-md">
          <CardContent className="pt-6">
            <div className="text-center">
              <p className="text-red-600 mb-4">{error}</p>
              <Button onClick={() => router.push("/tasks")}>
                Back to Tasks
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!task) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card className="max-w-md">
          <CardContent className="pt-6">
            <div className="text-center">
              <p className="text-gray-600 mb-4">Task not found</p>
              <Button onClick={() => router.push("/tasks")}>
                Back to Tasks
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation Bar */}
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <Button
                variant="secondary"
                onClick={() => router.push("/tasks")}
                className="text-sm"
              >
                ← Back to Tasks
              </Button>
              <h1 className="text-xl font-semibold text-gray-900">Task Details</h1>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Card>
          <CardHeader>
            <div className="flex justify-between items-start">
              <CardTitle className={task.completed ? "line-through text-gray-500" : ""}>
                {task.title}
              </CardTitle>
              <div className="flex gap-2">
                <Button
                  variant="secondary"
                  onClick={() => router.push(`/tasks/${task.id}/edit`)}
                  className="text-sm"
                >
                  Edit
                </Button>
                <Button
                  variant="danger"
                  onClick={handleDelete}
                  className="text-sm"
                >
                  Delete
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {/* Completion Status */}
              <div className="flex items-center gap-3">
                <input
                  type="checkbox"
                  checked={task.completed}
                  onChange={handleToggleComplete}
                  className="h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm font-medium text-gray-700">
                  {task.completed ? "Completed" : "Not completed"}
                </span>
              </div>

              {/* Description */}
              {task.description && (
                <div>
                  <h3 className="text-sm font-medium text-gray-700 mb-2">Description</h3>
                  <p className="text-gray-600">{task.description}</p>
                </div>
              )}

              {/* Metadata */}
              <div className="border-t border-gray-200 pt-4">
                <h3 className="text-sm font-medium text-gray-700 mb-3">Details</h3>
                <dl className="space-y-2">
                  <div className="flex justify-between">
                    <dt className="text-sm text-gray-600">Created</dt>
                    <dd className="text-sm font-medium text-gray-900">
                      {new Date(task.created_at).toLocaleString()}
                    </dd>
                  </div>
                  <div className="flex justify-between">
                    <dt className="text-sm text-gray-600">Last Updated</dt>
                    <dd className="text-sm font-medium text-gray-900">
                      {new Date(task.updated_at).toLocaleString()}
                    </dd>
                  </div>
                  <div className="flex justify-between">
                    <dt className="text-sm text-gray-600">Task ID</dt>
                    <dd className="text-sm font-medium text-gray-900">#{task.id}</dd>
                  </div>
                </dl>
              </div>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
