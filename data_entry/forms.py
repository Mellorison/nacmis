from django import forms


from .models import NationalOrganisation, StakeholderDirectory, ProgramActivity, TargetGroupPreventionMessage, \
    District, Ward, UserProfile, OtherQuestion, DACAValidation, PITMEOValidation
from .models import ActivityReportForm, IECMaterial
from django.forms import ValidationError
from dal import autocomplete


class NationalOrganisationModelForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        organisation_name = cleaned_data.get("organisation_name")
        organisation_address = cleaned_data.get("organisation_address")
        organisation_contact_email = cleaned_data.get("organisation_contact_email")

        if not (organisation_name and organisation_address and organisation_contact_email):
            raise forms.ValidationError('The System requires you to enter all fields.')
    
    class Meta: 
        model =NationalOrganisation
        fields = '__all__'

class StakeholderDirectoryModelForm(forms.ModelForm):

    class Meta:
        model = StakeholderDirectory
        fields = ['national_organisation', 'organisation_address', 'organisation_targets', 'organisation_province', 
            'organisation_district', 'start_year']

        widgets = {
            'national_organisation' : autocomplete.ModelSelect2(url='national-organisation-autocomplete'),
            'organisation_address' : forms.TextInput(attrs={'placeholder':'Enter district address'}),
            'organisation_targets' : autocomplete.ModelSelect2Multiple(url='organisationtarget-autocomplete'),
            'organisation_district' : autocomplete.ModelSelect2(url='district-autocomplete', forward=['organisation_province']),
            'start_year': forms.TextInput(attrs={'placeholder':'YYYY-MM-DD',}),
        }

class UserProfileModelForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        national_organisation = cleaned_data.get("national_organisation")
        stakeholder = cleaned_data.get("stakeholder")

        if not (national_organisation or stakeholder):
            raise forms.ValidationError('Please complete the User profile by selecting National organisation and/or stakeholder.')
        
    class Meta:
        model = UserProfile
        fields = ('__all__')

        widgets = {
            'national_organisation' : autocomplete.ModelSelect2(url='national-organisation-autocomplete', forward=['organisation_province']),
            'district' : autocomplete.ModelSelect2(url='district-autocomplete', forward=['province']),
            'stakeholder' : autocomplete.ModelSelect2(url='stakeholder-autocomplete', forward=['national_organisation']),
        }

class ActivityReportFormModelForm(forms.ModelForm):
    class Meta:
        model = ActivityReportForm
        #fields = ['report_date', 'quarter_been_reported', 'stake_holder_name', 'name', 'telephone_number', 'email_address',]
        fields = ('__all__')
        widgets = {
            'report_date' : forms.TextInput(attrs={'placeholder':'YYYY-MM-DD', 'type':'date',}),
        }

    def clean(self):
        cleaned_data = super().clean()
        form_quarter_been_reported = cleaned_data.get('quarter_been_reported')
        form_stake_holder_name = cleaned_data.get('stake_holder_name')
        if self.instance.pk: 
            #If the form already exists, only check if the quarter is selected in other similar forms whose pk is different
            existing_sarf_for_quarter = ActivityReportForm.objects.filter(quarter_been_reported=form_quarter_been_reported, stake_holder_name=form_stake_holder_name).exclude(pk=self.instance.pk)
            if existing_sarf_for_quarter:
                raise ValidationError("A Stakeholder Activity Report Form for this stakeholder: '%s' has already been recorded for %s"%(form_stake_holder_name, existing_sarf_for_quarter[0].get_quarter_been_reported_display()))
            return
        else: #No ID, this is a new form so we should run the quarters validation to make sure it is not duplication another form for the same quarter.
            existing_sarf_for_quarter = ActivityReportForm.objects.filter(quarter_been_reported=form_quarter_been_reported, stake_holder_name=form_stake_holder_name)
            if existing_sarf_for_quarter:
                raise ValidationError("A Stakeholder Activity Report Form for this stakeholder: '%s' has already been recorded for %s"%(form_stake_holder_name, existing_sarf_for_quarter[0].get_quarter_been_reported_display()))

class ProgramActivityModelForm(forms.ModelForm):
    # organisation_district
    class Meta:
        model = ProgramActivity
        fields = '__all__'
        
        widgets = {
            #'areas_of_support': autocomplete.ModelSelect2Multiple(url='supportfield-autocomplete'),
            'areas_of_support2': autocomplete.ModelSelect2Multiple(url='supportbyarea-autocomplete'),
            'ward':  autocomplete.ModelSelect2(url='ward-autocomplete', forward=['organisation_district'])
        }


class OtherQuestionModelForm(forms.ModelForm):
    class Meta:
        model = OtherQuestion
        fields = '__all__'

        widgets = {
            'sources_of_information' : autocomplete.ModelSelect2Multiple(url='supportofinformation-autocomplete'),
        }

class WardModelForm(forms.ModelForm):
    class Meta:
        model = Ward
        fields = '__all__'

        widgets = {
            'district' : autocomplete.ModelSelect2(url='district-autocomplete', forward=['organisation_province']),
        }

class TargetGroupPreventionMessageModelForm(forms.ModelForm):

    class Meta:
        model = TargetGroupPreventionMessage
        fields = '__all__'
        
        widgets = {
            'prevention_list': autocomplete.ModelSelect2(url='preventionmessagelist-autocomplete',),
            'target_groups': autocomplete.ModelSelect2Multiple(url='organisationtarget-autocomplete'),
        }

class IECMaterialModelForm(forms.ModelForm):
    class Meta:
        model = IECMaterial
        fields = '__all__'
        widgets = {
            'targeted_audience': autocomplete.ModelSelect2Multiple(url='organisationtarget-autocomplete'),
        }
class DACAValidationForm(forms.ModelForm):
    class Meta:
        model = DACAValidation
        fields = '__all__'

class PITMEOValidationForm(forms.ModelForm):
    class Meta:
        model = PITMEOValidation
        fields = '__all__'

class MyForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
   
