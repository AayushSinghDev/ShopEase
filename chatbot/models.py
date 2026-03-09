from django.db import models


class ChatLog(models.Model):
    session_key = models.CharField(max_length=100)
    user_role = models.CharField(max_length=20, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Chat Log'
        verbose_name_plural = 'Chat Logs'

    def __str__(self):
        return f"[{self.session_key[:8]}] {self.user_message[:40]}"
