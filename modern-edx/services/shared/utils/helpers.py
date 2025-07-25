"""
Shared utility functions for Modern edX platform.
"""
import uuid
import hashlib
import secrets
from typing import Optional, Dict, Any
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

def generate_uuid() -> str:
    """Generate a unique UUID string."""
    return str(uuid.uuid4())

def generate_secure_token(length: int = 32) -> str:
    """Generate a cryptographically secure random token."""
    return secrets.token_urlsafe(length)

def hash_string(text: str, salt: Optional[str] = None) -> str:
    """Hash a string using SHA-256."""
    if salt:
        text = f"{text}{salt}"
    return hashlib.sha256(text.encode()).hexdigest()

def get_client_ip(request) -> str:
    """Get the client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_user_agent(request) -> str:
    """Get the user agent from request."""
    return request.META.get('HTTP_USER_AGENT', '')

def send_templated_email(
    template_name: str,
    context: Dict[str, Any],
    subject: str,
    recipient_list: list,
    from_email: Optional[str] = None
) -> bool:
    """Send an email using a template."""
    try:
        html_message = render_to_string(f'emails/{template_name}.html', context)
        text_message = render_to_string(f'emails/{template_name}.txt', context)
        
        send_mail(
            subject=subject,
            message=text_message,
            from_email=from_email or settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False
        )
        return True
    except Exception as e:
        # Log the error in production
        print(f"Failed to send email: {e}")
        return False

def create_verification_token(user_id: int) -> str:
    """Create a verification token for email verification."""
    timestamp = int(timezone.now().timestamp())
    data = f"{user_id}:{timestamp}"
    token = hash_string(data, settings.SECRET_KEY)
    return f"{user_id}:{timestamp}:{token}"

def verify_token(token: str, max_age_hours: int = 24) -> Optional[int]:
    """Verify a token and return user ID if valid."""
    try:
        parts = token.split(':')
        if len(parts) != 3:
            return None
        
        user_id, timestamp, token_hash = parts
        user_id = int(user_id)
        timestamp = int(timestamp)
        
        # Check if token is expired
        max_age_seconds = max_age_hours * 3600
        if timezone.now().timestamp() - timestamp > max_age_seconds:
            return None
        
        # Verify token
        data = f"{user_id}:{timestamp}"
        expected_hash = hash_string(data, settings.SECRET_KEY)
        
        if token_hash == expected_hash:
            return user_id
        
        return None
    except (ValueError, IndexError):
        return None

def calculate_progress_percentage(completed: int, total: int) -> float:
    """Calculate progress percentage."""
    if total == 0:
        return 0.0
    return round((completed / total) * 100, 2)

def format_duration(seconds: int) -> str:
    """Format duration in seconds to human readable format."""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}m"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        if minutes > 0:
            return f"{hours}h {minutes}m"
        return f"{hours}h"

def paginate_queryset(queryset, page: int, page_size: int = 20):
    """Paginate a queryset."""
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    
    paginator = Paginator(queryset, page_size)
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    return {
        'results': page_obj.object_list,
        'pagination': {
            'page': page_obj.number,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_size': page_size
        }
    }

def validate_file_extension(filename: str, allowed_extensions: list) -> bool:
    """Validate file extension."""
    extension = filename.lower().split('.')[-1]
    return extension in [ext.lower() for ext in allowed_extensions]

def generate_unique_filename(original_filename: str) -> str:
    """Generate a unique filename while preserving extension."""
    name, extension = original_filename.rsplit('.', 1)
    unique_id = generate_uuid()[:8]
    return f"{name}_{unique_id}.{extension}"

def clean_html_content(content: str) -> str:
    """Clean HTML content for security."""
    import re
    # Remove script tags
    content = re.sub(r'<script.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    # Remove potentially dangerous attributes
    content = re.sub(r'on\w+="[^"]*"', '', content, flags=re.IGNORECASE)
    content = re.sub(r"on\w+='[^']*'", '', content, flags=re.IGNORECASE)
    return content
