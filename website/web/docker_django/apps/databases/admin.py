from django.contrib import admin
from import_export.admin import ImportMixin
from import_export import resources, fields
from .models import NOTIFICATIONS, MUTANTS, MEETINGS

# create a resource to allow for csv upload in STRAIN model
class MutantResource(resources.ModelResource):
    INDEX = fields.Field(attribute='INDEX', column_name='INDEX')
    LOCATION_IDENTIFIER = fields.Field(attribute='LOCATION_IDENTIFIER', column_name='LOCATION_IDENTIFIER')
    GROUP = fields.Field(attribute='GROUP', column_name='GROUP')
    COLLECTION_NUMBER = fields.Field(attribute='COLLECTION_NUMBER', column_name='COLLECTION_NUMBER')
    GENOTYPE = fields.Field(attribute='GENOTYPE', column_name='GENOTYPE')
    CONSTRUCTION_DETAILS = fields.Field(attribute='CONSTRUCTION_DETAILS', column_name='CONSTRUCTION_DETAILS')
    DATE = fields.Field(attribute='DATE', column_name='DATE')
    LAB_MEMBER = fields.Field(attribute='LAB_MEMBER', column_name='LAB_MEMBER')
    GROWTH_CONDITIONS = fields.Field(attribute='GROWTH_CONDITIONS', column_name='GROWTH_CONDITIONS')
    KNOWN_AS = fields.Field(attribute='KNOWN_AS', column_name='KNOWN_AS')
    NOTES = fields.Field(attribute='NOTES', column_name='NOTES')
    ADDED_TO_DB = fields.Field(attribute='ADDED_TO_DB', column_name='ADDED_TO_DB')

    def get_instance(self, instance_loader, row):
        # Returning False prevents us from looking in the
        # database for rows that already exist
        return False

    class Meta:
        model = MUTANTS
        fields = ('INDEX', 'LOCATION_IDENTIFIER', 'GROUP', 'COLLECTION_NUMBER', 'GENOTYPE', 'CONSTRUCTION_DETAILS', 'DATE', 'LAB_MEMBER', 'GROWTH_CONDITIONS', 'KNOWN_AS', 'NOTES', 'ADDED_TO_DB')
        export_order = fields
        import_id_fields = ('LOCATION_IDENTIFIER',)

class MutantAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = MutantResource

# create a resource to allow for csv upload in MEETINGS model
class MeetingsResource(resources.ModelResource):
    DATE = fields.Field(attribute='DATE', column_name='DATE')
    TIME = fields.Field(attribute='TIME', column_name='TIME')
    VENUE = fields.Field(attribute='VENUE', column_name='VENUE')
    SPEAKER = fields.Field(attribute='SPEAKER', column_name='SPEAKER')
    TOPIC = fields.Field(attribute='TOPIC', column_name='TOPIC')

    def get_instance(self, instance_loader, row):
        return False

    class Meta:
        model = MEETINGS
        fields = ('DATE', 'TIME', 'VENUE', 'SPEAKER', 'TOPIC')
        export_order = fields
        import_id_fields = ('DATE',)

class MeetingsAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = MeetingsResource

# register models with admin site
admin.site.register(NOTIFICATIONS)
admin.site.register(MUTANTS, MutantAdmin)
admin.site.register(MEETINGS, MeetingsAdmin)
