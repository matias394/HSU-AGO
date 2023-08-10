from django import forms
from django.contrib.auth.models import User,Group
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm, SetPasswordForm,PasswordResetForm
from .validators import MaxSizeFileValidator
from django.core.validators import MinValueValidator, MaxValueValidator


from .models import *
from .choices import *


usuarios=Usuarios.objects.all()


class UsuariosCreateForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
                        'type':'password', 
                        'name': 'password1',}),
                label=''
                )
    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
                        'type':'password', 
                        'name': 'password2',}),
                label='')
    
    imagen      = forms.ImageField(validators=[MaxSizeFileValidator(max_file_size=2)],required=False)
    telefono    = forms.IntegerField(required=False,widget=forms.NumberInput(attrs={'name': 'telefono',}))
    dni         = forms.IntegerField(required=True, validators=[MinValueValidator(3000000), MaxValueValidator(100000000)],widget=forms.NumberInput(attrs={'name': 'dni',}),)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  
        self.fields['password1'].label = "Contraseña"  
        self.fields['password2'].label = "Confirmar contraseña"  
        for fieldname in ['username', 'password1', 'password2','groups']:
            self.fields[fieldname].help_text = None
        self.fields['telefono'].label = "Teléfono"  
        self.fields['dni'].label = "DNI"

    def clean(self):
        cleaned_data = super(UsuariosCreateForm, self).clean()
        dni = cleaned_data.get('dni')
        # validacion de dni unico para la tabla
        if dni and Usuarios.objects.filter(dni=dni).exists():
            self.add_error('dni', 'ya existe un usuario con ese DNI.')
        return cleaned_data

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'groups')
        labels = {
            'first_name' : 'Nombres',
            'last_name'  : 'Apellidos',
            'username'  : 'Nombre de Usuario',
            'email'  : 'Email',
            'groups'  : 'Grupos de usuarios'
        }
        

class UsuariosUpdateForm(UserChangeForm):
    '''
    Formulario solo para usuario administrador
    '''
    imagen      = forms.ImageField(validators=[MaxSizeFileValidator(max_file_size=2)],required=False)
    telefono    = forms.IntegerField(help_text="Solo valores numéricos",required=False,widget=forms.NumberInput(attrs={'name': 'telefono',}))
    dni         = forms.IntegerField(required=True, validators=[MinValueValidator(3000000), MaxValueValidator(100000000)],widget=forms.NumberInput(attrs={'name': 'dni',}),)

    # groups = forms.ModelChoiceField(queryset=Group.objects.all(), required=True,label='Grupos', widget=forms.SelectMultiple(attrs={'class': 'select2 w-100','name': 'groups'},),)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        usuario=(usuarios.get(usuario_id=self.instance.pk))
        self.fields['telefono'].initial = usuario.telefono
        self.fields['imagen'].initial = usuario.imagen
        self.fields['dni'].initial = usuario.dni 
        for fieldname in ['username', 'telefono','groups', 'imagen','dni','is_active']:
            self.fields[fieldname].help_text = None
        self.fields['telefono'].label = "Teléfono"  
        self.fields['dni'].label = "DNI"

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email','is_active','groups',)
        widgets = {
            'is_active' : forms.Select(choices=[(True, 'Activo'), (False, 'Inactivo')])
        }
        labels = {
            'first_name' : 'Nombres',
            'last_name'  : 'Apellidos',
            'username'  : 'Nombre de Usuario',
            'email'  : 'Email',
            'groups'  : 'Grupos de usuarios',
            'is_active' : 'Estado'
        }
        

class PerfilUpdateForm(UserChangeForm):
    '''
    Formulario para usuario actual
    '''
    imagen = forms.ImageField(required=False, label="Foto Perfil", validators=[MaxSizeFileValidator(max_file_size=2)])    
    dni    = forms.IntegerField(required=True,widget=forms.NumberInput(attrs={'name': 'dni',}))
    telefono    = forms.IntegerField(required=False,widget=forms.NumberInput(attrs={'name': 'telefono',}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['telefono'].initial = (usuarios.get(usuario_id=self.instance.pk)).telefono
        self.fields['dni'].initial = (usuarios.get(usuario_id=self.instance.pk)).dni
        self.fields['imagen'].initial = (usuarios.get(usuario_id=self.instance.pk)).imagen
        for fieldname in ['username']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)
        

class GruposUsuariosForm(forms.ModelForm):
    
    programa   = forms.ModelChoiceField(required=True, label="Módulo" , queryset = Permission.objects.filter(codename__startswith='programa_').order_by('id')) 
    permiso    = forms.ModelChoiceField(label="Rol",required=True,queryset = Permission.objects.filter(codename__startswith='rol_').order_by('id')) 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["programa"].initial = Group.objects.get(id=self.instance.pk).permissions.all().get(codename__startswith='programa_')
            self.fields["permiso"].initial = Group.objects.get(id=self.instance.pk).permissions.all().get(codename__startswith='rol_')
            self.fields['programa'].label = "Módulo"   

    def clean_name(self):
        name = self.cleaned_data['name']
        if Group.objects.filter(name=name).exists():
            raise forms.ValidationError("Ya existe un grupo similar.")
        return name

    class Meta:
        model = Group
        fields = '__all__'

class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget = forms.PasswordInput()
        self.fields["new_password1"].widget = forms.PasswordInput()
        self.fields["new_password2"].widget = forms.PasswordInput()

class MySetPasswordFormm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget = forms.PasswordInput()
        self.fields["new_password2"].widget = forms.PasswordInput()

class MyResetPasswordForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget = forms.EmailInput(attrs={'class': 'border-0 font-weight-bold text-center','readonly': True})

