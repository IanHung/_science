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
		newGlobalMainContentHeight = Math.max(3*0.5625*$(".heroUnit").width(), 0.5625*$(".heroUnit").width()+800, 1039);
		newHeroUnitHeight = Math.max(0.5625*$(".heroUnit").width(), 239);
	}
	else{
		newGlobalMainContentHeight = 0.5625*$(".heroUnit").width();
		newHeroUnitHeight = 0.5625*$(".heroUnit").width();
	}
	$(".heroUnit").height(newHeroUnitHeight);
	$(".globalMainContent").height(newGlobalMainContentHeight);
	$(window).resize(function(){
		
		
		if($(window).width() < 768){
			newGlobalMainContentHeight = Math.max(3*0.5625*$(".heroUnit").width(), 0.5625*$(".heroUnit").width()+800, 1039);
			newHeroUnitHeight = Math.max(0.5625*$(".heroUnit").width(), 239);
		}
		else{
			newGlobalMainContentHeight = 0.5625*$(".heroUnit").width();
			newHeroUnitHeight = 0.5625*$(".heroUnit").width();
		}
		$(".heroUnit").height(newHeroUnitHeight);
		$(".globalMainContent").height(newGlobalMainContentHeight);
		
	});
});