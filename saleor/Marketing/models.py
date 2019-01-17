from django.db import models
from django.conf import settings
from django.contrib import admin
import mptt
from django.contrib.auth.models import User
from mptt.admin import MPTTModelAdmin
from mptt.admin import DraggableMPTTAdmin

class LevelTree(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, unique=True, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    def __unicode__(self):
        return self.user.username
    def level_insert_at(self, target, position='first-child', commit=False):
        print ('|--> mptt models.py level_insert_at')
        print ('good owerride')
        self._tree_manager.insert_node(self, target, position, commit)

mptt.register(LevelTree)
setattr(LevelTree, 'insert_at', LevelTree.level_insert_at)

class LevelTreeAdmin(MPTTModelAdmin):
    list_title_field = 'name'
    list_display = ('user',)
    class Meta:
        model = LevelTree

admin.site.register(
    LevelTree,
    LevelTreeAdmin,
)


class MarketingRates(models.Model):
    marketing_tree = models.CharField(max_length=50, choices=settings.TREE_TYPES)
    generation = models.IntegerField()
    commission = models.FloatField()
    def __unicode__(self):
        return self.marketing_tree
    class Meta:
        ordering = ('marketing_tree', )

class MarketingRatesAdmin(admin.ModelAdmin):
    list_display = ('marketing_tree', 'generation', 'commission',)

admin.site.register(MarketingRates, MarketingRatesAdmin)