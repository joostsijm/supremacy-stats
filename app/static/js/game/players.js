$(document).ready(function() {
	$('.dataTable').DataTable({
		order: [2, 'desc'],
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
