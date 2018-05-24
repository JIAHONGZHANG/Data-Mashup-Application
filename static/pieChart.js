function pieChart(data) {
    // var data = [1, 1, 2, 3, 33, 8, 13, 21];

    var width = 600,
        height = 600,
        oRadius = 250; //var holding value for the outer radius of the arc
    var iRadius = 0; //var holding the value for the inner radius of the arc
    var cRadius = 3; //var holding the value for the corner radius of the arc

    var myArcMaker = d3.arc().outerRadius(oRadius).innerRadius(iRadius).cornerRadius(cRadius); //var that returns the values needed to create the arcs of the pie chart
    // Feel free to change or delete any of the code you see in this editor!


    function arcTween(a) { //<-- a is the datum bound to each arc
        var startAngle = a.startAngle; //<-- keep reference to start angle
        var i = d3.interpolate(a.startAngle, a.endAngle); //<-- interpolate start to end
        return function (t) {
            return myArcMaker({ //<-- return arc at each iteration from start to interpolate end
                startAngle: startAngle,
                endAngle: i(t)
            });
        };
    }

    var pie = d3.pie()
        .padAngle(.02);
    var color = d3.scaleOrdinal(d3.schemeCategory10);

    var svg = d3.select("#main").select('.container').append("svg")
        .attr("width", width)
        .attr("height", height)
        .attr('style', 'margin-left: 280px;')
        .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    var formatter = d3.format(".2f");
    var tip = d3.tip().offset(function() {
            return [this.getBBox().height / 2, 5]
        }).attr('class', 'd3-tip').html(function (d) {
        return d.value + ': ' + formatter(((d.endAngle-d.startAngle)/6.283185307179584)*100) + '%';
    });

	svg.call(tip);

    let paths = svg.selectAll("path")
        .data(pie(data.map(function (d) {
            return d.count;
        })));

    console.log(paths);
    paths.enter()
        .append("path")
        .style("fill", function (d, i) {
            return color(i);
        })
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide)
        .transition().duration(750).attrTween("d", arcTween); // redraw the arcs
}