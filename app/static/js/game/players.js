$(document).ready(function() {
	$('.dataTable').DataTable({
		order: [2, "desc"],
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
