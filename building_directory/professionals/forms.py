from django import forms
from .models import Contract, Review
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


class ContractForm(forms.ModelForm):
    contract_type = forms.ChoiceField(choices=[('one_day', 'Un jour'), ('interval', 'Intervalle')])

    class Meta:
        model = Contract
        fields = ['start_date', 'end_date', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.professional = kwargs.pop('professional', None)
        super().__init__(*args, **kwargs)
        self.fields['end_date'].required = False

    def clean(self):
        cleaned_data = super().clean()
        contract_type = cleaned_data.get('contract_type')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if contract_type == 'one_day':
            cleaned_data['end_date'] = start_date

        if start_date:
            tomorrow = timezone.now().date() + timedelta(days=1)
            if start_date < tomorrow:
                raise ValidationError("La date de début doit être au moins pour demain.")

        if contract_type == 'interval' and start_date and end_date:
            if end_date <= start_date:
                raise ValidationError("La date de fin doit être postérieure à la date de début.")

        if self.professional:
            existing_confirmed_contract = Contract.objects.filter(
                professional=self.professional,
                status="confirmed",
                payment_status="paid",
                start_date__lte=end_date or start_date,
                end_date__gte=start_date
            )

            if self.instance.pk:
                existing_confirmed_contract = existing_confirmed_contract.exclude(pk=self.instance.pk)

            if existing_confirmed_contract.exists():
                raise ValidationError("Le professionnel a déjà un contrat confirmé et payé pour cette période.")

        return cleaned_data
    
    
    from django import forms
from .models import Review  # Assurez-vous que ce chemin est correct

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].required = True

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is None:
            raise forms.ValidationError("Une note est requise.")
        if not (1 <= rating <= 5):
            raise forms.ValidationError("La note doit être comprise entre 1 et 5.")
        return rating
    

