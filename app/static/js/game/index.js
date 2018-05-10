$(document).ready(function() {
	$(".dataTable").DataTable({
		order: [0, "desc"],
			responsive: {
				details: {
					type: 'column',
					target: 'tr td:not(:first-child)'
				}
			},
		pageLength: 25,
	});
});
