function barChart(data) {
	data.forEach(function(d){
		d.profit = +d.profit;
		d.revenue = +d.revenue;
	});

    var margin = {top: 10, bottom: 100, left: 100, right: 10};
    var width = 1160 - margin.left - margin.right,
	    height = 600 - margin.top - margin.bottom;
    var t = d3.transition().duration(500);

	var svg = d3.select('#main').select('.container').append('svg');
	svg.attr('width', width + margin.left + margin.right)
	    .attr('height', height + margin.top + margin.bottom)
	    .attr('style', 'border:1px solid black;');

	var g = svg.append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

	var tip = d3.tip().attr('class', 'd3-tip').offset([-12, 0]).html(function (d) {
        return d.month + ': $' + d.revenue;
    });

	g.call(tip);

    var x = d3.scaleBand()
        .domain(data.map(function (d) {
            return d.month;
        }))
        .range([0,width])
        .padding(0.3);

    var y = d3.scaleLinear()
        .domain([0, d3.max(data, function (d) {
            return d.revenue*1.05;
        })])
        .range([height, 0]);

    var xAxisCall = d3.axisBottom(x);
    g.append('g')
        .attr('class', 'x-axis')
        .attr('transform', 'translate(0,' + height + ')')
        .call(xAxisCall);

    var yAxisCall = d3.axisLeft(y);
    g.append('g')
        .attr('class', 'y-axis')
        .call(yAxisCall);

    var xLabel = g.append('text')
        .attr('class', 'xLabel')
        .attr('x', width/2)
        .attr('y', height + 60)
        .attr('font-size', '20px')
        .text('Month');

	var yLabel = g.append('text')
		.attr('class', 'y axis-label')
		.attr('x', -(height/2))
		.attr('y', -60)
		.attr('font-size', '20px')
		.attr('text-anchor', 'middle')
		.attr('transform', 'rotate(-90)')
		.text('Revnue');


    console.log(data);
    var rects = g.selectAll('rect')
        .data(data);

    rects.enter()
        .append('rect')
        .attr('x', function (d) {
            return x(d.month);
        })
        .attr('y', y(0))
        .attr('width', x.bandwidth())
        .attr('fill', 'gray')
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide)
        .transition(t)
        .attr('y', function (d) {
            return y(d.revenue);
        })
        .attr('height', function (d) {
            return height - y(d.revenue);
        })
        .attr('fill', 'gray');

}

function barChart_2(data) {

    var margin = {top: 10, bottom: 100, left: 100, right: 10};
    var width = 1160 - margin.left - margin.right,
	    height = 600 - margin.top - margin.bottom;
    var t = d3.transition().duration(500);

	var svg = d3.select('#bar').append('svg');
	svg.attr('width', width + margin.left + margin.right)
	    .attr('height', height + margin.top + margin.bottom);

	var g = svg.append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

	var tip = d3.tip().attr('class', 'd3-tip').offset([-12, 0]).html(function (d) {
        return d.state + ': ' + d.count;
    });

	g.call(tip);

    var x = d3.scaleBand()
        .domain(data.map(function (d) {
            return d.state;
        }))
        .range([0,width])
        .padding(0.3);

    var y = d3.scaleLinear()
        .domain([0, d3.max(data, function (d) {
            return d.count*1.05;
        })])
        .range([height, 0]);

    var xAxisCall = d3.axisBottom(x);
    g.append('g')
        .attr('class', 'x-axis')
        .attr('transform', 'translate(0,' + height + ')')
        .call(xAxisCall)
        .selectAll('text')
        .attr('y', '10')
        .attr('x', '-5')
        .attr('text-anchor', 'end')
        .attr('transform', 'rotate(-40)');

    var yAxisCall = d3.axisLeft(y);
    g.append('g')
        .attr('class', 'y-axis')
        .call(yAxisCall);

    // var xLabel = g.append('text')
    //     .attr('class', 'xLabel')
    //     .attr('x', width/2)
    //     .attr('y', height + 60)
    //     .attr('font-size', '20px')
    //     .text('Count');

	var yLabel = g.append('text')
		.attr('class', 'y axis-label')
		.attr('x', -(height/2))
		.attr('y', -60)
		.attr('font-size', '20px')
		.attr('text-anchor', 'middle')
		.attr('transform', 'rotate(-90)')
		.text('count');


    var rects = g.selectAll('rect')
        .data(data);

    rects.enter()
        .append('rect')
        .attr('x', function (d) {
            return x(d.state);
        })
        .attr('y', y(0))
        .attr('width', x.bandwidth())
        .attr('fill', 'gray')
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide)
        .transition(t)
        .attr('y', function (d) {
            return y(d.count);
        })
        .attr('height', function (d) {
            return height - y(d.count);
        })
        .attr('fill', 'gray');

}



