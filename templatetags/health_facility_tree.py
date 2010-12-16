"""
Template tags for presenting health facilities as a hierachical tree
"""
from django import template
from django.utils.safestring import mark_safe
register = template.Library()


class HealthTreeNode(template.Node):
    def __init__(self,template_nodes, queryset):
        self.template_nodes = template_nodes
        self.queryset=template.Variable(queryset)

    def _render_node(self, context, node):
        bits = []
        context.push()
        chldn=node.get_children()
        if chldn:
            for child in chldn:
                context['node'] = child
                bits.append(self._render_node(context, child))
        context['node'] = node
        context['children'] = mark_safe(u''.join(bits))
        rendered = self.template_nodes.render(context)
        context.pop()
        return rendered
    def render(self, context):
        facilities=self.queryset.resolve(context)
        #get root nodes
        root_nodes=facilities.filter(report_to_id=None)
        bits = [self._render_node(context, node) for node in root_nodes]
        return ''.join(bits)
            

@register.tag
def facilitytree(parser, token):
    """
    Populates a template variable with a ``QuerySet`` containing the
    the the health facilities.


    """
    try:

        tag,queryset=token.split_contents()
        template_nodes = parser.parse(('endfacilitytree',))
        parser.delete_first_token()
    except ValueError:
        msg="%r tag requires one arguments " %(token.contents[0])
        raise template.TemplateSyntaxError(msg)
    return HealthTreeNode(template_nodes,queryset)



  
    
    
