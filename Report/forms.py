from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from Report.models import HardwareManagementConsole
from django import forms
from django.core.urlresolvers import reverse_lazy
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

class HMCForm(ModelForm):

    class Meta:
        model=HardwareManagementConsole
        fields = ['ip','name','username','password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self,*args ,**kargs):
        super(HMCForm,self).__init__(*args,**kargs)
        self.fields['ip'].widget.attrs['placeholder'] = "HMC IP"
        self.fields['name'].widget.attrs['placeholder'] = "HMC Name"
        self.fields['username'].widget.attrs['placeholder'] = "HMC Username"
        self.fields['password'].widget.attrs['placeholder'] = "HMC Password"

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_action = '/index/'
        self.helper.layout = Layout(  # the order of the items in this layout is important
            'name',
            'ip',  # field1 will appear first in HTML
            'username',
            'password',
            # this is how to add the submit button to your form and since it is the last item in this tuple, it will be rendered last in the HTML
            Submit('submit', u'Add', css_class='btn btn-success'),
        )


def update_select():
    CHOICES = []
    hmc_list = HardwareManagementConsole.objects.all()

    for i, j in enumerate(hmc_list):
        name_ip = j.name + " - " + j.ip
        CHOICES.append((str(i), name_ip))
    CHOICES = tuple(CHOICES)
    return CHOICES
class HMCSelectForm(forms.Form):
    field = forms.ChoiceField(choices=update_select())

    def __init__(self,*args ,**kargs):
        super(HMCSelectForm, self).__init__(*args, **kargs)
        self.fields['field'].choices = update_select()
        print("I start when the camapnas suenan")
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_action = '/hmc_report/'
        self.helper.layout = Layout(
            'field',
            Submit('submit', u'Select', css_class='btn btn-success'),
        )


