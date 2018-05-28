function map(data) {

        function tooltipHtml(n, count) {    /* function to create html content string in tooltip div. */
            return "<h4>" + n + "</h4><table>" +
                "<tr><td>Cases</td><td>" + (count) + "</td></tr></table>";
        }

        zika_data = [];

        data.forEach(function (d) {
            //console.log(d);
            zika_data.push({"state": d.state, "count": +d.count});

        })
        //console.log(zika_data);

        var sampleData = [];
        /* Sample random data. This is for a range of values */
        start = d3.max([1, d3.min(zika_data, function (d) {
            return d.count
        })])
        end = 1 + d3.max(zika_data, function (d) {
            console.log(d);
            return d.count
        });

        const logScale = d3.scaleLog()
            .domain([start, end])
        /* definelog scale start var has to =1 not 0 */
        const colorScaleLog = d3.scaleSequential(
            (d) => {
                return d3.interpolateReds(logScale(d))
            }
        )

        zika_data.forEach(function (d) {
            //console.log("d:", d);
            uStatePaths.forEach(function (s) {
                //console.log("s:", s);
                if (d.state == s.n) {
                    d.n = s.n;
                    d.d = s.d;
                    d.id = s.id;
                }
            })

            //console.log(zika_data)
            count = +d.count;


            sampleData.push({
                n: d.n,
                state: d.state,
                count: count,
                path: d.d,
                color: colorScaleLog(count),
                color2: d3.interpolate("#000000", "#ffffff")(Math.round(count) / 100)
            });
        });
        //console.log("sampleData:", sampleData);
        /* draw states on id #statesvg */
        uStates.draw("#statesvg", sampleData, tooltipHtml);

    d3.select(self.frameElement).style("height", "600px");

}