import re
from typing import Dict, Any, List, Optional, Tuple

class ValidationError(Exception):
    """Custom exception raised when payload validation fails."""
    def __init__(self, errors: Dict[str, List[str]]):
        self.errors = errors
        super().__init__(str(errors))

class BaseValidator:
    """Base class for request data validation, payload sanitization, and type checking."""

    def __init__(self, data: Dict[str, Any]):
        self.data = data or {}
        self.errors: Dict[str, List[str]] = {}

    def add_error(self, field: str, message: str) -> None:
        """Add error message for field."""
        if field not in self.errors:
            self.errors[field] = []
        self.errors[field].append(message)

    def is_valid(self) -> bool:
        """Check if any validation errors exist."""
        return len(self.errors) == 0

    def validate_required(self, fields: List[str]) -> None:
        """Ensure required fields exist in payload and are non-empty."""
        for field in fields:
            val = self.data.get(field)
            if val is None or (isinstance(val, str) and val.strip() == ""):
                self.add_error(field, f"{field.replace('_', ' ').title()} is required.")

    def validate_email(self, field: str = 'email') -> Optional[str]:
        """Validate email format."""
        email = self.data.get(field)
        if email:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, str(email).strip()):
                self.add_error(field, "Invalid email address format.")
                return None
            return str(email).strip().lower()
        return None

    def validate_phone(self, field: str = 'phone') -> Optional[str]:
        """Validate telephone number format."""
        phone = self.data.get(field)
        if phone:
            cleaned = re.sub(r'[\s\-\(\)\+]', '', str(phone))
            if not (7 <= len(cleaned) <= 15 and cleaned.isdigit()):
                self.add_error(field, "Invalid phone number format.")
                return None
            return str(phone).strip()
        return None

    def validate_range(self, field: str, min_val: Optional[float] = None, max_val: Optional[float] = None) -> Optional[float]:
        """Validate numeric range."""
        val = self.data.get(field)
        if val is not None:
            try:
                num = float(val)
                if min_val is not None and num < min_val:
                    self.add_error(field, f"{field.replace('_', ' ').title()} must be at least {min_val}.")
                    return None
                if max_val is not None and num > max_val:
                    self.add_error(field, f"{field.replace('_', ' ').title()} cannot exceed {max_val}.")
                    return None
                return num
            except (ValueError, TypeError):
                self.add_error(field, f"{field.replace('_', ' ').title()} must be a valid number.")
                return None
        return None

    def validate_choice(self, field: str, allowed_choices: List[str]) -> Optional[str]:
        """Validate field value matches allowed choice set."""
        val = self.data.get(field)
        if val:
            val_str = str(val).strip()
            allowed_lower = [c.lower() for c in allowed_choices]
            if val_str.lower() not in allowed_lower:
                self.add_error(field, f"{field.replace('_', ' ').title()} must be one of: {', '.join(allowed_choices)}.")
                return None
            return val_str
        return None

    def sanitize_string(self, field: str, max_length: Optional[int] = None) -> Optional[str]:
        """Sanitize text string to prevent XSS / script injection."""
        val = self.data.get(field)
        if val is not None:
            clean = str(val).strip()
            # Replace html tag brackets for basic sanitization
            clean = clean.replace('<', '&lt;').replace('>', '&gt;')
            if max_length and len(clean) > max_length:
                self.add_error(field, f"{field.replace('_', ' ').title()} exceeds maximum length of {max_length} characters.")
                return None
            return clean
        return None
