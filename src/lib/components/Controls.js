import { Colors, Controls } from 'flume'

const generateControl = (itype) => {
    return (others) => {
        return Controls.custom(
            {
                name: others.name,
                label: others.label,
                render: (data, onChange, context, redraw, portProps, inputData) => {
                    return (
                        <input type={itype} value={data} className="TextInput_input__1QHwS" onChange={e => (onChange(e.target.value))}></input>
                    )
                }
            }
        )
    }
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
    week: generateControl("week")
}

export { standardControls }