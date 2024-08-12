from django.contrib.auth.models import User

# Obtén el usuario que creaste manualmente
user = User.objects.get(username='edwin')

# Encripta la contraseña correctamente
user.set_password('123')
user.save()