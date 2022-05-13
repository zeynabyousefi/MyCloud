from django.db import models
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.username, filename)


class DirectoryModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=280)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    size = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class File(models.Model):
    name = models.CharField(max_length=280, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    directory = models.ForeignKey(DirectoryModel, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to=user_directory_path)

    @property
    def filename(self):
        name = self.file.name.split("/")[1].replace('_', ' ').replace('-', ' ')
        return name

    def __str__(self):
        return self.name


class PermissionUser(models.Model):
    TYPE = (
        ("d", "directory"),
        ("f", "file")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE, null=True, blank=True)
    directory = models.ForeignKey(DirectoryModel, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=1, choices=TYPE)

    def __str__(self):
        return self.id
