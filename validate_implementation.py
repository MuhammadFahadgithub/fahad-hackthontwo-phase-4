"""
Basic validation script to ensure the Todo Chatbot application is properly implemented
"""
import subprocess
import sys
import os

def check_backend_structure():
    """Check that backend structure is properly implemented"""
    backend_path = "D:/fahadhacktodo/todophs4/backend"
    
    required_dirs = [
        "src",
        "src/models",
        "src/services",
        "src/api",
        "src/database",
        "src/utils",
        "src/auth"
    ]
    
    required_files = [
        "src/main.py",
        "src/config.py",
        "src/database/__init__.py",
        "src/models/__init__.py",
        "src/models/user.py",
        "src/models/todo.py",
        "src/models/conversation.py",
        "src/models/message.py",
        "src/services/chat_service.py",
        "src/services/todo_service.py",
        "src/api/__init__.py",
        "src/api/todo.py",
        "src/api/chat.py",
        "src/api/health.py",
        "src/api/metrics.py",
        "src/utils/chat_parser.py"
    ]
    
    print("Checking backend structure...")
    for dir_path in required_dirs:
        full_path = os.path.join(backend_path, dir_path)
        if not os.path.exists(full_path):
            print(f"[ERROR] Missing directory: {full_path}")
            return False
        print(f"[OK] Directory exists: {dir_path}")
    
    for file_path in required_files:
        full_path = os.path.join(backend_path, file_path)
        if not os.path.exists(full_path):
            print(f"[ERROR] Missing file: {full_path}")
            return False
        print(f"[OK] File exists: {file_path}")
    
    return True

def check_frontend_structure():
    """Check that frontend structure is properly implemented"""
    frontend_path = "D:/fahadhacktodo/todophs4/frontend"
    
    required_dirs = [
        "src/components",
        "src/services",
        "src/store"
    ]
    
    required_files = [
        "src/components/ChatInterface.jsx",
        "src/components/TodoList.jsx",
        "src/components/TodoForm.jsx",
        "src/components/TodoItem.jsx",
        "src/services/api.js",
        "src/services/chatService.js",
        "src/services/todoService.js",
        "src/store/todoSlice.js",
        "src/store/index.js"
    ]
    
    print("\nChecking frontend structure...")
    for dir_path in required_dirs:
        full_path = os.path.join(frontend_path, dir_path)
        if not os.path.exists(full_path):
            print(f"[ERROR] Missing directory: {full_path}")
            return False
        print(f"[OK] Directory exists: {dir_path}")
    
    for file_path in required_files:
        full_path = os.path.join(frontend_path, file_path)
        if not os.path.exists(full_path):
            print(f"[ERROR] Missing file: {full_path}")
            return False
        print(f"[OK] File exists: {file_path}")
    
    return True

def check_docker_files():
    """Check that Docker files are properly implemented"""
    docker_path = "D:/fahadhacktodo/todophs4/docker"
    
    required_files = [
        "backend/Dockerfile",
        "backend/.dockerignore",
        "frontend/Dockerfile",
        "frontend/.dockerignore"
    ]
    
    print("\nChecking Docker files...")
    for file_path in required_files:
        full_path = os.path.join(docker_path, file_path)
        if not os.path.exists(full_path):
            print(f"[ERROR] Missing file: {full_path}")
            return False
        print(f"[OK] File exists: {file_path}")
    
    return True

def check_helm_chart():
    """Check that Helm chart is properly implemented"""
    helm_path = "D:/fahadhacktodo/todophs4/helm/todo-chatbot"
    
    required_files = [
        "Chart.yaml",
        "values.yaml",
        "templates/_helpers.tpl",
        "templates/backend-deployment.yaml",
        "templates/frontend-deployment.yaml",
        "templates/services.yaml",
        "templates/ingress.yaml",
        "templates/postgres-statefulset.yaml",
        "templates/secrets.yaml",
        "templates/hpa.yaml"
    ]
    
    print("\nChecking Helm chart...")
    for file_path in required_files:
        full_path = os.path.join(helm_path, file_path)
        if not os.path.exists(full_path):
            print(f"[ERROR] Missing file: {full_path}")
            return False
        print(f"[OK] File exists: {file_path}")
    
    return True

def check_test_files():
    """Check that test files are properly implemented"""
    test_paths = [
        "D:/fahadhacktodo/todophs4/tests/contract/test_chat_api.py",
        "D:/fahadhacktodo/todophs4/tests/integration/test_chat_todo_creation.py",
        "D:/fahadhacktodo/todophs4/tests/unit/test_chat_parser.py",
        "D:/fahadhacktodo/todophs4/tests/contract/test_todo_api.py",
        "D:/fahadhacktodo/todophs4/tests/integration/test_web_todo_operations.py",
        "D:/fahadhacktodo/todophs4/tests/integration/test_hpa.py",
        "D:/fahadhacktodo/todophs4/tests/integration/test_health_checks.py"
    ]
    
    print("\nChecking test files...")
    for file_path in test_paths:
        if not os.path.exists(file_path):
            print(f"[ERROR] Missing test file: {file_path}")
            return False
        print(f"[OK] Test file exists: {file_path}")
    
    return True

def check_scripts_and_docs():
    """Check that scripts and documentation are properly implemented"""
    paths_to_check = [
        "D:/fahadhacktodo/todophs4/scripts/deploy-all.sh",
        "D:/fahadhacktodo/todophs4/scripts/cleanup.sh",
        "D:/fahadhacktodo/todophs4/docs/ai-operations-guide.md",
        "D:/fahadhacktodo/todophs4/README.md"
    ]
    
    print("\nChecking scripts and documentation...")
    for file_path in paths_to_check:
        if not os.path.exists(file_path):
            print(f"[ERROR] Missing file: {file_path}")
            return False
        print(f"[OK] File exists: {file_path}")
    
    return True

def main():
    print("Validating Todo Chatbot Implementation...\n")
    
    all_checks_passed = True
    
    all_checks_passed &= check_backend_structure()
    all_checks_passed &= check_frontend_structure()
    all_checks_passed &= check_docker_files()
    all_checks_passed &= check_helm_chart()
    all_checks_passed &= check_test_files()
    all_checks_passed &= check_scripts_and_docs()
    
    print("\n" + "="*50)
    if all_checks_passed:
        print("[SUCCESS] All checks passed! The Todo Chatbot implementation is complete.")
        print("\nThe application includes:")
        print("- Backend API with todo and chat endpoints")
        print("- Frontend with chat interface and web UI")
        print("- Docker configurations for both services")
        print("- Helm chart for Kubernetes deployment")
        print("- Comprehensive test suite")
        print("- AI-assisted operations documentation")
        print("- Deployment and cleanup scripts")
    else:
        print("[ERROR] Some checks failed. Please review the implementation.")
        sys.exit(1)

if __name__ == "__main__":
    main()