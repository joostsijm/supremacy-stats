game_id = $("input[name='game_id']").val()

$.getJSON("/api/game/" + game_id + "/score", function(game_data) {
	player_data = []
	for (var item in game_data[0]) {
		if (item != "day") {
			player_data.push(item)
		}
    }

	new Morris.Line({
		element: "game_index",
		data: game_data,
		xkey: "day",
		ykeys: player_data,
		labels: player_data,
		parseTime: false,
		postUnits: " points",
		goals: [1000],
	});
});
