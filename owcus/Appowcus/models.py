from django.db import models
from django.contrib.auth.models import User

class School(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=20)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    def __str__(self):
        return f"{self.user.username} ({self.roll_no})"

class SchoolPost(models.Model):
    POST_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('text', 'Text'),
    ]
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    author = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES)
    media_url = models.URLField(blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(StudentProfile, related_name='liked_posts', blank=True)
    shares = models.ManyToManyField(StudentProfile, related_name='shared_posts', blank=True)
    def __str__(self):
        return f"{self.author.user.username}: {self.content[:30]}"

class StudentChat(models.Model):
    sender = models.ForeignKey(StudentProfile, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(StudentProfile, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.sender.user.username} → {self.receiver.user.username}: {self.message[:20]}"