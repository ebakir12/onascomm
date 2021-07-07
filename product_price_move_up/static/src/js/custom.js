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
	
	let prod = document.getElementsByName("product_id");
	if(prod){
		let targetC = prod[0];
		let prices = document.getElementsByName("product_variant_price");
		if(prices && targetC){
			let callbackC = function(mutations){
				for(i = 0; i < prices.length; i++){
					if("product-" + targetC.value == prices[i].id){
					    prices[i].classList.remove('hidden');
					}
					else{
					    prices[i].classList.add('hidden');	
					}	
				}
			};
	
			//Create Observer
			let observerC = new MutationObserver(callbackC);
	
			//Set config settings
			let configC = { attributes: true, childList: true, subtree: true, characterData: true };
	
			//Start Observing
			observerC.observe(targetC, configC);
		}
	}	
});
