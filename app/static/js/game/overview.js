game_id = $("input[name='game_id']").val()

$(document).ready(function(e) {
	get_data("players")
})

$(".show_players").on("click", function() {
	get_data("players")
	$(".switch_player").text("Players")
});

$(".show_active").on("click", function() {
	get_data("active")
	$(".switch_player").text("Active")
});

$(".show_everyone").on("click", function() {
	get_data("everyone")
	$(".switch_player").text("Everyone")
});

function get_data(type)
{
	$(".show_button").text(type.charAt(0).toUpperCase() + type.slice(1))

	url = "/api/game/" + game_id + "/score/" + type
	$.ajax({
		dataType: "json",
		url: url,
	})
		.done(function(data) {
			player_data = get_player_data(data)
			days_data = data["days"]

			make_chart(player_data, days_data)
		})
}

function get_player_data(data)
{
	player_data = data["players"]

	for (var player in player_data) {
		player_data[player]["bullet"] = "round"
		player_data[player]["bulletBorderAlpha"] = 1
		player_data[player]["bulletColor"] = "#FFFFFF"
		player_data[player]["bulletSize"] = 8
		player_data[player]["hideBulletsCount"] = 50
		player_data[player]["labelText"] = "[[title]]"
		player_data[player]["labelFunction"] = labelFunction
		player_data[player]["labelPosition"] = "top"
		player_data[player]["lineThickness"] = 2
		player_data[player]["useLineColorForBulletBorder"] = true
		player_data[player]["balloonText"] = "[[title]]: [[value]]"
	}

	return player_data
}

function make_chart(player_data, days_data)
{
	var chart = AmCharts.makeChart("game_index", {
		"type": "serial",
		"dataProvider": days_data,
		"graphs": player_data,
		"categoryField": "day",
		"categoryAxis": {
			"gridPosition": "start",
		},
		"valueAxes": [{
			"minimum": 20
		}],
		"chartScrollbar": {
			"oppositeAxis":false,
			"offset":30,
		},
		"valueScrollbar":{
			"oppositeAxis":false,
			"offset":50,
			"scrollbarHeight":10
		},
		"theme": "light",
		"addClassNames": true,
	})
}

function labelFunction(item, label)
{
	if (item.index === item.graph.chart.dataProvider.length - 1)
		return label
	else
		return ""
}

$(document).ready(function() {
	$('.dataTable.countrys').DataTable({
		order: [4, 'desc'],
		responsive: {
			details: {
				type: 'column',
				target: 'tr td:not(:first-child)'
			}
		},
		paging: false,
		columnDefs: [
			{
				targets: [5],
				orderData:[6],
			},
			{
				targets: [6],
				visible: false,
				searchable: false,
				type: 'non-empty-string',
			},
		],
	});

	jQuery.extend( jQuery.fn.dataTableExt.oSort, {
	    'non-empty-string-asc': function (str1, str2) {
	        if(str1 == '')
	            return 1;
	        if(str2 == '')
	            return -1;
	        return ((str1 < str2) ? -1 : ((str1 > str2) ? 1 : 0));
	    },

	    'non-empty-string-desc': function (str1, str2) {
	        if(str1 == '')
	            return 1;
	        if(str2 == '')
	            return -1;
	        return ((str1 < str2) ? 1 : ((str1 > str2) ? -1 : 0));
	    }
	});
});
