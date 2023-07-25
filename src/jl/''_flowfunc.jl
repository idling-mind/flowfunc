# AUTO GENERATED FILE - DO NOT EDIT

export ''_flowfunc

"""
    ''_flowfunc(;kwargs...)

A Flowfunc component.
Flowfunc: A node editor for dash
This component gives a flow based programming interface for dash users.
The developer can define the nodes using simple python functions and these
will be available as nodes which can be connected together to create a logic
at runtime.
Keyword arguments:
- `id` (String; optional): The ID used to identify this component in Dash callbacks.
- `comments` (Dict; optional): Comments in the node editor
- `config` (Dict; optional): The available port types and node types
- `context` (Dict; optional): Pass extra data to nodes
- `default_nodes` (Array; optional): Default nodes present in the editor
A list of nodes from the config
- `disable_pan` (Bool; optional): Disable zoom option
- `disable_zoom` (Bool; optional): Disable zoom option
- `double_clicked_node` (String; optional): Node on which a double click event was registered
- `editor_status` (String; optional): A property denoting the status of the editor
Following statuses are possible.
["client", "server"]
- `initial_scale` (Real; optional): Initial zoom level of the editor
- `nodes` (Dict; optional): The nodes of the node editor
- `nodes_status` (Dict; optional): The status of each node on the editor
- `selected_nodes` (Array; optional): The nodes of the node editor
- `space_to_pan` (Bool; optional): Disable zoom option
- `style` (Dict; optional): The style of the container div
- `type_safety` (Bool; optional): If any port can connect to any other port
"""
function ''_flowfunc(; kwargs...)
        available_props = Symbol[:id, :comments, :config, :context, :default_nodes, :disable_pan, :disable_zoom, :double_clicked_node, :editor_status, :initial_scale, :nodes, :nodes_status, :selected_nodes, :space_to_pan, :style, :type_safety]
        wild_props = Symbol[]
        return Component("''_flowfunc", "Flowfunc", "flowfunc", available_props, wild_props; kwargs...)
end

