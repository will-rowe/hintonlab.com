var slideout=new Slideout({'panel':document.getElementById('main'),'menu':document.getElementById('navbar-main'),'padding':256,'tolerance':70,'side':'right'});slideout.close();document.querySelector('.toggle-button').addEventListener('click',function(){slideout.toggle();});document.querySelector('.toggle-button-alt').addEventListener('click',function(){slideout.toggle();});$(window).load(function(){$('#profileModal').modal('show');});$(document).ready(function(){$('.carousel').carousel({interval:6000})});$(document).on('click','.navbar-collapse.in',function(e){if($(e.target).is('a')&&$(e.target).attr('class')!='dropdown-toggle'){$(this).collapse('hide');}});$(function(){var pageName=document.getElementById('_pageName');if(pageName!=null){pageName=pageName.innerHTML;}
else{pageName='';}
if(pageName.length>0){$("li[data-link-name='"+pageName+"']").addClass('active');}});!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+"://platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");$(window).scroll(function(){var topWindow=$(window).scrollTop();var topWindow=topWindow*1.5;var windowHeight=$(window).height();var position=topWindow/windowHeight;position=1-position;$('.arrow-wrap').css('opacity',position);});