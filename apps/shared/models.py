import uuid

from django.db import models


class AbstractModel(models.Model):
    """
    Abstract model class that provides common fields and functionality
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def get_model_fields(self) -> list:
        # TODO check if we will need this
        """
        Returns a list of field.attname for this model. This is useful for
        :return: list of field.attname
        """
        return [field.name for field in self._meta.fields]
