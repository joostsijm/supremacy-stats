game_id = $("input[name='game_id']").val();

$(document).ready(function(e) {
	width = window.innerWidth / 2
	height = window.innerHeight

	nodes = {};
	api_url = "/api/game/" + game_id + "/force_relations";

	d3.json(api_url, function(error, directed) {
		if (error) throw error;

		directed.forEach(function(link) {
			link.source = nodes[link.source] || (nodes[link.source] = { name : link.source });
			link.target = nodes[link.target] || (nodes[link.target] = { name : link.target });
		});

		force = d3.layout.force()
			.nodes(d3.values(nodes))
			.links(directed)
			.linkDistance(150)
			.charge(-280)
			.on("tick", tick)
			.start();

		svg = d3.select("#force_relations").append("svg")
			.attr('viewBox','0 0 ' + width + ' ' + height)
			.append("g")
			.attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

		// Per-type markers, as they don't inherit styles.
		svg.append("defs").selectAll("marker")
			.data(["war", "right-of-way", "share-map", "share-info"])
			.enter().append("marker")
			.attr("id", function(d) { return d; })
			.attr("viewBox", "0 -5 10 10")
			.attr("refX", 15)
			.attr("refY", -1.5)
			.attr("markerWidth", 6)
			.attr("markerHeight", 6)
			.attr("orient", "auto")
			.append("path")
			.attr("d", "M0,-5L10,0L0,5");

		path = svg.append("g").selectAll("path")
			.data(force.links())
			.enter().append("path")
			.attr("class", function(d) { return "link " + d.type; })
			.attr("marker-end", function(d) { return "url(#" + d.type + ")"; });

		circle = svg.append("g").selectAll("circle")
			.data(force.nodes())
			.enter().append("circle")
			.attr("r", 6)
			.attr("class", function(n) {
				return 'force_node ' + n.name.replace(/\s+/g, '_').toLowerCase();
			})
			.call(force.drag);

		text = svg.append("g").selectAll("text")
			.data(force.nodes())
			.enter().append("text")
			.attr("x", 8)
			.attr("y", ".31em")
			.text(function(d) { return d.name; });

		// Use elliptical arc path segments to doubly-encode directionality.
		function tick() {
			path.attr("d", linkArc);
			circle.attr("transform", transform);
			text.attr("transform", transform);
		}
	});

	function linkArc(d) {
		dx = d.target.x - d.source.x,
			dy = d.target.y - d.source.y,
			dr = Math.sqrt(dx * dx + dy * dy);
		return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
	}

	function transform(d) {
		return "translate(" + d.x + "," + d.y + ")";
	}
});

$(window).bind("load", function() {
	diameter = $("#edge_relations").innerWidth();
	radius = diameter / 2;
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

	svg = d3.select("#edge_relations").append("svg")
		.attr("width", diameter)
		.attr("height", diameter)
		.append("g")
		.attr("transform", "translate(" + radius + "," + radius + ")");

	share_map = svg.append("g").selectAll(".share_map");
	war = svg.append("g").selectAll(".war");
	right_of_way = svg.append("g").selectAll(".right_of_way");
	share_info = svg.append("g").selectAll(".share_info");
	node = svg.append("g").selectAll(".node");

	api_url = "/api/game/" + game_id + "/edge_relations";

	d3.json(api_url, function(error, classes) {
		nodes = cluster.nodes(packageHierarchy(classes));
		share_maps = typeShare_map(nodes);
		right_of_ways = typeRight_of_way(nodes);
		wars = typeWar(nodes);
		share_infos = typeShare_info(nodes);

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

		share_info = share_info
			.data(bundle(share_infos))
			.enter().append("path")
			.each(function(d) { d.source = d[0], d.target = d[d.length - 1]; })
			.attr("class", "share_info")
			.attr("d", line);

		node = node
			.data(nodes.filter(function(n) { return !n.children; }))
			.enter().append("text")
			.attr("class", function(n) {
				return 'node ' + n.name.replace(/\s+/g, '_').toLowerCase();
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

		share_info
			.classed("shares_info_with", function(l) { if (l.source === d) { return l.target.target = true;} })
			.filter(function(l) { return l.source === d; })
			.each(function() { this.parentNode.appendChild(this); });

		node
			.classed("node--target", function(n) { return n.target; })
			.style('fill', function(l) {
				if(d.share_maps.indexOf(l.name) != -1) {
					return '#28a745';
				}
				if(d.wars.indexOf(l.name) != -1) {
					return '#dc3545';
				}
				if(d.right_of_ways.indexOf(l.name) != -1) {
					return '#adff2f';
				}
				return null;
			 });

		name = $(this).text().replace(/\s+/g, '_').toLowerCase();
		selector = ".force_node." + name;
		$(selector).addClass("active");
		$(selector)
			.addClass("active")
			.attr("r", "10");
	}

	function mouseouted(d) {
		share_map
			.classed("shares_maps_with", false);

		war
			.classed("fights_against", false);

		right_of_way
			.classed("shares_ways_with", false);

		share_info
			.classed("shares_info_with", false);

		node
			.classed("node--target", false)
			.style('fill', null);

		name = $(this).text().replace(/\s+/g, '_').toLowerCase();
		selector = ".force_node." + name;
		$(selector)
			.removeClass("active")
			.attr("r", "6");
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

	// Make the war links
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

	// Make the right of way links
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

	// Make the share info links
	function typeShare_info(nodes) {
		map = {},
		share_infos = [];

		nodes.forEach(function(d) {
			map[d.name] = d;
		});

		nodes.forEach(function(d) {
			if (d.share_infos) d.share_infos.forEach(function(i) {
				share_infos.push({source: map[d.name], target: map[i]});
			});
		});

		return share_infos;
	}
});
