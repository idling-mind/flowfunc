import React, { Component } from 'react';
import * as R from 'ramda'
import { NodeEditor } from 'flume';
import { FlumeConfig, Colors, Controls } from 'flume'
import PropTypes, { string } from 'prop-types';
import { standardControls } from '../utils/Controls';
import "./nodeeditor.css"

/**
 * Flowfunc: A node editor for dash
 * This component gives a flow based programming interface for dash users.
 * The developer can define the nodes using simple python functions and these
 * will be available as nodes which can be connected together to create a logic
 * at runtime.
 */
export default class Flowfunc extends Component {

  constructor(props) {
    super(props)
    this.nodeEditor = React.createRef();
    this.container = React.createRef();
    this.ukey = (new Date()).toISOString();
    this.localSelectedNodes = new Set();
    this.updateConfig();
  }

  updateConfig = () => {
    // Function to convert the python based config data to a FlumeConfig object
    const config = this.props.config;
    this.flconfig = new FlumeConfig();
    // Adding all standard ports first
    for (const port of config.portTypes) {
      const { color, controls, ...port_obj } = port;
      if (!R.isNil(color) && !R.isEmpty(color)) {
        port_obj.color = Colors[color];
      }
      if (!R.isNil(controls) && !R.isEmpty(controls)) {
        port_obj.controls = controls.map(control => {
          const { type, ...others } = control;
          return standardControls[type]({
            ...others
          })
        })
      }
      else {
        port_obj.controls = [
          Controls.custom({
            name: port_obj.type,
            label: port_obj.label,
            defaultValue: null,
            render: (data, onChange, context, redraw, portProps, inputData) => {
              return <label data-flume-component="port-label" className="IoPorts_portLabel__qOE7y"> {portProps.inputLabel}</label>;
            }
          })
        ];
      }
      try {
        //The standard ports are already added and hence will cause an error here
        this.flconfig.addPortType(port_obj);
      } catch (e) {
      }
    }
    for (const node of config.nodeTypes) {
      const { inputs, outputs, label, category, ...node_obj } = node;
      if (!R.isNil(inputs) && !R.isEmpty(inputs)) {
        if (R.hasIn("source", inputs)) {
          var func = new Function(inputs.source);
          node_obj.inputs = ports => (inputData, connections, context) => {
            return func(ports, inputData, connections, context)
          }
        }
        else if (R.hasIn("path", inputs)) {
          try{
            node_obj.inputs = ports => (inputData, connections, context) => {
              var func = window.dash_clientside.flowfunc[inputs.path];
              return func(ports, inputData, connections, context)
            }
          }
          catch (e){
            console.log("Error in evaluating function from path", e);
          }
        }
        else {
          node_obj.inputs = (ports) => inputs.map(input => {
            const { type, controls, ...input_data } = input;
            // console.log(input, type, controls, input_data);
            return ports[type](input_data);
          })
        }
      }
      if (!R.isNil(outputs) && !R.isEmpty(outputs)) {
        node_obj.outputs = (ports) => outputs.map(output => {
          const { type, controls, ...output_data } = output;
          return ports[type](output_data);
        })
      }
      if (!R.isNil(category) && !R.isEmpty(category)) {
        node_obj.label = `${category}: ${label}`;
      } else {
        node_obj.label = label;
      }
      this.flconfig.addNodeType(node_obj);
    }
    // console.log(this.flconfig);
    if (!this.props.type_safety) {
      // Use acceptTypes from the object port
      const allPortTypes = this.flconfig.portTypes.object.acceptTypes;
      for (const [type, obj] of Object.entries(this.flconfig.portTypes)) {
        obj.acceptTypes = allPortTypes;
      }
    }
  }

  handleChange = () => {
    // Dash function which will raise the nodes properties
    this.props.setProps({
      editor_status: "client",
      nodes: this.nodeEditor.current.getNodes(),
      comments: this.nodeEditor.current.getComments(),
    })
    // console.log(this.props.comments);
    // console.log(this.props.nodes);
  }

  componentDidMount() {
    this.addEventListners(); // Adding on click event listners to nodes
    // console.log("Adding listeners")
  }

  componentDidUpdate(prevProps) {
    if (this.props.config !== prevProps.config) {
      this.updateConfig();
    }
    if (this.props.editor_status === "server") {
      // console.log("Pushing new nodes", this.props.nodes)
      this.ukey = (Math.random() + 1).toString(36).substring(7);
    }
    this.setNodesStatus();
  }

