let firstColIndex = 0;
let secondColIndex = 0;
let configs = {};
let isLoading = false;

function enterLoadingState() {
  // block input and put up loading screen
  isLoading = true;
}

function exitLoadingState() {
  // remove loading screen and return control
  isLoading = false;
}

function getConfigs(callback)
{
  // ajax check if password necessary
  // if yes prompt password
  // ajax request json
}

function buildFromConfigs() {
  // delete all blocks not in our initial state
  // wipe listeners, then set listeners on initial stuff
  // loop through configs, adding components
  // and setting listeners
}

function saveConfigs(callback) {

}

function firstColumnSelect(index) {
  // if button already selected do nothing
  // otherwise deselect selected and select this one
  // hide other sources and show the set for this one
  // hide other workspaces and show top for this one
  // aka secondColumnSelect(0)
  if(index != firstColIndex) {
    // Deselect other accounts, select other (style)
    $accountBtns = $(".account-list .account-btn")
    $accountBtns.removeClass("selected")
    $accountBtns[index].addClass("selected")

    // Hide unrelated sources, show related set
    $sourceSets = $(".source-list > div")
    $sourceSets.hide()
    $sourceSets[index].show()

    firstColIndex = index

    secondColumnSelect(0, true)
  }
}

function secondColumnSelect(index, force = false) {
  // if button already selected do nothing
  // otherwise deselect selected and select this one
  // hide other workspaces and show the one for this one
  console.log("2nd col: " + index)
  if(force || index != secondColIndex) {
    // Deselect any other sources, select the one (style)
    sourceBtns = sourceSets[firstColIndex].find(".source-btn")
    $(sourceBtns).removeClass("selected")
    $(sourceBtns[index]).addClass("selected")

    // Hide unrelated workspaces, show the one
    workSets = $(".workspace > div")
    workSets.children().hide()
    $(workSets[index]).children()[index].show()

    secondColIndex = index
  }
}

function setupInitialListeners() {
  $("#settings-btn").click(function() {
    firstColumnSelect(0)
  })
  let sourceBtns = $(".source-list button")
  for(var index in sourceBtns) {
    $(sourceBtns[index]).click(function() {
      secondColumnSelect(index)
    })
  }
}

function addAccount() {
  // append new account stub to configs
  // and rebuild

}

function addSource() {
  // append new source to current
  // rebuild
}

$(document).ready(function(){
  // TODO lock up and get actual configs

  setupInitialListeners()

});
