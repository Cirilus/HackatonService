from .models import User

class GetUser():
    def delete_user(self, pk):
        User.objects.filter(pk=pk).first().delete()