diameter = 750,
radius = diameter / 2,
innerRadius = radius - 120;

cluster = d3.layout.cluster()
	.size([360, innerRadius])
	.sort(null)
	.value(function(d) { return d.size; });

bundle = d3.layout.bundle();

line = d3.svg.line.radial()
	.interpolate("bundle")
	.tension(0.75)
	.radius(function(d) { return d.y; })
	.angle(function(d) { return d.x / 180 * Math.PI; });
	
svg = d3.select("#graph").append("svg")
	.attr("width", diameter)
	.attr("height", diameter)
	.append("g")
	.attr("transform", "translate(" + radius + "," + radius + ")");

share_map = svg.append("g").selectAll(".share_map");
war = svg.append("g").selectAll(".war");
right_of_way = svg.append("g").selectAll(".right_of_way");
node = svg.append("g").selectAll(".node");

d3.json("types.json", function(error, classes) {
	nodes = cluster.nodes(packageHierarchy(classes));
	share_maps = typeShare_map(nodes);
	right_of_ways = typeRight_of_way(nodes);
	wars = typeWar(nodes);

	share_map = share_map
		.data(bundle(share_maps))
		.enter().append("path")
		.each(function(d) { d.source = d[0], d.target = d[d.length - 1]; })
		.attr("class", "share_map")
		.attr("d", line);

	war = war
		.data(bundle(wars))
		.enter().append("path")
		.each(function(d) { d.source = d[0], d.target = d[d.length - 1]; })
		.attr("class", "war")
		.attr("d", line);

	right_of_way = right_of_way
		.data(bundle(right_of_ways))
		.enter().append("path")
		.each(function(d) { d.source = d[0], d.target = d[d.length - 1]; })
		.attr("class", "right_of_way")
		.attr("d", line)
		.attr("data-is-effective-against-self", function(d) { return (d[0] === d[d.length - 1]) });

	node = node
		.data(nodes.filter(function(n) { return !n.children; }))
		.enter().append("text")
		.attr("class", function(n) {
			return 'node ' + n.name.toLowerCase();
		})
		.attr("dx", function(d) { return d.x < 180 ? 8 : -8; })
		.attr("dy", ".31em")
		.attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + d.y + ")" + (d.x < 180 ? "" : "rotate(180)"); })
		.style("text-anchor", function(d) { return d.x < 180 ? "start" : "end"; })
		.text(function(d) { return d.key; })
		.on("mouseover", mouseovered)
		.on("mouseout", mouseouted);
});

function mouseovered(d) {
	node
		.each(function(n) { n.target = n.source = false; });

	share_map
		.classed("shares_maps_with", function(l) { if (l.source === d) return l.target.target = true; })
		.filter(function(l) { return l.source === d; })
		.each(function(d) { this.parentNode.appendChild(this); });

	war
		.classed("fights_against", function(l) { if (l.source === d) return l.target.target = true; })
		.filter(function(l) { return l.source === d })
		.each(function() { this.parentNode.appendChild(this); });

	right_of_way
		.classed("shares_ways_with", function(l) { if (l.source === d) { return l.target.target = true;} })
		.filter(function(l) { return l.source === d; })
		.each(function() { this.parentNode.appendChild(this); });


	node
		.classed("node--target", function(n) { return n.target; })
		.style('fill', function(l) { 
			if(d.share_maps.indexOf(l.name) != -1) {
				return 'rgba(250, 0, 235, 1)';
			}
			if(d.wars.indexOf(l.name) != -1) {
				return 'rgba(0, 193, 248, 1)';
			}
			if(d.right_of_ways.indexOf(l.name) != -1) {
				return 'rgba(255, 204, 0, 1)';
			}
			return null;
		 });
}

function mouseouted(d) {
	share_map
		.classed("shares_maps_with", false);

	war
		.classed("fights_against", false);

	right_of_way
		.classed("shares_ways_with", false);

	node
		.classed("node--target", false)
		.style('fill', null);

}

d3.select(self.frameElement).style("height", diameter + "px");

// Lazily construct the package hierarchy from class names.
function packageHierarchy(classes) {
	var map = {};

	function find(name, data) {
		var node = map[name], i;
		if (!node) {
			node = map[name] = data || {name: name, children: []};
			if (name.length) {
				node.parent = find(name.substring(0, i = name.lastIndexOf(".")));
				node.parent.children.push(node);
				node.key = name.substring(i + 1);
			}
		}
		return node;
	}
	classes.forEach(function(d) {
		find(d.name, d);
	});

	return map[""];
}

//Make the share_map links
function typeShare_map(nodes) {
	map = {},
	share_maps = [];

	nodes.forEach(function(d) {
		map[d.name] = d;
	});

	nodes.forEach(function(d) {
		if (d.share_maps) d.share_maps.forEach(function(i) {
			share_maps.push({source: map[d.name], target: map[i]});
		});
	});

	return share_maps;
}
//Make the share_map links
function typeWar(nodes) {
	map = {},
	wars = [];

	nodes.forEach(function(d) {
		map[d.name] = d;
	});

	nodes.forEach(function(d) {
		if (d.wars) d.wars.forEach(function(i) {
			wars.push({source: map[d.name], target: map[i]});
		});
	});

	return wars;
}
function typeRight_of_way(nodes) {
	map = {},
	right_of_ways = [];

	nodes.forEach(function(d) {
		map[d.name] = d;
	});

	nodes.forEach(function(d) {
		if (d.right_of_ways) d.right_of_ways.forEach(function(i) {
			right_of_ways.push({source: map[d.name], target: map[i]});
		});
	});

	return right_of_ways;
}
