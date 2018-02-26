from models import Lists

def get_lists(context):
    lists = Lists.objects.filter(owner=context.user.username)
    return {'todos_list':lists}