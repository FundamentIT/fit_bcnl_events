let spans = document.querySelectorAll('.bcnl_word span');
let spans_small = document.querySelectorAll('.bcnl_word_small span');

$.each(spans, function(idx, span) {
    setTimeout(function() {
		span.classList.add('active');
		spans_small[idx].classList.add('active');
	}, 750 * (idx+1));
});

/*
$.each(spans_small, function(idx, span) {
    setTimeout(function() {
		span.classList.add('active');
	}, 750 * (idx+1));
});
*/

/*function setRepeatSpansActive(span, idx) {
    span.classList.add('active');
    //setTimeout(() => {
    //	setRepeatSpansActive(span,idx);
    //}, 7500)
}
spans.forEach((span, idx) = > {
    span.addEventListener('click', (e) = > {
        e.target.classList.add('active');
    });
    span.addEventListener('animationend', (e) = > {
        e.target.classList.remove('active');
    });

    // Initial animation
    setTimeout(() = > {
        setRepeatSpansActive(span, idx);
        span.style.opacity = '1';
    },
    750 * (idx + 1))
});

spans_small.forEach((span, idx) = > {
    span.addEventListener('click', (e) = > {
        e.target.classList.add('active');
    });
    span.addEventListener('animationend', (e) = > {
        e.target.classList.remove('active');
    });

    // Initial animation
    setTimeout(() = > {
        setRepeatSpansActive(span, idx);
        span.style.opacity = '1';
    },
    750 * (idx + 1))
});*/