import pytest
from backend.src.utils.chat_parser import parse_todo_command, extract_todo_details


def test_parse_add_todo_command():
    """Test parsing of add todo commands"""
    message = "Add a todo: Buy groceries"
    result = parse_todo_command(message)
    
    assert result['operation'] == 'add'
    assert result['text'] == 'Buy groceries'


def test_parse_list_todos_command():
    """Test parsing of list todos commands"""
    message = "Show my todos"
    result = parse_todo_command(message)
    
    assert result['operation'] == 'list'


def test_parse_complete_todo_command():
    """Test parsing of complete todo commands"""
    message = "Complete todo: Buy groceries"
    result = parse_todo_command(message)
    
    assert result['operation'] == 'complete'
    assert result['text'] == 'Buy groceries'


def test_parse_delete_todo_command():
    """Test parsing of delete todo commands"""
    message = "Delete todo: Buy groceries"
    result = parse_todo_command(message)
    
    assert result['operation'] == 'delete'
    assert result['text'] == 'Buy groceries'


def test_extract_todo_details_basic():
    """Test extracting basic todo details"""
    text = "Buy groceries"
    result = extract_todo_details(text)
    
    assert result['title'] == 'Buy groceries'
    assert result['priority'] == 'medium'  # default priority


def test_extract_todo_details_with_priority():
    """Test extracting todo details with priority indicators"""
    text = "Buy groceries - high priority"
    result = extract_todo_details(text)
    
    assert result['title'] == 'Buy groceries - high priority'
    assert result['priority'] == 'high'


def test_extract_todo_details_with_urgent():
    """Test extracting todo details with urgent indicator"""
    text = "Finish report urgent"
    result = extract_todo_details(text)
    
    assert result['title'] == 'Finish report urgent'
    assert result['priority'] == 'high'


def test_unknown_command():
    """Test parsing of unknown commands"""
    message = "What's the weather like?"
    result = parse_todo_command(message)
    
    assert result['operation'] == 'unknown'