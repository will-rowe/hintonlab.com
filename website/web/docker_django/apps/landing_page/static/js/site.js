/**********************************************/
/* Launch modal on page load if no profile exists */
$(window).load(function(){
    $('#profileModal').modal('show');
});


/**********************************************/
/* Carousel Auto-Cycle */
$(document).ready(function() {
  $('.carousel').carousel({
    interval: 6000
  })
});


/**********************************************/
/* Hide navbar on link click (fix for viewing members side bar on mobiles) */
$(document).on('click','.navbar-collapse.in',function(e) {
  if( $(e.target).is('a') && $(e.target).attr('class') != 'dropdown-toggle' ) {
    $(this).collapse('hide');
  }
});


/**********************************************/
/* JS for highlighting active pages */
$(function() {
  var pageName = document.getElementById('_pageName');
  if (pageName != null) { pageName = pageName.innerHTML; }
  else { pageName = ''; }
  if (pageName.length > 0) {
      $("li[data-link-name='" + pageName + "']").addClass('active');
  }
});


/**********************************************/
/* Twitter Feed */
!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+"://platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");


/**********************************************/
/* Arrow for page scrolling (from codepen) */
//this is where we apply opacity to the arrow
$(window).scroll( function(){
      //get scroll position
  var topWindow = $(window).scrollTop();
      //multipl by 1.5 so the arrow will become transparent half-way up the page
  var topWindow = topWindow * 1.5;
      //get height of window
  var windowHeight = $(window).height();
      //set position as percentage of how far the user has scrolled
  var position = topWindow / windowHeight;
      //invert the percentage
  position = 1 - position;
      //define arrow opacity as based on how far up the page the user has scrolled
      //no scrolling = 1, half-way up the page = 0
  $('.arrow-wrap').css('opacity', position);
});
