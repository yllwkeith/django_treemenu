from django import template
from treemenu.models import MenuItem

register = template.Library()


def get_item_by_id(items, _id):
    for i in items:
        if i.id == _id:
            return i


@register.inclusion_tag('menu.html', takes_context=True)
def draw_menu(context, menu_slug):
    menu_items = MenuItem.objects.filter(menu__slug=menu_slug)
    if not menu_items:
        return {'error': "Menu doesn't exist or empty"}

    selected_item_id = context.get('menu_item_id')

    current_item = get_item_by_id(menu_items, selected_item_id)

    while current_item:
        # some monkey patching here to prevent hitting the DB
        children = [item for item in menu_items if item.parent_id == current_item.id]

        for c in children:
            c.is_open = hasattr(c, 'is_open') or False
        current_item.children_as_list = children
        current_item.is_open = True
        current_item = get_item_by_id(menu_items, current_item.parent_id)
    return {'menu_items': [item for item in menu_items if item.parent_id is None]}
