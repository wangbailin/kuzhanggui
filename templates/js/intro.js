$(function() {
	$(".case img ").popover({
		html: true,
		placement: "right",
		// trigger: "click",
        trigger: "hover",
		content: "<div style='width: 140px; height: 140px'><img src='/static/img/case_lmjy_hover.jpg'/></div>"
		//content: "<img src='/static/img/case_lmjy_hover.jpg' style='width: 140px; height: 140px'/>"
    });
});

