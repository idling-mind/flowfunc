window.dash_clientside = Object.assign({}, window.dash_clientside, {
    flowfunc: {
        dynamic_ports: function (ports, inputData, connections, context) {
            // Example from flume.dev
            const template = (inputData && inputData.template && inputData.template.in_string) || "";
            const re = /\{(.*?)\}/g;
            let res, ids = []
            while ((res = re.exec(template)) !== null) {
                if (!ids.includes(res[1])) ids.push(res[1]);
            }
            return [
                ports.str({ name: "template", label: "Template", hidePort: true }),
                ...ids.map(id => ports.str({ name: id, label: id }))
            ];
        },
        increasing_ports: function (ports, inputData, connections, context) {
            const arr = [];
            connection_count = Object.keys(connections.inputs).length;
            for (let i = 0; i <= connection_count; i++) {
                arr.push(ports.str({ name: `port${i}`, label: `String ${i}` }));
            }
            return arr
        },
        custom_control: function (data, onChange) {
            return (
                window.dash_bootstrap_components.Button({
                    children: data,
                    onClick: (e) => {
                        e.target.textContent = String(Number(e.target.textContent)+1);
                        onChange(e.target.textContent);
                    }
                })
            )
        },
        upload_control: function(data, onChange) {
            var i = {type:"btn", index: crypto.randomUUID()};
            var button = React.createElement(
                window.dash_bootstrap_components.Button,
                {}, "Upload"
            );
            var comp = React.createElement(window.dash_core_components.Upload, {
                id: JSON.stringify(i),
                setProps: (props) => {
                    onChange(props);
                    return props
                }
            }, data?.filename ? data.filename : button);
            return comp
        }
    }
});