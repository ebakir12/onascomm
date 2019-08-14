//Import the MutationObserver for each browser
var MutationObserver = window.MutationObserver || window.WebKitMutationObserver || window.MozMutationObserver;
$(document).ready(function () {
	let webLoc = window.location.pathname;
	if('/' === webLoc){
		sessionStorage['is_business'] = true;
	}else if('/personal-homepage' === webLoc){
		sessionStorage['is_business'] = false;
	}
	
    //$('#business-btn a').removeClass('on');
    //$('#personal-btn a').removeClass('on');
	
    //let isBusiness = sessionStorage['is_business'];
	
    /*if (!isBusiness) {
        $('#personal-btn a').addClass('on');
        $('#business-btn a').removeClass('on');
    }
    else {
        $('#business-btn a').addClass('on');
        $('#personal-btn a').removeClass('on');
    }*/
	
	let pp = document.getElementById("productPrice");
	if(pp){
		let target = pp.children[0].children[1];
		let upperPP = document.getElementById("upperProductPrice");
		if(upperPP){
			pp.style = "display:none;";
			upperPP.classList = pp.classList;
			upperPP.innerHTML = pp.innerHTML;
	
			let callback = function(mutations){
				let upperPP = document.getElementById("upperProductPrice");
				let pp = document.getElementById("productPrice");
				upperPP.innerHTML = pp.innerHTML;
			};
	
			//Create Observer
			let observer = new MutationObserver(callback);
	
			//Set config settings
			let config = { attributes: true, childList: true, subtree: true, characterData: true };
	
			//Start Observing
			observer.observe(target, config);
		}
	}	
});
