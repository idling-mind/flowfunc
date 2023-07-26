window.dash_clientside = Object.assign({}, window.dash_clientside, {
    flowfunc: {
        onLoad: function(x) {
            console.log(x);
            x.addNodeType({
                type: "string",
                label: "Text",
                description: "Outputs a string of text",
                inputs: ports => x => {
                    console.log(x);
                }
            })
        }
    }
});