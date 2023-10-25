from .models import User

class GetUser():
    def get_user(self, pk):
        return User.objects.filter(pk=pk).first()
    
    def delete_user(self, pk):
        User.objects.filter(pk=pk).first().delete()
    

class UserScore():
    def give_points(self, user_id, points):
        user = GetUser().get_user(pk=user_id)
        if user:
            user.count_point += points
            user.save()
            return True
        
        return False
    

