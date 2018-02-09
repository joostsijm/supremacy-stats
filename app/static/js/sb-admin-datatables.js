// Call the dataTables jQuery plugin
$(document).ready(function() {
	$('.dataTable').DataTable();

	$('table.countrys').DataTable({
		"order": [[ 2, "desc" ]]
	});
});
