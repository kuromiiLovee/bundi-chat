import ulid
from tortoise import fields, models


class BaseModel(models.Model):
    """
    A shared base class that auto-generates ID when a record is saved in db.
    """

    id = fields.CharField(max_length=32, primary_key=True, index=True)

    async def save(self, *args, **kwargs):
        """
        Override `save()` to use ULID to generate ID on save.
        """
        if not self.id:
            self.id = str(ulid.new())[:32]
        await super().save(*args, **kwargs)

    class Meta:
        abstract = True


class TimestampMixin(models.Model):
    """
    A model mixin that adds timestamp fields for tracking creation and modification times.

    ---
    Attributes:
        created_at (fields.DatetimeField): The date and time when the record was created. Automatically set on creation.
        updated_at (fields.DatetimeField): The date and time when the record was last updated. Automatically updated on save.

    Meta:
        abstract (bool): Indicates that this model is intended to be used as a base class for
          other models and will not be created as a database table.
    """

    created_at = fields.DatetimeField(
        auto_now_add=True, description="The date and time when the record was created"
    )
    updated_at = fields.DatetimeField(
        auto_now=True, description="The date and time when the record was last updated"
    )

    class Meta:
        abstract = True  # use model as a base class for other models to inherit field
