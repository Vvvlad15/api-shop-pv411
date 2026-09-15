from django import forms

class ContactForm(forms.Form):
    """Форма зворотного зв'язку (не пов'язана з моделлю БД)"""
    name = forms.CharField(
        max_length=100,
        label="Ваше ім'я",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': "Введіть ваше ім'я"
        })
    )
    email = forms.EmailField(
        label="Email-адреса",
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': "example@email.com"
        })
    )
    subject = forms.CharField(
        max_length=200,
        label="Тема повідомлення",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': "З якого питання звертаєтесь?"
        })
    )
    message = forms.CharField(
        label="Текст повідомлення",
        widget=forms.Textarea(attrs={
            'class': 'form-input',
            'placeholder': "Напишіть ваше повідомлення тут...",
            'rows': 6
        })
    )
