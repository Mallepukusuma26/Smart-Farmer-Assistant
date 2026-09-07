from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy import or_, and_, func
from app.extensions import db
from app.models.fertilizer import Fertilizer, FertilizerInventory, FertilizerRecommendation, FertilizerApplication, FertilizerPurchase
from app.repositories.base_repository import BaseRepository

class FertilizerRepository(BaseRepository[Fertilizer]):
    """Data Access Repository for Fertilizer Catalog, Stock Inventory, Recommendations, and Applications."""

    def __init__(self):
        super().__init__(Fertilizer)

    def find_by_name(self, name: str) -> Optional[Fertilizer]:
        """Look up fertilizer product by exact name."""
        return db.session.query(Fertilizer).filter(func.lower(Fertilizer.name) == name.lower().strip()).first()

    def get_by_category(self, category: str) -> List[Fertilizer]:
        """Fetch fertilizers by category (Nitrogenous, Phosphatic, Potassic, Complex, Organic)."""
        return db.session.query(Fertilizer).filter(func.lower(Fertilizer.category) == category.lower().strip()).all()

    def search_fertilizers(
        self,
        keyword: Optional[str] = None,
        category: Optional[str] = None,
        max_price: Optional[float] = None,
        page: int = 1,
        per_page: int = 20
    ) -> Tuple[List[Fertilizer], int, int]:
        """Search fertilizer products with filter options."""
        query = db.session.query(Fertilizer)

        if keyword:
            term = f"%{keyword.strip()}%"
            query = query.filter(
                or_(
                    Fertilizer.name.ilike(term),
                    Fertilizer.suitable_crops.ilike(term),
                    Fertilizer.application_notes.ilike(term)
                )
            )

        if category:
            query = query.filter(Fertilizer.category == category)

        if max_price is not None:
            query = query.filter(Fertilizer.price_per_kg <= max_price)

        return self.paginate(page=page, per_page=per_page, query=query.order_by(Fertilizer.name.asc()))

    def get_farmer_inventory(self, farmer_id: int) -> List[FertilizerInventory]:
        """Fetch current fertilizer stock inventory of a farmer."""
        return db.session.query(FertilizerInventory).filter_by(farmer_id=farmer_id).all()

    def update_stock(self, farmer_id: int, fertilizer_id: int, quantity_change_kg: float) -> FertilizerInventory:
        """Add or subtract stock quantity for a farmer's inventory."""
        inv = db.session.query(FertilizerInventory).filter_by(farmer_id=farmer_id, fertilizer_id=fertilizer_id).first()
        if not inv:
            inv = FertilizerInventory(farmer_id=farmer_id, fertilizer_id=fertilizer_id, stock_quantity_kg=max(0.0, quantity_change_kg))
            db.session.add(inv)
        else:
            inv.stock_quantity_kg = max(0.0, inv.stock_quantity_kg + quantity_change_kg)
        db.session.commit()
        return inv

    def save_recommendation(self, field_id: int, recommended_fertilizer: str, quantity_kg_per_acre: float, total_quantity_kg: float, crop_id: Optional[int] = None, soil_record_id: Optional[int] = None, application_stage: str = 'Basal / Sowing', cost_estimate: float = 0.0, safety_notes: Optional[str] = None) -> FertilizerRecommendation:
        """Save generated NPK fertilizer recommendation."""
        rec = FertilizerRecommendation(
            field_id=field_id,
            crop_id=crop_id,
            soil_record_id=soil_record_id,
            recommended_fertilizer=recommended_fertilizer,
            quantity_kg_per_acre=quantity_kg_per_acre,
            total_quantity_kg=total_quantity_kg,
            application_stage=application_stage,
            cost_estimate=cost_estimate,
            safety_notes=safety_notes
        )
        db.session.add(rec)
        db.session.commit()
        return rec

    def get_field_recommendations(self, field_id: int) -> List[FertilizerRecommendation]:
        """Fetch historical fertilizer recommendations for a field."""
        return db.session.query(FertilizerRecommendation).filter_by(field_id=field_id).order_by(FertilizerRecommendation.created_at.desc()).all()

    def log_application(self, field_id: int, fertilizer_id: int, applied_quantity_kg: float, application_method: str = 'Broadcasting', operator_notes: Optional[str] = None, application_date=None) -> FertilizerApplication:
        """Record completed field fertilizer application."""
        from datetime import date
        if application_date is None:
            application_date = date.today()
        app_log = FertilizerApplication(
            field_id=field_id,
            fertilizer_id=fertilizer_id,
            applied_quantity_kg=applied_quantity_kg,
            application_method=application_method,
            operator_notes=operator_notes,
            application_date=application_date
        )
        db.session.add(app_log)
        db.session.commit()
        return app_log

    def record_purchase(self, farmer_id: int, fertilizer_id: int, bags_bought: int, weight_per_bag_kg: float, total_cost: float, vendor_store: Optional[str] = None) -> FertilizerPurchase:
        """Record purchase receipt for fertilizer acquisition and update inventory."""
        purchase = FertilizerPurchase(
            farmer_id=farmer_id,
            fertilizer_id=fertilizer_id,
            bags_bought=bags_bought,
            weight_per_bag_kg=weight_per_bag_kg,
            total_cost=total_cost,
            vendor_store=vendor_store
        )
        db.session.add(purchase)
        db.session.flush()

        total_kg = bags_bought * weight_per_bag_kg
        self.update_stock(farmer_id, fertilizer_id, total_kg)
        return purchase
