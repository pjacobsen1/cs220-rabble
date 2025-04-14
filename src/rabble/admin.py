from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(Following)
admin.site.register(Community)
admin.site.register(CommunityMember)
admin.site.register(Subrabble)
admin.site.register(SubrabbleMember)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Conversation)
admin.site.register(ConversationMember)
admin.site.register(ConversationMessage)
admin.site.register(CommunityInvite)
