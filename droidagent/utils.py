
def add_period(text):
    if text.endswith('.'):
        return text
    else:
        return text + '.'

def remove_quotes(text):
    text = text.replace('"', '').replace("'", '')
    text = text.replace('\\n', '[NEWLINE]')
    text = text.replace('\\', '')
    return text

def remove_period(text):
    if text.endswith('.'):
        return text[:-1]
    else:
        return text

def __safe_dict_get(d, key, default=None):
    return d[key] if (key in d) else default


def __get_all_children(view_dict, views):
        """
        Get temp view ids of the given view's children
        :param view_dict: dict, an element of DeviceState.views
        :return: set of int, each int is a child node id
        """
        children = __safe_dict_get(view_dict, 'children')
        if not children:
            return set()
        children = set(children)
        for child in children:
            children_of_child = __get_all_children(views[child], views)
            children.union(children_of_child)
        return children


class GUIStateManager:
    activity_name_restore_map = {}

    @classmethod
    def fix_activity_name(cls, activity):
        original_activity_name = activity
        activity = activity.split('.')[-1]
        # if activity.startswith('.'):
        #     activity = f'{agent_config.package_name}.{activity[1:]}'
        if activity.endswith('}'):
            activity = activity[:-1]
        if activity.endswith('Activity'):
            activity = activity.removesuffix('Activity')
        elif activity.endswith('activity'):
            activity = activity.removesuffix('activity')

        if activity not in cls.activity_name_restore_map:
            cls.activity_name_restore_map[activity] = original_activity_name

        return activity