function helperMenuFunction(targetDiv){
		$(".publishFormHelperMenu").on("click","#textContentButton", function(){
			
			targetDiv.before('<div class="emptyContentContainer">Click to Add Content Here</div><div class="contentInputContainer"><div class="textSubmission"><div class="textInputContainer"><textarea class="form=control" rows="10" ></textarea></div><div class="hiddenfield"><input type="hidden" class="contentType" value="textContent"></div></div><div class="edittingButtonsContainer"><button type="button" class="btn btn-move-up"><i class="icon-arrow-up"></i></button><button type="button" class="btn btn-move-down"><i class="icon-arrow-down"></i></button><button type="button" class="btn btn-delete"><i class="icon-remove"></i></button></div></div>');
			var thisSectionPosition = targetDiv.parents(".sectionSubmission").find(".class_sectionPosition").val();
			var thisSectionContentCounter = 0;
			targetDiv.parents(".sectionSubmission").find(".contentInputContainer").each(function(){
				nameSetterFunction(this, thisSectionPosition, thisSectionContentCounter);
				thisSectionContentCounter++;
			});
			//positionNewSectionButton();
			//positionPublishFormHelperMenu();
			//$(".publishFormHelperMenu").hide();
			targetDiv.parents(".sectionSubmission").find(".class_numberOfContentSections").val(thisSectionContentCounter);	
		});
		$(".publishFormHelperMenu").on("click","#imageContentButton", function(){
			
			targetDiv.before('<div class="emptyContentContainer">Click to Add Content Here</div><div class="contentInputContainer"><div class="imageSubmission"><div class="imageInputContainer"><div class="variableHeader"><h3>Insert Image</h3><div class="selectSource"><button type="button" class="btn btn-upload">From File</button><button type="button" class="btn btn-link">From a URL</button>{% if labbook_imageNode_list %}<button type="button" class="btn btn-labbook">From Labbook</button>{% endif %}</div></div><div class="localSourceSubmission"><div class="localSourceInputContainer"><input class="imageInputLocalSource inputLocalSource" id="id_imageFormLocalSource" type="file" /></div></div><div class="linkSourceSubmission"><div class="linkSourceInputContainer"><input id="id_imageFormLinkSource" class="imageInputLinkSource inputLinkSource" placeholder="Enter URL of image." type="text" /></div></div>{% if labbook_imageNode_list %}<div class="labbookSourceSubmission"><div class="labbookSourceInputContainer"><select class="imageInputLabbookSource inputLabbookSource" id="id_imageFormLabbookSource" ><option value="" selected="selected">---------</option>{% for imageNode in labbook_imageNode_list %}<option value="{{ imageNode.object_id }}">{{ imageNode.title }}</option>{% endfor %}</select></div></div>{% endif %}</div><div class="hiddenfield"><input type="hidden" class="contentType" value="imageContent"></div></div><div class="edittingButtonsContainer"><button type="button" class="btn btn-move-up"><i class="icon-arrow-up"></i></button><button type="button" class="btn btn-move-down"><i class="icon-arrow-down"></i></button><button type="button" class="btn btn-delete"><i class="icon-remove"></i></button></div></div>');
			var $newContentInputContainer = targetDiv.prev();
			$newContentInputContainer.find(".localSourceSubmission").hide();
			$newContentInputContainer.find(".linkSourceSubmission").hide();
			$newContentInputContainer.find(".labbookSourceSubmission").hide();
			var thisSectionPosition = targetDiv.parents(".sectionSubmission").find(".class_sectionPosition").val();
			var thisSectionContentCounter = 0;
			targetDiv.parents(".sectionSubmission").find(".contentInputContainer").each(function(){
				nameSetterFunction(this, thisSectionPosition, thisSectionContentCounter);
				thisSectionContentCounter++;
			});
			//positionNewSectionButton();
			//positionPublishFormHelperMenu();
			//$(".publishFormHelperMenu").hide();
			targetDiv.parents(".sectionSubmission").find(".class_numberOfContentSections").val(thisSectionContentCounter);
		});
		$(".publishFormHelperMenu").on("click","#videoContentButton", function(){
			
			targetDiv.before('<div class="emptyContentContainer">Click to Add Content Here</div><div class="contentInputContainer"><div class="timelikeSubmission"><div class="timelikeInputContainer"><div class="variableHeader"><h3>Submit video</h3><div class="selectSource"><button type="button" class="btn btn-upload">From File</button><button type="button" class="btn btn-link">From a URL</button>{% if labbook_timelikeNode_list %}<button type="button" class="btn btn-labbook">From Labbook</button>{% endif %}</div></div><div class="localSourceSubmission"><div class="localSourceInputContainer"><input class="timelikeInputLocalSource inputLocalSource" id="id_timelikeFormLocalSource" type="file" /></div></div><div class="linkSourceSubmission"><div class="linkSourceInputContainer"><input id="id_timelikeFormLinkSource" class="timelikeInputLinkSource inputLinkSource" placeholder="Enter URL of Video." type="text" /></div></div>{% if labbook_timelikeNode_list %}<div class="labbookSourceSubmission"><div class="labbookSourceInputContainer"><select class="timelikeInputLabbookSource inputLabbookSource" id="id_timelikeFormLabbookSource" ><option value="" selected="selected">---------</option>{% for timelikeNode in labbook_timelikeNode_list %}<option value="{{ timelikeNode.object_id }}">{{ timelikeNode.title }}</option>{% endfor %}</select></div></div>{% endif %}</div><div class="hiddenfield"><input type="hidden" class="contentType" value="timelikeContent"></div></div><div class="edittingButtonsContainer"><button type="button" class="btn btn-move-up"><i class="icon-arrow-up"></i></button><button type="button" class="btn btn-move-down"><i class="icon-arrow-down"></i></button><button type="button" class="btn btn-delete"><i class="icon-remove"></i></button></div></div>');
			var $newContentInputContainer = targetDiv.prev();
			$newContentInputContainer.find(".localSourceSubmission").hide();
			$newContentInputContainer.find(".linkSourceSubmission").hide();
			$newContentInputContainer.find(".labbookSourceSubmission").hide();
			var thisSectionPosition = targetDiv.parents(".sectionSubmission").find(".class_sectionPosition").val();
			var thisSectionContentCounter = 0;
			targetDiv.parents(".sectionSubmission").find(".contentInputContainer").each(function(){
				nameSetterFunction(this, thisSectionPosition, thisSectionContentCounter);
				thisSectionContentCounter++;
			});
			//positionNewSectionButton();
			//positionPublishFormHelperMenu();
			//$(".publishFormHelperMenu").hide();
			targetDiv.parents(".sectionSubmission").find(".class_numberOfContentSections").val(thisSectionContentCounter);
		});
		$(".publishFormHelperMenu").on("click","#dataContentButton", function(){
			
			targetDiv.before('<div class="emptyContentContainer">Click to Add Content Here</div><div class="contentInputContainer"><div class="dataSubmission"><div class="dataInputContainer"><div class="variableHeader"><h3>Submit Data</h3>{% if labbook_dataNode_list %}<div class="selectSource"><button type="button" class="btn btn-manual-data">Manually</button><button type="button" class="btn btn-labbook-data">From Labbook</button></div>{% else %}<p>No Data Sets Found!</p>{% endif %}</div><div class="manualSubmission"><div class="manualInputContainer"></div></div>{% if labbook_dataNode_list %}<div class="labbookSourceSubmission"><div class="labbookSourceInputContainer"><select class="dataInputLabbookSource inputLabbookSource"><option value="" selected="selected">---------</option>{% for dataNode in labbook_dataNode_list %}<option value="{{ dataNode.object_id }}">{{ dataNode.title }}</option>{% endfor %}</select></div></div>{% endif %}</div><div class="hiddenfield"><input type="hidden" class="contentType" value="dataContent"></div></div><div class="edittingButtonsContainer"><button type="button" class="btn btn-move-up"><i class="icon-arrow-up"></i></button><button type="button" class="btn btn-move-down"><i class="icon-arrow-down"></i></button><button type="button" class="btn btn-delete"><i class="icon-remove"></i></button></div></div>');
			var $newContentInputContainer = targetDiv.prev();
			{% if labbook_dataNode_list %}
			$newContentInputContainer.find(".manualSubmission").hide();
			$newContentInputContainer.find(".labbookSourceSubmission").hide();
			{% endif %}
			var thisSectionPosition = targetDiv.parents(".sectionSubmission").find(".class_sectionPosition").val();
			var thisSectionContentCounter = 0;
			targetDiv.parents(".sectionSubmission").find(".contentInputContainer").each(function(){
				nameSetterFunction(this, thisSectionPosition, thisSectionContentCounter);
				thisSectionContentCounter++;
			});
			//positionNewSectionButton();
			//positionPublishFormHelperMenu();
			//$(".publishFormHelperMenu").hide();
			targetDiv.parents(".sectionSubmission").find(".class_numberOfContentSections").val(thisSectionContentCounter);
		});
	}