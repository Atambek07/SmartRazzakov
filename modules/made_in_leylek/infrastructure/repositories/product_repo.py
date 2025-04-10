# modules/made_in_leylek/infrastructure/repositories/product_repo.py
from django.db import DatabaseError
from ...domain.entities import ProductEntity
from ...domain.exceptions import ProductNotFoundError
from ..models.products import Product

class ProductRepository:
    async def create(self, product: ProductEntity) -> ProductEntity:
        try:
            db_product = await Product.objects.acreate(
                id=product.id,
                seller_id=product.seller_id,
                name=product.name,
                description=product.description,
                category=product.category.value,
                price=product.price,
                quantity=product.quantity,
                production_date=product.production_date,
                expiration_date=product.expiration_date,
                tags=product.tags,
                rating=product.rating
            )
            return self._to_entity(db_product)
        except DatabaseError as e:
            raise ProductNotFoundError(f"Error creating product: {str(e)}")

    async def get_by_id(self, product_id: str) -> ProductEntity:
        try:
            db_product = await Product.objects.aget(id=product_id)
            return self._to_entity(db_product)
        except Product.DoesNotExist:
            raise ProductNotFoundError(f"Product {product_id} not found")

    async def update(self, product_id: str, **kwargs) -> ProductEntity:
        try:
            db_product = await Product.objects.aget(id=product_id)
            for key, value in kwargs.items():
                setattr(db_product, key, value)
            await db_product.asave()
            return self._to_entity(db_product)
        except Product.DoesNotExist:
            raise ProductNotFoundError(f"Product {product_id} not found")

    def _to_entity(self, db_product: Product) -> ProductEntity:
        return ProductEntity(
            id=str(db_product.id),
            seller_id=str(db_product.seller_id),
            name=db_product.name,
            description=db_product.description,
            category=db_product.category,
            price=db_product.price,
            quantity=db_product.quantity,
            production_date=db_product.production_date,
            expiration_date=db_product.expiration_date,
            tags=db_product.tags,
            rating=db_product.rating,
            created_at=db_product.created_at,
            updated_at=db_product.updated_at
        )