from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy import or_, and_, func
from app.extensions import db
from app.models.crop import Crop, CropVariety, CropCycle, CropCompatibility, CropPestDisease, CropGrowthStage
from app.repositories.base_repository import BaseRepository

class CropRepository(BaseRepository[Crop]):
    """Data Access Repository for Crop Species Catalog, Varieties, Cycles, and Compatibility."""

    def __init__(self):
        super().__init__(Crop)

    def find_by_name(self, name: str) -> Optional[Crop]:
        """Look up crop species by exact or case-insensitive name."""
        return db.session.query(Crop).filter(func.lower(Crop.name) == name.lower().strip()).first()

    def get_crops_by_category(self, category: str) -> List[Crop]:
        """Fetch all crops in a category (Cereal, Pulse, Vegetable, Cash Crop, Oilseed)."""
        return db.session.query(Crop).filter(func.lower(Crop.category) == category.lower().strip()).all()

    def get_crops_by_season(self, season: str) -> List[Crop]:
        """Fetch crops suitable for a growing season (Kharif, Rabi, Zaid, Perennial, All Season)."""
        return db.session.query(Crop).filter(
            or_(func.lower(Crop.season) == season.lower().strip(), Crop.season == 'All Season')
        ).all()

    def search_crops(
        self,
        keyword: Optional[str] = None,
        category: Optional[str] = None,
        season: Optional[str] = None,
        min_ph: Optional[float] = None,
        max_ph: Optional[float] = None,
        page: int = 1,
        per_page: int = 20
    ) -> Tuple[List[Crop], int, int]:
        """Search reference crop catalog with parameters."""
        query = db.session.query(Crop)

        if keyword:
            term = f"%{keyword.strip()}%"
            query = query.filter(
                or_(
                    Crop.name.ilike(term),
                    Crop.scientific_name.ilike(term),
                    Crop.description.ilike(term)
                )
            )

        if category:
            query = query.filter(Crop.category == category)

        if season:
            query = query.filter(Crop.season == season)

        if min_ph is not None:
            query = query.filter(Crop.min_ph <= min_ph)

        if max_ph is not None:
            query = query.filter(Crop.max_ph >= max_ph)

        return self.paginate(page=page, per_page=per_page, query=query.order_by(Crop.name.asc()))

    def add_variety(self, crop_id: int, variety_name: str, maturity_type: str = 'Medium Duration', disease_resistance: str = 'Moderate', yield_multiplier: float = 1.1) -> CropVariety:
        """Register a cultivar variety for a crop."""
        var = CropVariety(
            crop_id=crop_id,
            variety_name=variety_name,
            maturity_type=maturity_type,
            disease_resistance=disease_resistance,
            yield_potential_multiplier=yield_multiplier
        )
        db.session.add(var)
        db.session.commit()
        return var

    def get_varieties(self, crop_id: int) -> List[CropVariety]:
        """Fetch all varieties of a crop."""
        return db.session.query(CropVariety).filter_by(crop_id=crop_id).all()

    def create_crop_cycle(self, field_id: int, crop_id: int, sowing_date, expected_harvest_date, variety_id: Optional[int] = None, acreage: float = 1.0, seeding_rate: float = 25.0, notes: Optional[str] = None) -> CropCycle:
        """Register active or scheduled crop planting cycle on a field."""
        cycle = CropCycle(
            field_id=field_id,
            crop_id=crop_id,
            variety_id=variety_id,
            sowing_date=sowing_date,
            expected_harvest_date=expected_harvest_date,
            status='Sown',
            acreage=acreage,
            seeding_rate_kg_per_acre=seeding_rate,
            notes=notes
        )
        db.session.add(cycle)
        db.session.commit()
        return cycle

    def get_active_cycles(self, field_id: Optional[int] = None) -> List[CropCycle]:
        """Fetch active ongoing crop cycles."""
        query = db.session.query(CropCycle).filter(CropCycle.status.in_(['Sown', 'Growing', 'Flowering', 'Harvesting']))
        if field_id:
            query = query.filter_by(field_id=field_id)
        return query.order_by(CropCycle.sowing_date.desc()).all()

    def update_cycle_status(self, cycle_id: int, status: str, actual_harvest_date=None) -> Optional[CropCycle]:
        """Update growth stage status of crop cycle."""
        cycle = db.session.get(CropCycle, cycle_id)
        if cycle:
            cycle.status = status
            if actual_harvest_date:
                cycle.actual_harvest_date = actual_harvest_date
            db.session.commit()
        return cycle

    def add_compatibility_rule(self, crop_a_id: int, crop_b_id: int, relationship_type: str = 'Rotation Friendly', compatibility_score: float = 85.0, notes: Optional[str] = None) -> CropCompatibility:
        """Define crop rotation or intercropping compatibility rule."""
        rule = CropCompatibility(
            crop_a_id=crop_a_id,
            crop_b_id=crop_b_id,
            relationship_type=relationship_type,
            compatibility_score=compatibility_score,
            notes=notes
        )
        db.session.add(rule)
        db.session.commit()
        return rule

    def check_rotation_compatibility(self, prev_crop_id: int, next_crop_id: int) -> float:
        """Lookup compatibility score between previous crop and proposed next crop."""
        rule = db.session.query(CropCompatibility).filter(
            or_(
                and_(CropCompatibility.crop_a_id == prev_crop_id, CropCompatibility.crop_b_id == next_crop_id),
                and_(CropCompatibility.crop_a_id == next_crop_id, CropCompatibility.crop_b_id == prev_crop_id)
            )
        ).first()
        return rule.compatibility_score if rule else 70.0
