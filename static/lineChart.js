function lineChart(data) {
    	data.forEach(function(d){
            d.Date = new Date(d.Date)
		    d.Count = +d.Count;
	    });

        d3.select('#main').select('.container')
            .append('svg')
            .attr('id', 'chart')
            .attr('width', 960)
            .attr('height', 500);

        var svg = d3.select("svg"),
            margin = {top: 60, right: 50, bottom: 50, left: 90},
            width = +svg.attr("width") - margin.left - margin.right,
            height = +svg.attr("height") - margin.top - margin.bottom,
            g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var parseTime = d3.timeParse("%Y-%m-%d");

        var x = d3.scaleTime()
            .rangeRound([0, width]);


        var y = d3.scaleLinear()
            .rangeRound([height, 0]);

        var line = d3.line()
            .x(function(d) { return x(d.Date); })
            .y(function(d) { return y(d.Count); });

          data.Date = parseTime(data.Date);

          x.domain(d3.extent(data, function(d) { return d.Date; }));
          y.domain(d3.extent(data, function(d) { return d.Count; }));

          g.append("g")
              .attr("transform", "translate(0," + height + ")")
              .call(d3.axisBottom(x))
              .select(".domain");



          g.append("g")
              .call(d3.axisLeft(y))
              .append("text")
              .attr("fill", "#000")
              .attr("transform", "rotate(-90)")
              .attr("y", 8)
              .attr("dy", "0.71em")
              .attr("text-anchor", "end")
              .text("Amount in " + $('#form-state-input').val());

         g.append("text")
            .call(d3.axisBottom(x))
            //.append("text")
            .attr("class", "label")
            .attr("fill", "#000")
            .attr("x", width/2)
            .attr("dx", "0.71em")
            .attr("y", height+margin.bottom*0.69)
            .attr("text-anchor", "end")
            .text ("Date");


           g.append("path")
              .datum(data)
              .attr("fill", "none")
              .attr("stroke", "grey")
              .attr("stroke-linejoin", "round")
              .attr("stroke-linecap", "round")
              .attr("stroke-width", 1.5)
              .attr("d", line);

}