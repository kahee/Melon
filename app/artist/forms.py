from django import forms

from artist.models import Artist


# ModelForm
class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = [
            'img_profile',
            'name',
            'real_name',
            'nationality',
            'birth_date',
            'constellation',
            'blood_type',
            'intro',
        ]

        widgets = {
            # CLASS  지정
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'intro': forms.Textarea,

        }
