from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from .models import *


class CreateDirectory(View):
    def post(self, request):
        data = request.POST
        if data["directory_id"] == '0':
            DirectoryModel.objects.create(user=request.user, name=data["name"])
            return redirect("account:home")
        else:
            direcory = DirectoryModel.objects.get(id=str(data["directory_id"]))
            DirectoryModel.objects.create(user=request.user, name=data["name"], parent=direcory)
            return redirect("file:directory", id=direcory.id)


class CreateFile(LoginRequiredMixin, View):
    def post(self, request):
        files = request.FILES.getlist('files')
        if request.method == "POST":
            print("*" * 90)
            print(files)

            for f in files:
                File.objects.create(user=request.user, file=f)

            messages.success(request, 'You saved files successfully!')
            return render(request, "file/main.html")


class DirectoryView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            directory = DirectoryModel.objects.filter(user=user).filter(parent=id)
            return render(request, "file/main.html",
                          context={"user": request.user, "directory_id": id, "directory": directory})


class Delete_item(View):
    def get(self, request, type, id):
        return render(request, "file/manage.html", context={"type": type, "id": id})

    def post(self, request):
        data = request.POST
        if data["type"] == "delete_directory":
            directory = DirectoryModel.objects.get(id=data["id"])
            directory.delete()
            return redirect("account:home")
        elif data["type"] == "delete_file":
            pass


class Edit_item(View):
    def get(self, request, type, id):
        return render(request, "file/manage.html", context={"type": type, "id": id})

    def post(self, request):
        data = request.POST
        if data["type"] == "edit_directory":
            directory = DirectoryModel.objects.get(id=data["id"])
            directory.name = data["name"]
            directory.save()
            return redirect("account:home")
        elif data["type"] == "edit_file":
            pass


class Share_item(View):
    def get(self, request, type, id):
        return render(request, "file/manage.html", context={"type": type, "id": id})

    def post(self, request):
        data = request.POST
        if data["type"] == "share_directory":
            user = User.objects.get(username=data["username"])
            directory = DirectoryModel.objects.get(id=data["id"])
            PermissionUser.objects.create(user=user, type="d", directory=directory)
            return redirect("account:home")
        elif data["type"] == "share_file":
            pass
