$(document).ready(function() {
	$('.dataTable').DataTable({
		responsive: {
			details: {
				type: 'column',
				target: 'tr td:not(:first-child)'
			}
		},
		paging: false,
		width: "100%",
	});
});
