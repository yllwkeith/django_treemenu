from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class Menu(models.Model):
    title = models.CharField(max_length=64, help_text="It's useless")
    slug = models.SlugField(help_text="It's not, use draw_menu 'slug' for render")

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    parent = models.ForeignKey('self', verbose_name='parent', related_name='children', null=True, blank=True,
                               on_delete=models.SET_NULL)
    title = models.CharField(max_length=64)
    menu = models.ForeignKey(Menu, verbose_name='menu', related_name='menu_items', null=True, blank=True,
                             on_delete=models.SET_NULL)

    named_url = models.CharField(max_length=32, default='treemenu:menu-item')

    def get_absolute_url(self):
        return reverse(self.named_url, args=[str(self.id)])

    def save(self, *args, **kwargs):
        """
            There is some checks for circular items in menu and autoassigment menu filed for all items in branch
        """

        if self.parent:
            if self.menu is None and self.parent.menu:
                self.menu = self.parent.menu

            if self.menu and self.parent.menu != self.menu:
                self.parent.menu = self.menu
                self.parent.save(update_fields=['menu'])

        current_item = self
        while current_item:
            if current_item.parent != self:
                current_item = current_item.parent
            else:
                raise ValidationError("Circular menu items not allowed")

        for child in self.children.all():
            if self.menu and child.menu != self.menu:
                child.menu = self.menu
                child.save(update_fields=['menu'])

        # Everything is OK
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
