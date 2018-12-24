let spans = document.querySelectorAll('.bcnl_word span');
let spans_small = document.querySelectorAll('.bcnl_word_small span');

$.each(spans, function(idx, span) {
    setTimeout(function() {
		span.classList.add('active');
	}, 750 * (idx+1));
    setTimeout(function() {
		spans_small[0].classList.add('active');
	}, 750 * (5));

});