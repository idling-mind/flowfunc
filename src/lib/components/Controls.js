import { Colors, Controls } from 'flume'

const generateControl = (itype) => {
    return Controls.custom(
        {
            name: itype,
            label: itype,
            render: (data, onChange, context, redraw, portProps, inputData) => {
                return (
                    <input
                        type={itype}
                        className="TextInput_input__1QHwS"
                        onChange={e => (onChange(e.target.value))}
                        value={data}>
                    </input>
                )
            }
        }
    )
}

const flumeControls = {
    int: Controls.number(
        {
            name: "int",
            label: "int"
        }
    ),
    float: Controls.number(
        {
            name: "float",
            label: "float",
        }
    ),
    str: Controls.text(
        {
            name: "str",
            label: "str",
        }
    ),
    bool: Controls.checkbox(
        {
            name: "bool",
            label: "bool",
        }
    )
}

const controlTypes = ["color", "date", "time", "month", "week"];

const genericInputControls = controlTypes.map(itype => {
    return generateControl(itype)
})

const standardControls = flumeControls.concat(genericInputControls);

export { standardControls }