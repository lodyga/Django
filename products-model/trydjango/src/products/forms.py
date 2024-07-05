from django import forms
from products.models import Product

# widget=forms.Textarea(
#                         attrs={
#                             "placeholder": "Provide some description",
#                             "class": "new-class-name two",
#                             "rows": 20,
#                             "cols": 100,
#                             "id": "some_id"
#                             }
#                         ),

class ProductForm(forms.ModelForm):
    # title       = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Some placeholder"}))
    title       = forms.CharField()
    email       = forms.EmailField()
    description = forms.CharField(
                    required=False, 
                    widget=forms.Textarea(
                        attrs={"cols": 100,}
                    ))
    price       = forms.DecimalField(initial=199.99)

    class Meta:
        model = Product
        # fields = "__all__"
        fields = [
                  "title", 
                  "description",
                  "email",
                  "price"
                  ]

    # def clean_title(self, *args, **kwargs):
    #     title = self.cleaned_data.get("title")
    #     if not "ukasz" in title:
    #         raise forms.ValidationError("This is not a valit title")
    #     else:
    #         return title
    
    # def clean_email(self, *args, **kwargs):
    #     email = self.cleaned_data.get("email")
    #     if not "@" in email:
    #         raise forms.ValidationError("This is not a valit email")
    #     else:
    #         return email


class RawProductForm(forms.Form):
    title       = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Some placeholder"}))
    description = forms.CharField(
                    required=False, 
                    widget=forms.Textarea(
                        attrs={
                            "placeholder": "Provide some description",
                            "class": "new-class-name two",
                            "rows": 20,
                            "cols": 100,
                            "id": "some_id"
                            }
                        ),
                    )
    price       = forms.DecimalField(initial=100)
    
