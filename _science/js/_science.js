$(document).ready(function(){
	var newTimelikeHeight = 0.625*$(".timelikeContainer").width();
	$(".timelikeContainer").height(newTimelikeHeight);
	
	$(window).resize(function(){
		newTimelikeHeight = 0.625*$('.timelikeContainer').width();
		$(".timelikeContainer").height(newTimelikeHeight);
		
	});
	var newHeroUnitHeight;
	var newGlobalMainContentHeight;
	if($(window).width() < 768){
		newGlobalMainContentHeight = 3*0.5625*$(".heroUnit").width();
	}
	else{
		newGlobalMainContentHeight = 0.5625*$(".heroUnit").width();
	}
	newHeroUnitHeight = 0.5625*$(".heroUnit").width();
	$(".heroUnit").height(newHeroUnitHeight);
	$(".globalMainContent").height(newGlobalMainContentHeight);
	$(window).resize(function(){
		newHeroUnitHeight = 0.5625*$(".heroUnit").width();
		$(".heroUnit").height(newHeroUnitHeight);
		if($(window).width() < 768){
			newGlobalMainContentHeight = 3*0.5625*$(".heroUnit").width();
		}
		else{
			newGlobalMainContentHeight = 0.5625*$(".heroUnit").width();
		}
		$(".globalMainContent").height(newGlobalMainContentHeight);
	});
});