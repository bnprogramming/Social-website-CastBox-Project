
**Django CastBox Sample**

CastBox Sample is a Django app that clone the castbox website with django .
Application development and testing with django v4.2
Is use DTL , Js , HTML , CSS for this project


Quick start
-----------
1. Install all the packages and requirements with :
   
        pip install -r  requirements.txt
   
2. Set specific and custome settings for you project in ``settings.py``
3. open terminal and  make migrations  for ``models`` :

        python manage.py makemigrations     
        python manage.py migrate
   
4. Before all the things you should be logged in to use specific services , so at first:
   
          py manage.py createsuperuser
   
5. Then at last run the django server and run the app :

        python manage.py runserver
   
6. Then log in with url ``host:port/user-profile/login``        

7. You can register a new user with url ``host:port/user-profile/register``
   
8. If you add or register a new user you should go to the admin panel as a super superuser and make the new user active because they are none active by default   



