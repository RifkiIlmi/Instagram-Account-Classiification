from import_export import resources, fields
from .models import Data

class DataResource(resources.ModelResource):
    class Meta:
        model = Data
        import_id_fields = ('link',)
        exclude = ('id',)
        skip_unchanged = True
        fields = ('link','caption','username','label',)