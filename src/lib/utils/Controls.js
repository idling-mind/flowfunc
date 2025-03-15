import { Colors, Controls } from 'flume'

const generateControl = (itype) => {
    return (props) => {
        const {name, label, others} = props
        return Controls.custom(
            {
                name: name,
                label: label,
                render: (data, onChange, context, redraw, portProps, inputData) => {
                    return (
                        <>
                            <label data-flume-component="control-label" className="Control_controlLabel__3ga2-">{portProps.label}</label>
                            <div className="TextInput_wrapper__tefOZ" data-flume-component="text-input">
                                <input type={itype} data-flume-component={`text-input-$(itype)`} className="TextInput_input__1QHwS" defaultValue={data} onChange={(e) => onChange(e.target.value)} {...others} />
                            </div>
                        </>
                    )
                }
            }
        )
    }
}

const objectControl = (props) => {
    return Controls.custom(
        {
            name: props.name,
            label: props.label,
            render: (data, onChange, context, redraw, portProps, inputData) => {
                return (
                    <label data-flume-component="control-label" className="Control_controlLabel__3ga2-">{portProps.label}</label>
                )
            }
        }
    )
}

const standardControls = {
    number: Controls.number,
    int: Controls.number,
    float: Controls.number,
    text: Controls.text,
    str: Controls.text,
    checkbox: Controls.checkbox,
    bool: Controls.checkbox,
    select: Controls.select,
    multiselect: Controls.multiselect,
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