game_id = $("input[name='game_id']").val()

$.getJSON("/api/game/" + game_id + "/score", function(game_data) {
	player_data = []

	for (var player in game_data["players"]) {
		game_data["players"][player]["test"] = "hi"
		game_data["players"][player]["bullet"] = "round"
		game_data["players"][player]["bulletBorderAlpha"] = 1
		game_data["players"][player]["bulletColor"] = "#FFFFFF"
		game_data["players"][player]["bulletSize"] = 5
		game_data["players"][player]["hideBulletsCount"] = 50
		game_data["players"][player]["lineThickness"] = 2
		game_data["players"][player]["useLineColorForBulletBorder"] = true
		game_data["players"][player]["balloonText"] = "[[title]]: [[value]]"
	}

	console.log(game_data["days"])
	console.log(game_data["players"])

	var chart = AmCharts.makeChart("game_index", {
		"type": "serial",
		"dataProvider": game_data["days"],
		"graphs": game_data["players"],
		"chartCursor": {
			"categoryBalloonEnabled": false,
			"zoomable": true
		},
		"categoryField": "day",
		"categoryAxis": {
			"gridPosition": "start",
			"gridAlpha": 0
		},
		"chartScrollbar": {
			"graph": "g1",
			"oppositeAxis":false,
			"offset":30,
			"scrollbarHeight": 80,
			"backgroundAlpha": 0,
			"selectedBackgroundAlpha": 0.1,
			"selectedBackgroundColor": "#888888",
			"graphFillAlpha": 0,
			"graphLineAlpha": 0.5,
			"selectedGraphFillAlpha": 0,
			"selectedGraphLineAlpha": 1,
			"autoGridCount":true,
			"color":"#AAAAAA"
		},

	});

	/*
	var chart = AmCharts.makeChart("chartdiv", {
		"type": "serial",
		"theme": "light",
		"marginRight": 40,
		"marginLeft": 40,
		"autoMarginOffset": 20,
		"mouseWheelZoomEnabled":true,
		"dataDateFormat": "YYYY-MM-DD",
		"balloon": {
			"borderThickness": 1,
			"shadowAlpha": 0
		},
		"graphs": [{
			"id": "g1",
			"balloon":{
			  "drop":true,
			  "adjustBorderColor":false,
			  "color":"#ffffff"
			},
			"bullet": "round",
			"bulletBorderAlpha": 1,
			"bulletColor": "#FFFFFF",
			"bulletSize": 5,
			"hideBulletsCount": 50,
			"lineThickness": 2,
			"title": "red line",
			"useLineColorForBulletBorder": true,
			"valueField": "value",
			"balloonText": "<span style='font-size:18px;'>[[value]]</span>"
		}],
		"chartScrollbar": {
			"graph": "g1",
			"oppositeAxis":false,
			"offset":30,
			"scrollbarHeight": 80,
			"backgroundAlpha": 0,
			"selectedBackgroundAlpha": 0.1,
			"selectedBackgroundColor": "#888888",
			"graphFillAlpha": 0,
			"graphLineAlpha": 0.5,
			"selectedGraphFillAlpha": 0,
			"selectedGraphLineAlpha": 1,
			"autoGridCount":true,
			"color":"#AAAAAA"
		},
		"chartCursor": {
			"pan": true,
			"valueLineEnabled": true,
			"valueLineBalloonEnabled": true,
			"cursorAlpha":1,
			"cursorColor":"#258cbb",
			"limitToGraph":"g1",
			"valueLineAlpha":0.2,
			"valueZoomable":true
		},
		"valueScrollbar":{
		  "oppositeAxis":false,
		  "offset":50,
		  "scrollbarHeight":10
		},
		"categoryField": "date",
		"categoryAxis": {
			"parseDates": true,
			"dashLength": 1,
			"minorGridEnabled": true
		},
		"export": {
			"enabled": true
		},
		"dataProvider": game_data
	});

	chart.addListener("rendered", zoomChart);

	zoomChart();

	function zoomChart() {
		chart.zoomToIndexes(chart.dataProvider.length - 40, chart.dataProvider.length - 1);
	}
	*/
});
