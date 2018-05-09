// Call the dataTables jQuery plugin
$(document).ready(function() {
	$('.dataTable').DataTable({
		responsive: {
			details: {
				type: 'column',
				target: 'tr td:not(:first-child)'
			}
		},
		pageLength: 25,
		width: "100%",
	});
});
