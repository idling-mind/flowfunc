# AUTO GENERATED FILE - DO NOT EDIT

#' @export
flowfunc <- function(id=NULL, comments=NULL, config=NULL, context=NULL, default_nodes=NULL, disable_pan=NULL, disable_zoom=NULL, double_clicked_node=NULL, editor_status=NULL, initial_scale=NULL, nodes=NULL, nodes_status=NULL, selected_nodes=NULL, space_to_pan=NULL, style=NULL, type_safety=NULL) {
    
    props <- list(id=id, comments=comments, config=config, context=context, default_nodes=default_nodes, disable_pan=disable_pan, disable_zoom=disable_zoom, double_clicked_node=double_clicked_node, editor_status=editor_status, initial_scale=initial_scale, nodes=nodes, nodes_status=nodes_status, selected_nodes=selected_nodes, space_to_pan=space_to_pan, style=style, type_safety=type_safety)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'Flowfunc',
        namespace = 'flowfunc',
        propNames = c('id', 'comments', 'config', 'context', 'default_nodes', 'disable_pan', 'disable_zoom', 'double_clicked_node', 'editor_status', 'initial_scale', 'nodes', 'nodes_status', 'selected_nodes', 'space_to_pan', 'style', 'type_safety'),
        package = 'flowfunc'
        )

    structure(component, class = c('dash_component', 'list'))
}
