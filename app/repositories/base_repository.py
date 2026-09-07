from typing import TypeVar, Generic, Type, List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Query
from sqlalchemy import desc, asc, or_, and_, func
from app.extensions import db

T = TypeVar('T', bound=db.Model)

class BaseRepository(Generic[T]):
    """Generic Base Data Access Repository providing unified CRUD, filtering, pagination, and transaction management."""

    def __init__(self, model_cls: Type[T]):
        self.model_cls = model_cls

    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Fetch entity by primary key integer ID."""
        return db.session.get(self.model_cls, entity_id)

    def get_by_id_or_404(self, entity_id: int) -> T:
        """Fetch entity by ID or raise 404 error."""
        entity = self.get_by_id(entity_id)
        if not entity:
            from werkzeug.exceptions import NotFound
            raise NotFound(f"{self.model_cls.__name__} with ID {entity_id} not found.")
        return entity

    def get_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[T]:
        """Retrieve all entity records with optional limit and offset."""
        query = db.session.query(self.model_cls)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        return query.all()

    def count_all(self) -> int:
        """Get total record count for entity."""
        return db.session.query(func.count(self.model_cls.id)).scalar() or 0

    def find_by(self, **kwargs) -> List[T]:
        """Filter entities by exact keyword arguments match."""
        return db.session.query(self.model_cls).filter_by(**kwargs).all()

    def find_one_by(self, **kwargs) -> Optional[T]:
        """Fetch single entity matching exact keyword parameters."""
        return db.session.query(self.model_cls).filter_by(**kwargs).first()

    def create(self, **kwargs) -> T:
        """Instantiate and commit a new entity record."""
        instance = self.model_cls(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

    def save(self, instance: T) -> T:
        """Save/persist existing or new entity instance to session."""
        db.session.add(instance)
        db.session.commit()
        return instance

    def update(self, instance: T, **kwargs) -> T:
        """Update attribute values on entity instance and commit."""
        for key, value in kwargs.items():
            if hasattr(instance, key) and value is not None:
                setattr(instance, key, value)
        db.session.commit()
        return instance

    def delete(self, instance: T) -> bool:
        """Delete entity instance from database session."""
        db.session.delete(instance)
        db.session.commit()
        return True

    def delete_by_id(self, entity_id: int) -> bool:
        """Delete entity record by ID."""
        entity = self.get_by_id(entity_id)
        if entity:
            return self.delete(entity)
        return False

    def paginate(self, page: int = 1, per_page: int = 20, query: Optional[Query] = None) -> Tuple[List[T], int, int]:
        """Paginate database query records returning (items, total_count, total_pages)."""
        if query is None:
            query = db.session.query(self.model_cls)

        total = query.count()
        pages = (total + per_page - 1) // per_page if per_page > 0 else 1
        items = query.offset((page - 1) * per_page).limit(per_page).all()
        return items, total, pages

    def bulk_create(self, records: List[Dict[str, Any]]) -> List[T]:
        """Bulk instantiate and save multiple entity dictionaries."""
        instances = [self.model_cls(**rec) for rec in records]
        db.session.add_all(instances)
        db.session.commit()
        return instances
