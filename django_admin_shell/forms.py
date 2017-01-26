from django import forms


class ShellForm(forms.Form):

    code = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'codearea'}),
    )

    error_css_class = 'error'
