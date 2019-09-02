from wtforms.fields import BooleanField, IntegerField, FormField
from wtforms.validators import Email
from wtforms_alchemy import ModelForm, model_form_factory, ModelFormField, ModelFieldList
#from autochannel import db
from autochannel.models import Guild, Category


class CategoryForm(ModelForm):
    class meta:
        model = Category
        #include_primary_keys = True
        # include = ['id', 'name', 'enabled', 'prefix']

class GuildForm(ModelForm):
    class Meta:
        model = Guild
        # include = ['id']
        include_primary_keys = True
    #categories = ModelFormField(CategoryForm)
    #categories = ModelFieldList(CategoryForm)
    #categories = ModelFieldList(CategoryForm)
    categories = ModelFieldList(FormField(CategoryForm))

