"""
Chat parser utility for the Todo Chatbot application
"""
import re
from typing import Dict, Any


def parse_todo_command(message: str) -> Dict[str, Any]:
    """
    Parse a natural language command to extract todo operation details
    """
    message_lower = message.lower().strip()
    
    # Define patterns for different operations
    patterns = {
        'add': [
            r"(?:add|create|new)\s+(?:a\s+)?(?:todo|task)[:\s]+(.+)",
            r"(?:add|create|new)\s+(.+)"
        ],
        'complete': [
            r"(?:complete|done|finish)\s+(?:todo|task)[:\s]+(.+)",
            r"(?:complete|done|finish)\s+(.+)"
        ],
        'delete': [
            r"(?:delete|remove)\s+(?:todo|task)[:\s]+(.+)",
            r"(?:delete|remove)\s+(.+)"
        ],
        'list': [
            r"(?:show|list|view)\s+(?:my\s+)?(?:todos|tasks)",
            r"(?:what|show)\s+(?:are\s+)?(?:my\s+)?(?:todos|tasks)"
        ]
    }
    
    # Check for each operation type
    for operation, ops_patterns in patterns.items():
        for pattern in ops_patterns:
            match = re.search(pattern, message_lower)
            if match:
                # Extract the todo title/description if available
                extracted_text = match.group(1).strip().capitalize() if len(match.groups()) > 0 else None
                
                return {
                    'operation': operation,
                    'text': extracted_text,
                    'original_message': message
                }
    
    # If no specific pattern matched, return a generic response
    return {
        'operation': 'unknown',
        'text': message,
        'original_message': message
    }


def extract_todo_details(text: str) -> Dict[str, Any]:
    """
    Extract additional details from a todo text (like priority, due date, etc.)
    """
    details = {
        'title': text,
        'description': '',
        'priority': 'medium',  # default
        'due_date': None
    }
    
    # Look for priority indicators
    if 'high priority' in text.lower() or 'urgent' in text.lower() or 'asap' in text.lower():
        details['priority'] = 'high'
    elif 'low priority' in text.lower():
        details['priority'] = 'low'
    
    # Look for due date indicators (simple implementation)
    # In a real implementation, you would use more sophisticated date parsing
    if 'today' in text.lower():
        details['due_date'] = 'today'
    elif 'tomorrow' in text.lower():
        details['due_date'] = 'tomorrow'
    
    # Extract title and description
    # If the text is long, assume first sentence is title, rest is description
    sentences = text.split('.')
    if len(sentences) > 1:
        details['title'] = sentences[0].strip()
        details['description'] = '.'.join(sentences[1:]).strip()
    
    return details