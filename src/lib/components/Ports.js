import { Colors, Controls } from 'flume'

const intPort = {
    type: "int",
    name: "int",
    label: "int",
    color: Colors.green,
    controls: [
        Controls.number({ name: "int", label: "int" })
    ]
}

const floatPort = {
    type: "float",
    name: "float",
    label: "float",
    color: Colors.blue,
    acceptTypes: ["float", "int"],
    controls: [
        Controls.number({ name: "float", label: "float" })
    ]
}

const strPort = {
    type: "str",
    name: "str",
    label: "str",
    color: Colors.yellow,
    controls: [
        Controls.text({ name: "str", label: "str" })
    ]
}

const generatePort = (itype) => {
    return {
        type: itype,
        name: itype,
        label: itype,
        color: Colors.orange,
        controls: [
            Controls.custom(
                {
                    name: itype,
                    label: itype,
                    render: (data, onChange, context, redraw, portProps, inputData) => {
                        return (
                            <input type={itype} className="TextInput_input__1QHwS" onChange={e => (onChange(e.target.value))}></input>
                        )
                    }
                }
            )
        ]
    }
}


const boolPort = {
    type: "bool",
    name: "bool",
    label: "bool",
    color: Colors.red,
    controls: [
        Controls.checkbox({ name: "bool", label: "bool" })
    ]
}

const flumePorts = [
    intPort, floatPort, strPort, boolPort
]

const portTypes = ["color", "date", "time", "month", "week"];

const genericInputPorts = portTypes.map(itype => {
    return generatePort(itype)
})

const standardPorts = flumePorts.concat(genericInputPorts);

export { standardPorts }