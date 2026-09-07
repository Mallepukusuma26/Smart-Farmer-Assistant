from typing import Dict, Any, List, Optional, Generic, TypeVar, Tuple

T = TypeVar('T')

class BaseSchema:
    """Base serialization schema for transforming database models and dictionaries into API response structures."""

    @staticmethod
    def dump_one(instance: Any) -> Dict[str, Any]:
        """Serialize single object to dictionary if it implements to_dict()."""
        if instance is None:
            return {}
        if hasattr(instance, 'to_dict') and callable(getattr(instance, 'to_dict')):
            return instance.to_dict()
        if isinstance(instance, dict):
            return instance
        return vars(instance)

    @staticmethod
    def dump_many(instances: List[Any]) -> List[Dict[str, Any]]:
        """Serialize list of objects to list of dictionaries."""
        if not instances:
            return []
        return [BaseSchema.dump_one(item) for item in instances]

    @staticmethod
    def format_paginated_response(items: List[Any], total_count: int, current_page: int, total_pages: int, per_page: int = 20) -> Dict[str, Any]:
        """Format paginated API response wrapper."""
        return {
            'data': BaseSchema.dump_many(items),
            'pagination': {
                'total_items': total_count,
                'total_pages': total_pages,
                'current_page': current_page,
                'per_page': per_page,
                'has_next': current_page < total_pages,
                'has_prev': current_page > 1
            }
        }

    @staticmethod
    def format_success_response(data: Any = None, message: str = "Operation completed successfully.", status_code: int = 200) -> Tuple[Dict[str, Any], int]:
        """Format standard success JSON response tuple."""
        body = {
            'success': True,
            'message': message,
            'data': BaseSchema.dump_one(data) if data is not None and not isinstance(data, (list, dict)) else data
        }
        return body, status_code

    @staticmethod
    def format_error_response(message: str = "An error occurred.", errors: Optional[Dict[str, List[str]]] = None, status_code: int = 400) -> Tuple[Dict[str, Any], int]:
        """Format standard error JSON response tuple."""
        body = {
            'success': False,
            'message': message,
            'errors': errors or {}
        }
        return body, status_code
