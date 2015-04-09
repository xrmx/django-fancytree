from django.db import models
from django.core.urlresolvers import reverse
from django_extensions.db.fields import AutoSlugField
import mptt

from urlparse import urljoin

class Category(models.Model):
    parent = models.ForeignKey('self',
                               null=True,
                               blank=True,
                               related_name='children')
    name = models.CharField(max_length=50)
    slug = AutoSlugField(max_length=50,
                         overwrite=True,
                         populate_from='name')
    url = models.TextField(editable=False)

    class Meta:
        verbose_name_plural = "categories"
        unique_together = (("name", "slug", "parent"), )
        ordering = ("tree_id", "lft")

    def __unicode__(self):
        return self.url

    def save(self, force_insert=False, force_update=False, **kwargs):
        super(Category, self).save(
            force_insert=force_insert,
            force_update=force_update,
            **kwargs)
        self.update_url()

    def get_tree(self, *args):
        """
        Return the tree structure for this element
        """
        level_representation = "--"
        if self.level == 0:
            node = "| "
        else:
            node = "+ "
        _tree_structure = node + level_representation * self.level
        return _tree_structure
    get_tree.short_description = 'tree'

    def get_repr(self, *args):
        """
        Return the branch representation for this element
        """
        level_representation = "--"
        if self.level == 0:
            node = "| "
        else:
            node = "+ "
        _tree_structure = node + level_representation * self.level + ' ' + self.name
        return _tree_structure
    get_repr.short_description = 'representation'

    def tree_order(self):
        return str(self.tree_id) + str(self.lft)

    def update_url(self):
        """
        Updates the url for this Category and all children Categories.
        """
        url = urljoin(getattr(self.parent, 'url', '') + '/', self.slug)
        if url != self.url:
            self.url = url
            self.save()

            for child in self.get_children():
                child.update_url()

mptt.register(Category, order_insertion_by=['name'])

class Selection (models.Model):
    name = models.CharField(max_length=50)
    categories = models.ManyToManyField(Category)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('selection', args=[self.pk])
