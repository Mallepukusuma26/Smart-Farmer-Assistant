from app.extensions import db
from app.models.farm import Farm
from app.models.field import Field

class FarmService:
    """Service layer for managing farms and fields."""

    @staticmethod
    def create_farm(farmer_id, name, location, total_area, unit='Acres', ownership_type='Owned', default_soil_type='Loamy', notes=None):
        """Create a new farm for a farmer."""
        farm = Farm(
            farmer_id=farmer_id,
            name=name,
            location=location,
            total_area=float(total_area),
            unit=unit,
            ownership_type=ownership_type,
            default_soil_type=default_soil_type,
            notes=notes
        )
        db.session.add(farm)
        db.session.commit()
        return farm

    @staticmethod
    def update_farm(farm_id, farmer_id, name, location, total_area, unit, ownership_type, default_soil_type, notes=None):
        """Update existing farm."""
        farm = Farm.query.filter_by(id=farm_id, farmer_id=farmer_id).first()
        if not farm:
            return None, "Farm not found or access denied."

        farm.name = name
        farm.location = location
        farm.total_area = float(total_area)
        farm.unit = unit
        farm.ownership_type = ownership_type
        farm.default_soil_type = default_soil_type
        farm.notes = notes

        db.session.commit()
        return farm, "Farm updated successfully."

    @staticmethod
    def delete_farm(farm_id, farmer_id):
        """Delete farm and associated fields."""
        farm = Farm.query.filter_by(id=farm_id, farmer_id=farmer_id).first()
        if not farm:
            return False, "Farm not found or access denied."

        db.session.delete(farm)
        db.session.commit()
        return True, "Farm deleted successfully."

    @staticmethod
    def create_field(farm_id, field_name, area, soil_type='Loamy', irrigation_type='Drip', farming_method='Conventional', notes=None):
        """Create a field inside a farm."""
        field = Field(
            farm_id=farm_id,
            field_name=field_name,
            area=float(area),
            soil_type=soil_type,
            irrigation_type=irrigation_type,
            farming_method=farming_method,
            notes=notes
        )
        db.session.add(field)
        db.session.commit()
        return field

    @staticmethod
    def update_field(field_id, field_name, area, soil_type, irrigation_type, farming_method, current_status='Active', notes=None):
        """Update an existing field."""
        field = Field.query.get(field_id)
        if not field:
            return None, "Field not found."

        field.field_name = field_name
        field.area = float(area)
        field.soil_type = soil_type
        field.irrigation_type = irrigation_type
        field.farming_method = farming_method
        field.current_status = current_status
        field.notes = notes

        db.session.commit()
        return field, "Field updated successfully."

    @staticmethod
    def delete_field(field_id):
        """Delete a field."""
        field = Field.query.get(field_id)
        if not field:
            return False, "Field not found."

        db.session.delete(field)
        db.session.commit()
        return True, "Field deleted successfully."
