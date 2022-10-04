% Auto-generated: do not edit by hand
\name{flowfunc}

\alias{flowfunc}

\title{Flowfunc component}

\description{
Flowfunc: A node editor for dash This component gives a flow based programming interface for dash users. The developer can define the nodes using simple python functions and these will be available as nodes which can be connected together to create a logic at runtime.
}

\usage{
flowfunc(id=NULL, comments=NULL, config=NULL, context=NULL,
default_nodes=NULL, disable_pan=NULL, disable_zoom=NULL,
double_clicked_node=NULL, editor_status=NULL,
initial_scale=NULL, nodes=NULL, nodes_status=NULL,
selected_nodes=NULL, space_to_pan=NULL, style=NULL,
type_safety=NULL)
}

\arguments{
\item{id}{Character. The ID used to identify this component in Dash callbacks.}

\item{comments}{Named list. Comments in the node editor}

\item{config}{Named list. The available port types and node types}

\item{context}{Named list. Pass extra data to nodes}

\item{default_nodes}{Unnamed list. Default nodes present in the editor
A list of nodes from the config}

\item{disable_pan}{Logical. Disable zoom option}

\item{disable_zoom}{Logical. Disable zoom option}

\item{double_clicked_node}{Character. Node on which a double click event was registered}

\item{editor_status}{Character. A property denoting the status of the editor
Following statuses are possible.
["client", "server"]}

\item{initial_scale}{Numeric. Initial zoom level of the editor}

\item{nodes}{Named list. The nodes of the node editor}

\item{nodes_status}{Named list. The status of each node on the editor}

\item{selected_nodes}{Unnamed list. The nodes of the node editor}

\item{space_to_pan}{Logical. Disable zoom option}

\item{style}{Named list. The style of the container div}

\item{type_safety}{Logical. If any port can connect to any other port}
}

\value{named list of JSON elements corresponding to React.js properties and their values}

