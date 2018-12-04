game_id = $("input[name='game_id']").val()

$(document).ready(function(e) {
	get_data("resources")
})

function get_data(type)
{
	url = "/api/game/" + game_id + "/market"
	$.ajax({
		dataType: "json",
		url: url,
	})
		.done(function(data) {
			market_data = format_data(data)
			days_data = data["days"]

			make_chart(market_data, days_data)
		})
}

function format_data(data)
{
	resource_data = data["resource"]

	for (var resource in resource_data) {
		resource_data[resource]["bullet"] = "round"
		resource_data[resource]["bulletBorderAlpha"] = 1
		resource_data[resource]["bulletColor"] = "#FFFFFF"
		resource_data[resource]["bulletSize"] = 8
		resource_data[resource]["hideBulletsCount"] = 50
		resource_data[resource]["labelText"] = "[[title]]"
		resource_data[resource]["labelFunction"] = labelFunction
		resource_data[resource]["labelPosition"] = "top"
		resource_data[resource]["lineThickness"] = 2
		resource_data[resource]["useLineColorForBulletBorder"] = true
		resource_data[resource]["balloonText"] = "[[title]]: [[value]]"
	}

	return resource_data
}

function make_chart(resource_data, days_data)
{
	var chart = AmCharts.makeChart("game_index", {
		"type": "serial",
		"dataProvider": days_data,
		"graphs": resource_data,
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

