$.getJSON("/api/game/2190957/score", function(game_data) {
	player_data = []
	for (var item in game_data[0]) {
		if (item != "day") {
			player_data.push(item)
		}
    }

	new Morris.Line({
		// ID of the element in which to draw the chart.
		element: "game_index",
		// Chart data records -- each entry in this array corresponds to a point on
		// the chart.
		data: game_data,
		// The name of the data record attribute that contains x-values.
		xkey: "day",
		// A list of names of data record attributes that contain y-values.
		// ykeys: player_data,
		ykeys: player_data,
		// Labels for the ykeys -- will be displayed when you hover over the
		// chart.
		// labels: player_data,
		labels: player_data,
	});
});
