from typing import Dict, Any, Optional
from app.validators.base_validator import BaseValidator

class DiseaseImageUploadValidator(BaseValidator):
    """Validator for leaf disease image upload metadata and file format safety."""

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'bmp'}
    MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB limit

    def validate_file(self, filename: str, file_size_bytes: int) -> bool:
        """Validate filename extension and byte size limit."""
        if not filename or '.' not in filename:
            self.add_error('image_file', 'Valid image file is required.')
            return False

        ext = filename.rsplit('.', 1)[1].lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            self.add_error('image_file', f"File extension '.{ext}' is not supported. Allowed formats: PNG, JPG, JPEG, WEBP, BMP.")
            return False

        if file_size_bytes > self.MAX_FILE_SIZE_BYTES:
            self.add_error('image_file', 'Image size exceeds maximum limit of 10 MB.')
            return False

        return True

    def validate_payload(self) -> Dict[str, Any]:
        """Validate optional context parameters for disease diagnosis."""
        farmer_id = self.validate_range('farmer_id', min_val=1)
        field_id = self.validate_range('field_id', min_val=1)

        if not self.is_valid():
            return {}

        return {
            'farmer_id': int(farmer_id) if farmer_id else None,
            'field_id': int(field_id) if field_id else None,
            'crop_name_context': self.sanitize_string('crop_name', max_length=100)
        }
