import { Colors, Controls } from 'flume'

const generateControl = (itype, defaultValueIfUndefined=undefined, defaultStep=undefined) => {
    return (props) => {
        const { name, label, defaultValue, ...others } = props
        return Controls.custom(
            {
                name: name,
                label: label,
                defaultValue: defaultValue ? defaultValue : defaultValueIfUndefined,
                render: (data, onChange, context, redraw, portProps, inputData) => {
                    return (
                        <>
                            <label
                            data-flume-component="control-label"
                            className="Control_controlLabel__3ga2-">
                                {Object.keys(inputData).length > 1 ? portProps.portName+"."+portProps.label : portProps.inputLabel}
                            </label>
                            <div className="TextInput_wrapper__tefOZ" data-flume-component="text-input">
                                <input
                                type={itype}
                                data-flume-component={`text-input-$(itype)`}
                                className="TextInput_input__1QHwS"
                                defaultValue={data}
                                step={portProps.step ? portProps.step : defaultStep}
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

const today = new Date();
const year = today.getFullYear();

const standardControls = {
    checkbox: Controls.checkbox,
    bool: Controls.checkbox,
    select: Controls.select,
    multiselect: Controls.multiselect,
    int: generateControl("number", 0, 1),
    number: generateControl("number", 0.0, 0.1),
    float: generateControl("number", 0.0, 0.1),
    str: generateControl("text", ""),
    text: generateControl("text", ""),
    color: generateControl("color", "#000000"),
    date: generateControl("date", `${year}-01-01`),
    time: generateControl("time", "00:00"),
    month: generateControl("month", `${year}-01`),
    week: generateControl("week", `${year}-W01`),
    slider: generateControl("range", 0.0),
}

/**
 * standardControls: Extra controls for Flume ports
 * standardControls are created to add to the regular controls exposed by flume
 * that can be added to a port. The plan is to add more and more controls here.
 */
export { standardControls }