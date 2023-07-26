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
        }
    }
});