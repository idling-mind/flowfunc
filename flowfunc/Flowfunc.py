# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Flowfunc(Component):
    """A Flowfunc component.
Flowfunc: A node editor for dash
This component gives a flow based programming interface for dash users.
The developer can define the nodes using simple python functions and these
will be available as nodes which can be connected together to create a logic
at runtime.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- comments (dict; optional):
    Comments in the node editor.

- config (dict; optional):
    The available port types and node types.

- context (dict; optional):
    Pass extra data to nodes.

- default_nodes (list; optional):
    Default nodes present in the editor  A list of nodes from the
    config.

- disable_pan (boolean; optional):
    Disable zoom option.

- disable_zoom (boolean; optional):
    Disable zoom option.

- double_clicked_node (string; optional):
    Node on which a double click event was registered.

- editor_status (string; optional):
    A property denoting the status of the editor  Following statuses
    are possible.  [\"client\", \"server\"].

- initial_scale (number; optional):
    Initial zoom level of the editor.

- nodes (dict; optional):
    The nodes of the node editor.

- nodes_status (dict; optional):
    The status of each node on the editor.

- selected_nodes (list; optional):
    The nodes of the node editor.

- space_to_pan (boolean; optional):
    Disable zoom option.

- style (dict; optional):
    The style of the container div.

- type_safety (boolean; optional):
    If any port can connect to any other port."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'flowfunc'
    _type = 'Flowfunc'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, style=Component.UNDEFINED, nodes=Component.UNDEFINED, nodes_status=Component.UNDEFINED, editor_status=Component.UNDEFINED, selected_nodes=Component.UNDEFINED, double_clicked_node=Component.UNDEFINED, comments=Component.UNDEFINED, type_safety=Component.UNDEFINED, default_nodes=Component.UNDEFINED, context=Component.UNDEFINED, initial_scale=Component.UNDEFINED, disable_zoom=Component.UNDEFINED, disable_pan=Component.UNDEFINED, space_to_pan=Component.UNDEFINED, config=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'comments', 'config', 'context', 'default_nodes', 'disable_pan', 'disable_zoom', 'double_clicked_node', 'editor_status', 'initial_scale', 'nodes', 'nodes_status', 'selected_nodes', 'space_to_pan', 'style', 'type_safety']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'comments', 'config', 'context', 'default_nodes', 'disable_pan', 'disable_zoom', 'double_clicked_node', 'editor_status', 'initial_scale', 'nodes', 'nodes_status', 'selected_nodes', 'space_to_pan', 'style', 'type_safety']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Flowfunc, self).__init__(**args)
