"""
Security and authentication middleware
"""
from functools import wraps
from flask import request, jsonify
import os
import hashlib
import time
from collections import defaultdict
from datetime import datetime, timedelta


# In-memory rate limiting (use Redis in production)
request_counts = defaultdict(list)
RATE_LIMIT = int(os.getenv('RATE_LIMIT', '100'))  # requests per minute
RATE_WINDOW = 60  # seconds


def require_api_key(f):
    """
    Decorator to require API key authentication
    Set API_KEYS environment variable with comma-separated keys
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if API key authentication is enabled
        api_keys = os.getenv('API_KEYS', '').split(',')
        if not api_keys or api_keys == ['']:
            # API keys not configured, allow access
            return f(*args, **kwargs)
        
        # Get API key from header or query parameter
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        
        if not api_key:
            return jsonify({
                'error': 'API key required',
                'message': 'Please provide API key in X-API-Key header or api_key parameter'
            }), 401
        
        if api_key not in api_keys:
            return jsonify({
                'error': 'Invalid API key',
                'message': 'The provided API key is not valid'
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated_function


def rate_limit(f):
    """
    Decorator to implement rate limiting
    Limits requests per IP address
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get client IP
        client_ip = request.remote_addr or request.environ.get('HTTP_X_FORWARDED_FOR', 'unknown')
        
        # Clean up old requests
        current_time = time.time()
        request_counts[client_ip] = [
            req_time for req_time in request_counts[client_ip]
            if current_time - req_time < RATE_WINDOW
        ]
        
        # Check rate limit
        if len(request_counts[client_ip]) >= RATE_LIMIT:
            return jsonify({
                'error': 'Rate limit exceeded',
                'message': f'Maximum {RATE_LIMIT} requests per minute',
                'retry_after': RATE_WINDOW
            }), 429
        
        # Add current request
        request_counts[client_ip].append(current_time)
        
        return f(*args, **kwargs)
    
    return decorated_function


def validate_input(required_fields=None, optional_fields=None):
    """
    Decorator to validate JSON input
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({
                    'error': 'Invalid content type',
                    'message': 'Request must be JSON'
                }), 400
            
            data = request.get_json()
            
            # Check required fields
            if required_fields:
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    return jsonify({
                        'error': 'Missing required fields',
                        'fields': missing_fields
                    }), 400
            
            # Sanitize input (basic XSS prevention)
            def sanitize(obj):
                if isinstance(obj, str):
                    # Remove potentially dangerous characters
                    return obj.replace('<', '&lt;').replace('>', '&gt;')
                elif isinstance(obj, dict):
                    return {k: sanitize(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [sanitize(item) for item in obj]
                return obj
            
            request.sanitized_json = sanitize(data)
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


class SecurityHeaders:
    """Middleware to add security headers"""
    
    def __init__(self, app):
        self.app = app
        app.after_request(self.add_security_headers)
    
    @staticmethod
    def add_security_headers(response):
        """Add security headers to response"""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        
        return response


def generate_api_key():
    """Generate a secure API key"""
    timestamp = str(time.time())
    random_data = os.urandom(32)
    hash_input = (timestamp + random_data.hex()).encode()
    return hashlib.sha256(hash_input).hexdigest()


if __name__ == '__main__':
    # Generate sample API keys
    print("Generated API Keys:")
    for i in range(3):
        print(f"  {i+1}. {generate_api_key()}")
