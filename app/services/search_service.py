from typing import Dict, Any, List, Optional
from sqlalchemy import or_, func
from app.extensions import db
from app.models.farmer import Farmer
from app.models.farm import Farm
from app.models.field import Field
from app.models.crop import Crop
from app.models.fertilizer import Fertilizer
from app.models.disease import Disease
from app.models.soil import SoilRecord
from app.models.finance import Expense, Revenue

class SearchService:
    """Universal multi-entity search and filter engine for farmers, farms, fields, crops, fertilizers, diseases, and financial logs."""

    @staticmethod
    def global_search(keyword: str, farmer_id: Optional[int] = None) -> Dict[str, Any]:
        """Perform unified keyword search across all agricultural entities."""
        if not keyword or len(keyword.strip()) < 2:
            return {'query': keyword, 'results': {}}

        term = f"%{keyword.strip()}%"

        # 1. Farmers
        farmers_query = db.session.query(Farmer).filter(or_(Farmer.full_name.ilike(term), Farmer.phone.ilike(term), Farmer.address.ilike(term)))
        if farmer_id:
            farmers_query = farmers_query.filter(Farmer.id == farmer_id)
        farmers = [f.to_dict() for f in farmers_query.limit(10).all()]

        # 2. Farms
        farms_query = db.session.query(Farm).filter(or_(Farm.name.ilike(term), Farm.location.ilike(term)))
        if farmer_id:
            farms_query = farms_query.filter(Farm.farmer_id == farmer_id)
        farms = [f.to_dict() for f in farms_query.limit(10).all()]

        # 3. Fields
        fields_query = db.session.query(Field).filter(Field.field_name.ilike(term))
        if farmer_id:
            fields_query = fields_query.join(Farm, Field.farm_id == Farm.id).filter(Farm.farmer_id == farmer_id)
        fields = [fl.to_dict() for fl in fields_query.limit(10).all()]

        # 4. Crops
        crops = [c.to_dict() for c in db.session.query(Crop).filter(or_(Crop.name.ilike(term), Crop.category.ilike(term))).limit(10).all()]

        # 5. Fertilizers
        fertilizers = [ft.to_dict() for ft in db.session.query(Fertilizer).filter(or_(Fertilizer.name.ilike(term), Fertilizer.category.ilike(term))).limit(10).all()]

        # 6. Diseases
        diseases = [d.to_dict() for d in db.session.query(Disease).filter(or_(Disease.name.ilike(term), Disease.crop_name.ilike(term), Disease.symptoms.ilike(term))).limit(10).all()]

        # 7. Expenses
        exp_query = db.session.query(Expense).filter(or_(Expense.category.ilike(term), Expense.description.ilike(term)))
        if farmer_id:
            exp_query = exp_query.filter(Expense.farmer_id == farmer_id)
        expenses = [e.to_dict() for e in exp_query.limit(10).all()]

        total_matches = len(farmers) + len(farms) + len(fields) + len(crops) + len(fertilizers) + len(diseases) + len(expenses)

        return {
            'query': keyword,
            'total_matches': total_matches,
            'results': {
                'farmers': farmers,
                'farms': farms,
                'fields': fields,
                'crops': crops,
                'fertilizers': fertilizers,
                'diseases': diseases,
                'expenses': expenses
            }
        }
