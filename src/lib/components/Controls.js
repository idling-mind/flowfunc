import { Colors, Controls } from 'flume'

const generateControl = (itype) => {
    return (props) => {
        const { name, label, ...others } = props
        return Controls.custom(
            {
                name: name,
                label: label,
                render: (data, onChange, context, redraw, portProps, inputData) => {
                    return (
                        <>
                            <label data-flume-component="control-label" className="Control_controlLabel__3ga2-">{portProps.label}</label>
                            <div className="TextInput_wrapper__tefOZ" data-flume-component="text-input">
                                <input
                                type={itype}
                                data-flume-component={`text-input-$(itype)`}
                                className="TextInput_input__1QHwS"
                                defaultValue={data}
                                onChange={
                                    (e) => {
                                        e.target.title = e.target.value;
                                        onChange(e.target.value)
                                    }
                                }
                                onMouseDown={
                                    (e) => e.stopPropagation()
                                }
                                onDrag={
                                    (e) => e.stopPropagation()
                                }
                                onDragStart={
                                    (e) => e.stopPropagation()
                                }
                                {...others}
                                />
                            </div>
                        </>
                    )
                }
            }
        )
    }
}

const standardControls = {
    str: Controls.text,
    checkbox: Controls.checkbox,
    bool: Controls.checkbox,
    select: Controls.select,
    multiselect: Controls.multiselect,
    text: generateControl("text"),
    int: generateControl("number"),
    float: generateControl("number"),
    number: generateControl("number"),
    color: generateControl("color"),
    date: generateControl("date"),
    time: generateControl("time"),
    month: generateControl("month"),
    week: generateControl("week"),
    slider: generateControl("range"),
}

/**
 * standardControls: Extra controls for Flume ports
 * standardControls are created to add to the regular controls exposed by flume
 * that can be added to a port. The plan is to add more and more controls here.
 */
export { standardControls }