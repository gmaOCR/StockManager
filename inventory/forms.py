from django import forms
from .models import Produit, Mouvement, PrixVente, CoutAchat


class ProduitForm(forms.ModelForm):
    """Formulaire pour les produits"""
    
    class Meta:
        model = Produit
        fields = [
            'description', 'cout_achat', 'prix_vente', 'photo', 'seuil_alerte'
        ]
        widgets = {
            'description': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Опис товару'}
            ),
            'cout_achat': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}
            ),
            'prix_vente': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}
            ),
            'photo': forms.FileInput(
                attrs={'class': 'form-control', 'accept': 'image/*'}
            ),
            'seuil_alerte': forms.NumberInput(
                attrs={'class': 'form-control', 'min': '0'}
            ),
        }


class CoutAchatForm(forms.ModelForm):
    """Formulaire pour ajouter un nouveau coût d'achat"""
    
    class Meta:
        model = CoutAchat
        fields = ['cout', 'fournisseur', 'commentaire', 'actif']
        widgets = {
            'cout': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}
            ),
            'fournisseur': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Назва постачальника (необов\'язково)'
                }
            ),
            'commentaire': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Причина зміни вартості або деталі закупівлі'
                }
            ),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PrixVenteForm(forms.ModelForm):
    """Formulaire pour ajouter un nouveau prix de vente négocié"""
    
    class Meta:
        model = PrixVente
        fields = ['prix', 'client', 'commentaire', 'actif']
        widgets = {
            'prix': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}
            ),
            'client': forms.TextInput(
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Назва клієнта або контекст (необов\'язково)'
                }
            ),
            'commentaire': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Причина зміни ціни або деталі переговорів'
                }
            ),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class MouvementForm(forms.ModelForm):
    """Formulaire pour les mouvements"""
    
    class Meta:
        model = Mouvement
        fields = [
            'produit', 'type_mouvement', 'quantite',
            'prix_vente_utilise', 'cout_achat_utilise', 'commentaire'
        ]
        widgets = {
            'produit': forms.Select(attrs={
                'class': 'form-select',
                'onchange': 'loadPrixVenteEtCout(this.value)'
            }),
            'type_mouvement': forms.Select(attrs={
                'class': 'form-select',
                'onchange': 'togglePrixVenteEtCout()'
            }),
            'quantite': forms.NumberInput(
                attrs={'class': 'form-control', 'min': '1'}
            ),
            'prix_vente_utilise': forms.Select(attrs={
                'class': 'form-select',
                'style': 'display: none;'
            }),
            'cout_achat_utilise': forms.Select(attrs={
                'class': 'form-select',
                'style': 'display: none;'
            }),
            'commentaire': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Коментар (необов\'язково)'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['prix_vente_utilise'].required = False
        self.fields['cout_achat_utilise'].required = False


class FiltreMovementForm(forms.Form):
    """Formulaire de filtrage des mouvements"""
    TYPE_CHOICES = [
        ('', 'Всі типи'),
        ('entree', 'Надходження'),
        ('sortie', 'Вихід'),
    ]
    
    date_debut = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}
        ),
        label='Дата початку'
    )
    date_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}
        ),
        label='Дата кінця'
    )
    type_mouvement = forms.ChoiceField(
        choices=TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Тип операції'
    )
    produit = forms.ModelChoiceField(
        queryset=Produit.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Товар',
        empty_label='Всі товари'
    )
