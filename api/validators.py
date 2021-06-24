from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime as dt

def validate_year(year):
    current_year = datetime.now().date().year
    if year > current_year: 
        raise ValidationError(
            _('%(year) more than current'),
            params={'year': year},
        )