  setNodeStatus = (id, status) => {
    const nodeDiv = this.container.current.querySelector('[data-node-id="' + id + '"]');
    if (status) {
      // Removing any existing classes
      const classes = ["started", "queued", "deferred", "finished", "canceled", "stopped", "scheduled", "failed"];
      nodeDiv.classList.remove(...classes);
      nodeDiv.classList.add(status); // Status itself is added as the class
    }
  }

  setNodesStatus = () => {
    if (R.isNil(this.props.nodes_status) | R.isEmpty(this.props.nodes_status)) {
      return
    }
    for (const [id, node] of Object.entries(this.props.nodes_status)) {
      try {
        this.setNodeStatus(id, node);
      } catch (error) {
        // console.log(error);
      }
    }
  }

  addEventListners = () => {
    const comp = this;
    const stage = this.container.current
    var containerEventListenerAdded = stage.getAttribute("data-event-click");
    if (containerEventListenerAdded !== "true") {
      stage.addEventListener('click', function (e) {
        // console.log("Clicked", e);
        if (!e.ctrlKey) {
          comp.localSelectedNodes = new Set();
          for (const [id, node] of Object.entries(comp.props.nodes)) {
            try {
              const nodeDiv = stage.querySelector('[data-node-id = "' + id + '"]');
              nodeDiv.classList.remove("active")
            } catch (error) {
              // console.log("error", error, node);
            }
          }
        }
        const nodeDiv = e.target.closest('[class^=Node_wrapper]')
        if (nodeDiv) {
          var nodeId = nodeDiv.getAttribute('data-node-id');
          comp.localSelectedNodes.add(nodeId);
          nodeDiv.classList.add("active")
        }
        comp.props.setProps({ selected_nodes: [...comp.localSelectedNodes] });
      })
      stage.addEventListener('dblclick', function (e) {
        const nodeDiv = e.target.closest('[class^=Node_wrapper]')
        if (nodeDiv) {
          var nodeId = nodeDiv.getAttribute('data-node-id');
          comp.props.setProps({ double_clicked_node: nodeId });
        }
      })
      stage.setAttribute("data-event-click", "true");
    }
  }


  render() {
    // this.nodeEditor.current.setNodes(this.props.nodes);
    const output = (
      <div id={this.props.id} style={{ height: "100%", zIndex: -1 }} ref={this.container}>
        <NodeEditor
          ref={this.nodeEditor}
          portTypes={this.flconfig.portTypes}
          nodeTypes={this.flconfig.nodeTypes}
          nodes={this.props.nodes}
          defaultNodes={this.props.default_nodes}
          context={this.props.context}
          initialScale={this.props.initial_scale}
          disableZoom={this.props.disable_zoom}
          disablePan={this.props.disable_pan}
          spaceToPan={this.props.space_to_pan}
          onChange={this.handleChange}
          onCommentsChange={this.handleChange}
          key={this.ukey}
        />
      </div>
    );
    return output;
  }
}

Flowfunc.defaultProps = {};

Flowfunc.propTypes = {
  /**
   * The ID used to identify this component in Dash callbacks.
   */
  id: PropTypes.string,

  /**
   * The style of the container div
   */
  style: PropTypes.object,

  /**
   * The nodes of the node editor
   */
  nodes: PropTypes.object,

  /**
   * The status of each node on the editor
   */
  nodes_status: PropTypes.object,

  /**
   * A property denoting the status of the editor
   * Following statuses are possible.
   * ["client", "server"]
   */
  editor_status: PropTypes.string,

  /**
   * The nodes of the node editor
   */
  selected_nodes: PropTypes.array,
  /**
   * Node on which a double click event was registered
   */
  double_clicked_node: PropTypes.string,

  /**
   * Comments in the node editor
   */
  comments: PropTypes.object,
  /**
   * If any port can connect to any other port
   */
  type_safety: PropTypes.bool,

  /**
   * Default nodes present in the editor
   * A list of nodes from the config
   */
  default_nodes: PropTypes.array,

  /**
   * Pass extra data to nodes
   */
  context: PropTypes.object,

  /**
   * Initial zoom level of the editor
   */
  initial_scale: PropTypes.number,

  /**
   * Disable zoom option
   */
  disable_zoom: PropTypes.bool,

  /**
   * Disable zoom option
   */
  disable_pan: PropTypes.bool,

  /**
   * Disable zoom option
   */
  space_to_pan: PropTypes.bool,


  /**
   * The available port types and node types
   */
  config: PropTypes.object,

  /**
   * Dash-assigned callback that should be called to report property changes
   * to Dash, to make them available for callbacks.
   */
  setProps: PropTypes.func
};
