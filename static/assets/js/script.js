/*
Author       : Dreamguys
Template Name: Doccure - Bootstrap Template
Version      : 1.3
*/

(function ($) {
	"use strict";

	// Stick Sidebar

	if ($(window).width() > 767) {
		if ($('.theiaStickySidebar').length > 0) {
			$('.theiaStickySidebar').theiaStickySidebar({
				// Settings
				additionalMarginTop: 30
			});
		}
	}

	// Sidebar

	if ($(window).width() <= 991) {
		var Sidemenu = function () {
			this.$menuItem = $('.main-nav a');
		};

		function init() {
			var $this = Sidemenu;
			$('.main-nav a').on('click', function (e) {
				if ($(this).parent().hasClass('has-submenu')) {
					e.preventDefault();
				}
				if (!$(this).hasClass('submenu')) {
					$('ul', $(this).parents('ul:first')).slideUp(350);
					$('a', $(this).parents('ul:first')).removeClass('submenu');
					$(this).next('ul').slideDown(350);
					$(this).addClass('submenu');
				} else if ($(this).hasClass('submenu')) {
					$(this).removeClass('submenu');
					$(this).next('ul').slideUp(350);
				}
			});
		}

		// Sidebar Initiate
		init();
	}
	// JQuery counterUp

	if ($('.counter').length > 0) {
		$('.counter').counterUp({
			delay: 10,
			time: 2000
		});
		$('.counter').addClass('animated fadeInDownBig');
	}

	// Textarea Text Count

	var maxLength = 100;
	$('#review_desc').on('keyup change', function () {
		var length = $(this).val().length;
		length = maxLength - length;
		$('#chars').text(length);
	});

	// Select 2

	if ($('.select').length > 0) {
		$('.select').select2({
			minimumResultsForSearch: -1,
			width: '100%'
		});
	}

	// consultation

	$(".consultation-types").on('click', function () {
		$(".consultation-types").removeClass('active');
		$(this).addClass('active');
	});

	// Date Time Picker

	if ($('.datetimepicker').length > 0) {
		$('.datetimepicker').datetimepicker({
			format: 'DD/MM/YYYY',
			icons: {
				up: "fas fa-chevron-up",
				down: "fas fa-chevron-down",
				next: 'fas fa-chevron-right',
				previous: 'fas fa-chevron-left'
			}
		});
	}

	if($('.timepicker1').length > 0 ){
        $('.timepicker1').datetimepicker({
            format: 'HH:mm A',
            icons: {
                up: "fas fa-angle-up",
                down: "fas fa-angle-down",
                next: 'fas fa-angle-right',
                previous: 'fas fa-angle-left'
            }
        });
    }

	// AOS Animation

	if ($('.main-wrapper .aos').length > 0) {
		AOS.init({
			duration: 1200,
			once: true,
		});
	}

	// Floating Label

	if ($('.floating').length > 0) {
		$('.floating').on('focus blur', function (e) {
			$(this).parents('.form-focus').toggleClass('focused', (e.type === 'focus' || this.value.length > 0));
		}).trigger('blur');
	}

	// Mobile menu sidebar overlay

	$('body').append('<div class="sidebar-overlay"></div>');
	$(document).on('click', '#mobile_btn', function () {
		$('main-wrapper').toggleClass('slide-nav');
		$('.sidebar-overlay').toggleClass('opened');
		$('html').toggleClass('menu-opened');
		return false;
	});

	$(document).on('click', '.sidebar-overlay', function () {
		$('html').removeClass('menu-opened');
		$(this).removeClass('opened');
		$('main-wrapper').removeClass('slide-nav');
	});

	$(document).on('click', '#menu_close', function () {
		$('html').removeClass('menu-opened');
		$('.sidebar-overlay').removeClass('opened');
		$('main-wrapper').removeClass('slide-nav');
	});

	// Tooltip

	if ($('[data-bs-toggle="tooltip"]').length > 0) {
		var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
		var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
			return new bootstrap.Tooltip(tooltipTriggerEl)
		})
	}

	// Add More Hours

	$(".hours-info").on('click', '.trash', function () {
		$(this).closest('.hours-cont').remove();
		return false;
	});

	$(".add-hours").on('click', function () {

		var hourscontent = '<div class="row form-row hours-cont">' +
			'<div class="col-12 col-md-10">' +
			'<div class="row form-row">' +
			'<div class="col-12 col-md-6">' +
			'<div class="form-group">' +
			'<label>Start Time</label>' +
			'<select class="form-select form-control">' +
			'<option>-</option>' +
			'<option>12.00 am</option>' +
			'<option>12.30 am</option>' +
			'<option>1.00 am</option>' +
			'<option>1.30 am</option>' +
			'</select>' +
			'</div>' +
			'</div>' +
			'<div class="col-12 col-md-6">' +
			'<div class="form-group">' +
			'<label>End Time</label>' +
			'<select class="form-select form-control">' +
			'<option>-</option>' +
			'<option>12.00 am</option>' +
			'<option>12.30 am</option>' +
			'<option>1.00 am</option>' +
			'<option>1.30 am</option>' +
			'</select>' +
			'</div>' +
			'</div>' +
			'</div>' +
			'</div>' +
			'<div class="col-12 col-md-2"><label class="d-md-block d-sm-none d-none">&nbsp;</label><a href="#" class="btn btn-danger trash"><i class="far fa-trash-alt"></i></a></div>' +
			'</div>';

		$(".hours-info").append(hourscontent);
		return false;
	});

	// Content div min height set

	function resizeInnerDiv() {
		var height = $(window).height();
		var header_height = $(".header").height();
		var footer_height = $(".footer").height();
		var setheight = height - header_height;
		var trueheight = setheight - footer_height;
		$(".content").css("min-height", trueheight);
	}

	if ($('.content').length > 0) {
		resizeInnerDiv();
	}

	$(window).resize(function () {
		if ($('.content').length > 0) {
			resizeInnerDiv();
		}
	});

	// Favourites
	$('.fav-icon').on('click', function () {
		$(this).toggleClass('selected');
		//$(this).children().toggleClass("feather-heart fa-solid fa-heart");
	});

	if($('.header-eleven').length > 0) {
		$(document).ready(function(){
		  $(window).scroll(function(){
			var scroll = $(window).scrollTop();
			  if (scroll > 95) {
				$(".header-eleven").css("background" , "#1e5d92");
			  }
	
			  else{
				  $(".header-eleven").css("background" , "transparent");  	
			  }
		  })
		})
	}
	
	//owl carousel
		
	if($('.owl-carousel.special').length > 0) {
		$('.owl-carousel.special').owlCarousel({
			loop:true,
			margin:15,
			dots: true,
			nav:true,
			smartSpeed: 2000,
			navText: [ '<i class="fas fa-chevron-left"></i>', '<i class="fas fa-chevron-right"></i>' ], 
			responsive:{
				0:{
					items:1
				},
				500:{
					items:2
				},
				768:{
					items:3
				},
				1000:{
					items:4
				},
				1300:{
					items:4
				}
			}
		})	
	}
	
	//Eye Clicnic carousel
	
	if($('.owl-carousel.eye-clinic').length > 0) {
		$('.owl-carousel.eye-clinic').owlCarousel({
			loop:true,
			margin:15,
			dots: true,
			nav:true,
			smartSpeed: 2000,
			navText: [ '<i class="fas fa-chevron-left"></i>', '<i class="fas fa-chevron-right"></i>' ], 
			responsive:{
				0:{
					items:1
				},
				500:{
					items:1
				},
				768:{
					items:2
				},
				992:{
					items:3
				},
				1200:{
					items:4
				}
			}
		})	
	}
	
	//Eye Blog carousel
	
	if($('.owl-carousel.eye-blogslider').length > 0) {
		$('.owl-carousel.eye-blogslider').owlCarousel({
			loop:true,
			margin:15,
			dots: true,
			nav:true,
			smartSpeed: 2000,
			navText: [ '<i class="fas fa-chevron-left"></i>', '<i class="fas fa-chevron-right"></i>' ], 
			responsive:{
				0:{
					items:1
				},
				500:{
					items:1
				},
				768:{
					items:3
				},
				1000:{
					items:4
				},
				1300:{
					items:4
				}
			}
		})	
	}
	
	//Eye Blog carousel
	
	if($('.owl-carousel.eye-blogslider').length > 0) {
		$('.owl-carousel.eye-blogslider').owlCarousel({
			loop:true,
			margin:15,
			dots: true,
			nav:true,
			smartSpeed: 2000,
			navText: [ '<i class="fas fa-chevron-left"></i>', '<i class="fas fa-chevron-right"></i>' ], 
			responsive:{
				0:{
					items:1
				},
				500:{
					items:1
				},
				768:{
					items:3
				},
				1000:{
					items:4
				},
				1300:{
					items:4
				}
			}
		})	
	}
	
	//Eye Testimonial carousel
	
	if($('.owl-carousel.eye-testislider').length > 0) {
		$('.owl-carousel.eye-testislider').owlCarousel({
			loop:true,
			margin:15,
			dots: false,
			nav:true,
			smartSpeed: 2000,
			navContainer: '.slide-11',
			navText: [ '<i class="fa-solid fa-arrow-left"></i>', '<i class="fa-solid fa-arrow-right"></i>' ], 
			responsive:{
				0:{
					items:1
				},
				1300:{
					items:1
				}
			}
		})	
	}

	// Specialities Slider

	if ($('.owl-carousel.specialities-slider-one').length > 0) {
		$('.owl-carousel.specialities-slider-one').owlCarousel({
			loop: true,
			margin: 24,
			dots: false,
			nav: true,
			smartSpeed: 2000,
			navContainer: '.slide-nav-1',
			navText: ['<i class="fas fa-chevron-left custom-arrow"></i>', '<i class="fas fa-chevron-right custom-arrow"></i>'],
			responsive: {
				0: {
					items: 1
				},
				500: {
					items: 1
				},
				768: {
					items: 2
				},
				1000: {
					items: 3
				},
				1300: {
					items: 6
				}
			}
		})
	}

	// Doctors Slider

	if ($('.owl-carousel.doctor-slider-one').length > 0) {
		$('.owl-carousel.doctor-slider-one').owlCarousel({
			loop: true,
			margin: 24,
			dots: false,
			nav: true,
			smartSpeed: 2000,
			navContainer: '.slide-nav-2',
			navText: ['<i class="fas fa-chevron-left custom-arrow"></i>', '<i class="fas fa-chevron-right custom-arrow"></i>'],
			responsive: {
				0: {
					items: 1
				},
				500: {
					items: 1
				},
				768: {
					items: 2
				},
				1000: {
					items: 3
				},
				1300: {
					items: 4
				}
			}
		})
	}

	// Team Slider
	if ($('.owl-carousel.team-fourteen-slider').length > 0) {
		$('.owl-carousel.team-fourteen-slider').owlCarousel({
			loop: true,
			margin: 24,
			dots: false,
			nav: true,
			smartSpeed: 2000,
			navContainer: '.slide-nav-14',
			navText: ['<i class="fa-solid fa-caret-left "></i>', '<i class="fa-solid fa-caret-right"></i>'],
			responsive: {
				0: {
					items: 1
				},
				500: {
					items: 1
				},
				768: {
					items: 2
				},
				1000: {
					items: 2
				},
				1300: {
					items: 2
				}
			}
		})
	}

	// Feature Slider
	if ($('.owl-carousel.features-slider-sixteen').length > 0) {
		$('.owl-carousel.features-slider-sixteen').owlCarousel({
			loop: true,
			margin: 24,
			dots: true,
			nav: false,
			smartSpeed: 2000,
			responsive: {
				0: {
					items: 1
				},
				500: {
					items: 1
				},
				768: {
					items: 2
				},
				1000: {
					items: 3
				},
				1300: {
					items: 3
				}
			}
		})
	}

	// Blog Slider

	if ($('.owl-carousel.blog-slider-fourteen').length > 0) {
		$('.owl-carousel.blog-slider-fourteen').owlCarousel({
			loop: true,
			margin: 24,
			dots: false,
			nav: true,
			smartSpeed: 2000,
			navContainer: '.slide-nav-15',
			navText: ['<i class="fa-solid fa-caret-left "></i>', '<i class="fa-solid fa-caret-right"></i>'],
			responsive: {
				0: {
					items: 1
				},
				500: {
					items: 1
				},
				575: {
					items: 1
				},
				768: {
					items: 2
				},
				1000: {
					items: 3
				},
				1300: {
					items: 3
				}
			}
		})
	}
	if ($('.owl-carousel.blog-slider-twelve').length > 0) {
		$('.owl-carousel.blog-slider-twelve').owlCarousel({
			loop: true,
			margin: 24,
			dots: false,
			nav: true,
			smartSpeed: 2000,
			navContainer: '.slide-nav-16',
			navText: ['<i class="fa-solid fa-caret-left "></i>', '<i class="fa-solid fa-caret-right"></i>'],
			responsive: {
				0: {
					items: 1
				},
				500: {
					items: 1
				},
				575: {
					items: 2
				},
				768: {
					items: 2
				},
				1000: {
					items: 4
				},
				1300: {
					items: 4
				}
			}
		})
	}

	// Our Doctor
	if ($('.owl-carousel.our-slider-thirteen').length > 0) {
		$('.owl-carousel.our-slider-thirteen').owlCarousel({
			loop: true,
			margin: 64,
			dots: true,
			nav: false,
			smartSpeed: 2000,
			responsive: {
				0: {
					items: 1
				},
				500: {
					items: 1
				},
				575: {
					items: 2
				},
				768: {
					items: 2
				},
				1000: {
					items: 3
				},
				1300: {
					items: 3
				}
			}
		})
	}

	// Doctor Slider

	if ($('.owl-carousel.doctor-slider-fifteen').length > 0) {
		$('.owl-carousel.doctor-slider-fifteen').owlCarousel({
			loop: true,
			margin: 24,
			dots: false,
			nav: true,
			smartSpeed: 2000,
			navText: ['<i class="fas fa-chevron-left"></i>', '<i class="fas fa-chevron-right"></i>'],
			responsive: {
				0: {
					items: 1
				},
				500: {
					items: 1
				},
				575: {
					items: 2
				},
				768: {
					items: 2
				},
				1000: {
					items: 3
				},
				1300: {
					items: 3
				}
			}
		})
	}

	if ($('.owl-carousel.client-says-thirteen').length > 0) {
		$('.owl-carousel.client-says-thirteen').owlCarousel({
			loop: true,
			margin: 24,
			dots: true,
			nav: false,
			smartSpeed: 2000,
			responsive: {
				0: {
					items: 1
				},
				500: {
					items: 1
				},
				575: {
					items: 1
				},
				768: {
					items: 1
				},
				1000: {
					items: 1
				},
				1300: {
					items: 1
				}
			}
		})
	}

	// Doctor Slider

	if ($('.owl-carousel.pharmacy-slider-fifteen').length > 0) {
		$('.owl-carousel.pharmacy-slider-fifteen').owlCarousel({
			loop: true,
			margin: 24,
			dots: false,
			nav: true,
			smartSpeed: 2000,
			navText: ['<i class="fas fa-chevron-left"></i>', '<i class="fas fa-chevron-right"></i>'],
			responsive: {
				0: {
					items: 1
				},
				500: {
					items: 1
				},
				575: {
					items: 2
				},
				768: {
					items: 2
				},
				1000: {
					items: 3
				},
				1300: {
					items: 3
				}
			}
		})
	}

	//Eye Testimonial carousel

	if ($('.owl-carousel.eye-testislider').length > 0) {
		$('.owl-carousel.eye-testislider').owlCarousel({
			loop: true,
			margin: 15,
			dots: false,
			nav: true,
			smartSpeed: 2000,
			navContainer: '.slide-11',
			navText: ['<i class="fa-solid fa-arrow-left"></i>', '<i class="fa-solid fa-arrow-right"></i>'],
			responsive: {
				0: {
					items: 1
				},
				1300: {
					items: 1
				}
			}
		})
	}

	// Feedback Slider

	if ($('.owl-carousel.feedback-slider-fourteen').length > 0) {
		$('.owl-carousel.feedback-slider-fourteen').owlCarousel({
			loop: true,
			margin: 24,
			dots: false,
			nav: true,
			smartSpeed: 2000,
			navText: ['<i class="fa-solid fa-caret-left "></i>', '<i class="fa-solid fa-caret-right"></i>'],
			responsive: {
				0: {
					items: 1
				},
				500: {
					items: 1
				},
				768: {
					items: 1
				},
				1000: {
					items: 1
				},
				1300: {
					items: 1
				}
			}
		})
	}

	// Date Slider

	if ($('.date-slider').length > 0) {
		$('.date-slider').slick({
			dots: false,
			autoplay: false,
			infinite: true,
			variableWidth: false,
			slidesToShow: 7,
			slidesToScroll: 1,
			swipeToSlide: true,
			responsive: [
				{
					breakpoint: 1024,
					settings: {
						slidesToShow: 3,
						slidesToScroll: 1
					}
				},
				{
					breakpoint: 992,
					settings: {
						slidesToShow: 3,
						slidesToScroll: 1
					}
				},
				{
					breakpoint: 768,
					settings: {
						slidesToShow: 3,
						slidesToScroll: 1
					}
				},
				{
					breakpoint: 500,
					settings: {
						slidesToShow: 1,
						slidesToScroll: 1
					}
				}
			]
		});
	}

	// Testimonial Slider

	if ($('.testimonial-slider').length > 0) {
		$('.testimonial-slider').slick({
			dots: false,
			autoplay: false,
			infinite: true,
			speed: 2000,
			variableWidth: false,
			slidesToShow: 1,
			slidesToScroll: 1,
			swipeToSlide: true,
			responsive: [
				{
					breakpoint: 1024,
					settings: {
						slidesToShow: 1,
						slidesToScroll: 1
					}
				},
				{
					breakpoint: 992,
					settings: {
						slidesToShow: 1,
						slidesToScroll: 1
					}
				},
				{
					breakpoint: 768,
					settings: {
						slidesToShow: 1,
						slidesToScroll: 1
					}
				},
				{
					breakpoint: 500,
					settings: {
						slidesToShow: 1,
						slidesToScroll: 1
					}
				}
			]
		});
	}

	// Partners Slider

	if ($('.owl-carousel.partners-slider').length > 0) {
		$('.owl-carousel.partners-slider').owlCarousel({
			loop: true,
			margin: 24,
			nav: true,
			autoplay: true,
			smartSpeed: 2000,
			responsive: {
				0: {
					items: 1
				},

				550: {
					items: 2
				},
				700: {
					items: 4
				},
				1000: {
					items: 6
				}
			}
		})
	}

	// Doctors Slider

	if ($('.owl-carousel.doctor-slider-one').length > 0) {
		$('.owl-carousel.doctor-slider-one').owlCarousel({
			loop: true,
			margin: 24,
			dots: false,
			nav: true,
			smartSpeed: 2000,
			navContainer: '.slide-nav-2',
			navText: ['<i class="fas fa-chevron-left custom-arrow"></i>', '<i class="fas fa-chevron-right custom-arrow"></i>'],
			responsive: {
				0: {
					items: 1
				},
				500: {
					items: 1
				},
				768: {
					items: 2
				},
				1000: {
					items: 3
				},
				1300: {
					items: 4
				}
			}
		})
	}

	// Frequent Slider

	if ($('.owl-carousel.frequent-slider-fifteen').length > 0) {
		$('.owl-carousel.frequent-slider-fifteen').owlCarousel({
			loop: true,
			margin: 24,
			dots: true,
			nav: true,
			smartSpeed: 2000,
			navText: ['<i class="fas fa-chevron-left"></i>', '<i class="fas fa-chevron-right"></i>'],
			responsive: {
				0: {
					items: 1
				},
				500: {
					items: 1
				},
				768: {
					items: 2
				},
				1000: {
					items: 3
				},
				1300: {
					items: 3
				}
			}
		})
	}

	// Team Slider
	if ($('.owl-carousel.team-fourteen-slider').length > 0) {
		$('.owl-carousel.team-fourteen-slider').owlCarousel({
			loop: true,
			margin: 24,
			dots: false,
			nav: true,
			smartSpeed: 2000,
			navContainer: '.slide-nav-14',
			navText: ['<i class="fa-solid fa-caret-left "></i>', '<i class="fa-solid fa-caret-right"></i>'],
			responsive: {
				0: {
					items: 1
				},
				500: {
					items: 1
				},
				768: {
					items: 2
				},
				1000: {
					items: 2
				},
				1300: {
					items: 2
				}
			}
		})
	}

	// Blog Slider

	if ($('.owl-carousel.blog-slider-fourteen').length > 0) {
		$('.owl-carousel.blog-slider-fourteen').owlCarousel({
			loop: true,
			margin: 24,
			dots: false,
			nav: true,
			smartSpeed: 2000,
			navContainer: '.slide-nav-15',
			navText: ['<i class="fa-solid fa-caret-left "></i>', '<i class="fa-solid fa-caret-right"></i>'],
			responsive: {
				0: {
					items: 1
				},
				500: {
					items: 1
				},
				575: {
					items: 2
				},
				768: {
					items: 2
				},
				1000: {
					items: 3
				},
				1300: {
					items: 3
				}
			}
		})
	}

	// Doctor Slider

	if ($('.owl-carousel.doctor-slider-fifteen').length > 0) {
		$('.owl-carousel.doctor-slider-fifteen').owlCarousel({
			loop: true,
			margin: 24,
			dots: false,
			nav: true,
			smartSpeed: 2000,
			navText: ['<i class="fas fa-chevron-left"></i>', '<i class="fas fa-chevron-right"></i>'],
			responsive: {
				0: {
					items: 1
				},
				500: {
					items: 1
				},
				575: {
					items: 2
				},
				768: {
					items: 2
				},
				1000: {
					items: 3
				},
				1300: {
					items: 3
				}
			}
		})
	}

	// Pharmacy Slider

	if ($('.owl-carousel.pharmacy-slider-fifteen').length > 0) {
		$('.owl-carousel.pharmacy-slider-fifteen').owlCarousel({
			loop: true,
			margin: 10,
			dots: false,
			nav: true,
			smartSpeed: 2000,
			navText: ['<i class="fas fa-chevron-left"></i>', '<i class="fas fa-chevron-right"></i>'],
			responsive: {
				0: {
					items: 1
				},
				500: {
					items: 1
				},
				575: {
					items: 2
				},
				768: {
					items: 2
				},
				1000: {
					items: 3
				},
				1300: {
					items: 3
				}
			}
		})
	}

	// Discover Slider

	if ($('.owl-carousel.discover-slider').length > 0) {
		$('.owl-carousel.discover-slider').owlCarousel({
			loop: true,
			margin: 10,
			dots: true,
			nav: false,
			smartSpeed: 2000,
			responsive: {
				0: {
					items: 1
				},
				500: {
					items: 1
				},
				575: {
					items: 2
				},
				768: {
					items: 2
				},
				1000: {
					items: 3
				},
				1300: {
					items: 5
				}
			}
		})
	}

	// Treatment Slider

	if ($('.owl-carousel.treatment-sixteen-slider').length > 0) {
		$('.owl-carousel.treatment-sixteen-slider').owlCarousel({
			loop: true,
			margin: 10,
			dots: true,
			nav: false,
			smartSpeed: 2000,
			responsive: {
				0: {
					items: 1
				},
				500: {
					items: 1
				},
				575: {
					items: 2
				},
				768: {
					items: 2
				},
				1000: {
					items: 3
				},
				1300: {
					items: 4
				}
			}
		})
	}

	// Choose Slider
	$('.about-us-section-fifteen .vertical-slider').slick({
		dots: true,
		arrows: true,
        autoplay: false,
        centerMode: true,
        infinite: true,
        rows: 0,
        slidesToShow: 3,
        vertical: true,
        verticalSwiping: true
	});

	var defaults = {
		calendarWeeks: true,
		showClear: true,
		showClose: true,
		allowInputToggle: true,
		useCurrent: false,
		ignoreReadonly: true,
		minDate: new Date(),
		toolbarPlacement: 'top',
		locale: 'nl',
		icons: {
			time: 'fa fa-clock-o',
			date: 'fa fa-calendar',
			up: 'fa fa-angle-up',
			down: 'fa fa-angle-down',
			previous: 'fa fa-angle-left',
			next: 'fa fa-angle-right',
			today: 'fa fa-dot-circle-o',
			clear: 'fa fa-trash',
			close: 'fa fa-times'
		}
	};
	
	$(function() {
		var optionsDatetime = $.extend({}, defaults, {format:'DD-MM-YYYY HH:mm'});
		var optionsDate = $.extend({}, defaults, {format:'DD-MM-YYYY'});
		var optionsTime = $.extend({}, defaults, {format:'HH:mm'});
		
		$('.datepicker').datetimepicker(optionsDate);
		$('.timepicker').datetimepicker(optionsTime);
		$('.datetimepicker').datetimepicker(optionsDatetime);
	});


	//slider
	if ($(' #slide-experts').length > 0) {
	$('#slide-experts').owlCarousel({
		margin: 0,
		center: true,
		loop: true,
		nav: false,
		dots: false,
		responsive: {
			0: {
				items: 1
			},
			768: {
				items: 1,
				margin: 15,
			},
			1000: {
				items: 3,
			}
		}
	});
};



	// Feedback Slider

	if ($('.owl-carousel.feedback-slider-fourteen').length > 0) {
		$('.owl-carousel.feedback-slider-fourteen').owlCarousel({
			loop: true,
			margin: 24,
			dots: false,
			nav: true,
			smartSpeed: 2000,
			navText: ['<i class="fa-solid fa-caret-left "></i>', '<i class="fa-solid fa-caret-right"></i>'],
			responsive: {
				0: {
					items: 1
				},
				500: {
					items: 1
				},
				768: {
					items: 1
				},
				1000: {
					items: 1
				},
				1300: {
					items: 1
				}
			}
		})
	}

	// Date Slider

	if ($('.date-slider').length > 0) {
		$('.date-slider').slick({
			dots: false,
			autoplay: false,
			infinite: true,
			variableWidth: false,
			slidesToShow: 7,
			slidesToScroll: 1,
			swipeToSlide: true,
			responsive: [
				{
					breakpoint: 1024,
					settings: {
						slidesToShow: 3,
						slidesToScroll: 1
					}
				},
				{
					breakpoint: 992,
					settings: {
						slidesToShow: 3,
						slidesToScroll: 1
					}
				},
				{
					breakpoint: 768,
					settings: {
						slidesToShow: 3,
						slidesToScroll: 1
					}
				},
				{
					breakpoint: 500,
					settings: {
						slidesToShow: 1,
						slidesToScroll: 1
					}
				}
			]
		});
	}

	// Testimonial Slider

	if ($('.testimonial-slider').length > 0) {
		$('.testimonial-slider').slick({
			dots: false,
			autoplay: false,
			infinite: true,
			speed: 2000,
			variableWidth: false,
			slidesToShow: 1,
			slidesToScroll: 1,
			swipeToSlide: true,
			responsive: [
				{
					breakpoint: 1024,
					settings: {
						slidesToShow: 1,
						slidesToScroll: 1
					}
				},
				{
					breakpoint: 992,
					settings: {
						slidesToShow: 1,
						slidesToScroll: 1
					}
				},
				{
					breakpoint: 768,
					settings: {
						slidesToShow: 1,
						slidesToScroll: 1
					}
				},
				{
					breakpoint: 500,
					settings: {
						slidesToShow: 1,
						slidesToScroll: 1
					}
				}
			]
		});
	}

	// Partners Slider

	if ($('.owl-carousel.partners-slider').length > 0) {
		$('.owl-carousel.partners-slider').owlCarousel({
			loop: true,
			margin: 24,
			nav: true,
			autoplay: true,
			smartSpeed: 2000,
			responsive: {
				0: {
					items: 1
				},

				550: {
					items: 2
				},
				700: {
					items: 4
				},
				1000: {
					items: 6
				}
			}
		})
	}


	// Slick Slider

	if ($('.specialities-slider').length > 0) {
		$('.specialities-slider').slick({
			dots: true,
			autoplay: false,
			infinite: true,
			variableWidth: true,
			prevArrow: false,
			nextArrow: false
		});
	}

	if ($('.doctor-slider').length > 0) {
		$('.doctor-slider').slick({
			dots: false,
			autoplay: false,
			infinite: true,
			variableWidth: true,
		});
	}
	if ($('.features-slider').length > 0) {
		$('.features-slider').slick({
			dots: true,
			infinite: true,
			centerMode: true,
			slidesToShow: 3,
			speed: 500,
			variableWidth: true,
			arrows: false,
			autoplay: false,
			responsive: [{
				breakpoint: 992,
				settings: {
					slidesToShow: 1
				}

			}]
		});
	}

	// Load More Timings Open

	$(".time-slot-morning").slideUp();
	$(".load-more-morning").on("click", function () {
		$(this).toggleClass("show");
		$(".time-slot-morning").slideToggle();
	});

	$(".time-slot-afternoon").slideUp();
	$(".load-more-afternoon").on("click", function () {
		$(this).toggleClass("show");
		$(".time-slot-afternoon").slideToggle();
	});

	$(".time-slot-evening").slideUp();
	$(".load-more-evening").on("click", function () {
		$(this).toggleClass("show");
		$(".time-slot-evening").slideToggle();
	});


	// Slick Slider
	if ($('.features-slider1').length == 1) {
		$('.features-slider1').slick({
			dots: false,
			infinite: true,
			centerMode: false,
			slidesToShow: 1,
			speed: 500,
			variableWidth: true,
			arrows: true,
			autoplay: false,
			responsive: [{
				breakpoint: 992,
				settings: {
					slidesToShow: 1
				}

			}]
		});
	}
	if ($('.slider-1').length > 0) {
		$('.slider-1').slick();
	}

	//Home pharmacy slider
	if ($('.dot-slider').length > 0) {
		$('.dot-slider').slick({
			dots: true,
			autoplay: false,
			infinite: true,
			slidesToShow: 1,
			slidesToScroll: 1,
			arrows: false,
			responsive: [{
				breakpoint: 992,
				settings: {
					slidesToShow: 1
				}
			},
			{
				breakpoint: 800,
				settings: {
					slidesToShow: 1
				}
			},
			{
				breakpoint: 776,
				settings: {
					slidesToShow: 1
				}
			},
			{
				breakpoint: 567,
				settings: {
					slidesToShow: 1
				}
			}]
		});
	}

	//clinic slider
	if ($('.clinic-slider').length > 0) {
		$('.clinic-slider').slick({
			dots: false,
			autoplay: false,
			infinite: true,
			slidesToShow: 4,
			slidesToScroll: 1,
			rows: 2,
			responsive: [{
				breakpoint: 992,
				settings: {
					slidesToShow: 3
				}
			},
			{
				breakpoint: 800,
				settings: {
					slidesToShow: 3
				}
			},
			{
				breakpoint: 776,
				settings: {
					slidesToShow: 3
				}
			},
			{
				breakpoint: 567,
				settings: {
					slidesToShow: 1
				}
			}]
		});
	}

	//browse slider
	if ($('.browse-slider').length > 0) {
		$('.browse-slider').slick({
			dots: false,
			autoplay: false,
			infinite: true,
			slidesToShow: 4,
			slidesToScroll: 1,
			rows: 2,
			responsive: [{
				breakpoint: 992,
				settings: {
					slidesToShow: 3
				}
			},
			{
				breakpoint: 800,
				settings: {
					slidesToShow: 3
				}
			},
			{
				breakpoint: 776,
				settings: {
					slidesToShow: 3
				}
			},
			{
				breakpoint: 567,
				settings: {
					slidesToShow: 1
				}
			}]
		});
	}

	//book doctor slider
	if ($('.book-slider').length > 0) {
		$('.book-slider').slick({
			dots: false,
			autoplay: false,
			infinite: true,
			slidesToShow: 4,
			slidesToScroll: 1,
			responsive: [{
				breakpoint: 992,
				settings: {
					slidesToShow: 3
				}
			},
			{
				breakpoint: 800,
				settings: {
					slidesToShow: 3
				}
			},
			{
				breakpoint: 776,
				settings: {
					slidesToShow: 2
				}
			},
			{
				breakpoint: 567,
				settings: {
					slidesToShow: 1
				}
			}]
		});
	}

	//avalable features slider
	if ($('.aval-slider').length > 0) {
		$('.aval-slider').slick({
			dots: false,
			autoplay: false,
			infinite: true,
			slidesToShow: 3,
			slidesToScroll: 1,
			responsive: [{
				breakpoint: 992,
				settings: {
					slidesToShow: 2
				}
			},
			{
				breakpoint: 800,
				settings: {
					slidesToShow: 2
				}
			},
			{
				breakpoint: 776,
				settings: {
					slidesToShow: 2
				}
			},
			{
				breakpoint: 567,
				settings: {
					slidesToShow: 1
				}
			}]
		});
	}
	//Home pharmacy slider
	if ($('.pharmacy-home-slider .swiper-container').length > 0) {
		var swiper = new Swiper('.pharmacy-home-slider .swiper-container', {
			loop: true,
			speed: 1000,
			pagination: {
				el: '.pharmacy-home-slider .swiper-pagination',
				dynamicBullets: true,
				clickable: true,
			},
			navigation: {
				nextEl: '.pharmacy-home-slider .swiper-button-next',
				prevEl: '.pharmacy-home-slider .swiper-button-prev',
			},
		});
	}

	// Date Range Picker
	if ($('.bookingrange').length > 0) {
		var start = moment().subtract(6, 'days');
		var end = moment();

		function booking_range(start, end) {
			$('.bookingrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
		}

		$('.bookingrange').daterangepicker({
			startDate: start,
			endDate: end,
			ranges: {
				'Today': [moment(), moment()],
				'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
				'Last 7 Days': [moment().subtract(6, 'days'), moment()],
				'Last 30 Days': [moment().subtract(29, 'days'), moment()],
				'This Month': [moment().startOf('month'), moment().endOf('month')],
				'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
			}
		}, booking_range);

		booking_range(start, end);
	}
	// Chat

	var chatAppTarget = $('.chat-window');
	(function () {
		if ($(window).width() > 991)
			chatAppTarget.removeClass('chat-slide');

		$(document).on("click", ".chat-window .chat-users-list a.media", function () {
			if ($(window).width() <= 991) {
				chatAppTarget.addClass('chat-slide');
			}
			return false;
		});
		$(document).on("click", "#back_user_list", function () {
			if ($(window).width() <= 991) {
				chatAppTarget.removeClass('chat-slide');
			}
			return false;
		});
	})();

	//Increment Decrement Numberes
	var quantitiy = 0;
	$('.quantity-right-plus').click(function (e) {
		e.preventDefault();
		var quantity = parseInt($('#quantity').val());
		$('#quantity').val(quantity + 1);
	});

	$('.quantity-left-minus').click(function (e) {
		e.preventDefault();
		var quantity = parseInt($('#quantity').val());
		if (quantity > 0) {
			$('#quantity').val(quantity - 1);
		}
	});

	//Cart Click
	$("#cart").on("click", function (o) {
		o.preventDefault();
		$(".shopping-cart").fadeToggle();
		$(".shopping-cart").toggleClass('show-cart');
	});

	// Circle Progress Bar

	function animateElements() {
		$('.circle-bar1').each(function () {
			var elementPos = $(this).offset().top;
			var topOfWindow = $(window).scrollTop();
			var percent = $(this).find('.circle-graph1').attr('data-percent');
			var animate = $(this).data('animate');
			if (elementPos < topOfWindow + $(window).height() - 30 && !animate) {
				$(this).data('animate', true);
				$(this).find('.circle-graph1').circleProgress({
					value: percent / 100,
					size: 400,
					thickness: 30,
					fill: {
						color: '#da3f81'
					}
				});
			}
		});
		$('.circle-bar2').each(function () {
			var elementPos = $(this).offset().top;
			var topOfWindow = $(window).scrollTop();
			var percent = $(this).find('.circle-graph2').attr('data-percent');
			var animate = $(this).data('animate');
			if (elementPos < topOfWindow + $(window).height() - 30 && !animate) {
				$(this).data('animate', true);
				$(this).find('.circle-graph2').circleProgress({
					value: percent / 100,
					size: 400,
					thickness: 30,
					fill: {
						color: '#68dda9'
					}
				});
			}
		});
		$('.circle-bar3').each(function () {
			var elementPos = $(this).offset().top;
			var topOfWindow = $(window).scrollTop();
			var percent = $(this).find('.circle-graph3').attr('data-percent');
			var animate = $(this).data('animate');
			if (elementPos < topOfWindow + $(window).height() - 30 && !animate) {
				$(this).data('animate', true);
				$(this).find('.circle-graph3').circleProgress({
					value: percent / 100,
					size: 400,
					thickness: 30,
					fill: {
						color: '#1b5a90'
					}
				});
			}
		});
	}

	if ($('.circle-bar').length > 0) {
		animateElements();
	}
	$(window).scroll(animateElements);

	// Preloader

	$(window).on('load', function () {
		if ($('#loader').length > 0) {
			$('#loader').delay(350).fadeOut('slow');
			$('body').delay(350).css({ 'overflow': 'visible' });
		}
	})

	//owl carousel

	if ($('.owl-carousel.clinics').length > 0) {
		$('.owl-carousel.clinics').owlCarousel({
			loop: true,
			margin: 15,
			dots: false,
			nav: true,
			navContainer: '.slide-nav-1',
			navText: ['<i class="fas fa-chevron-left custom-arrow"></i>', '<i class="fas fa-chevron-right custom-arrow"></i>'],
			responsive: {
				0: {
					items: 1
				},
				500: {
					items: 1
				},
				768: {
					items: 3
				},
				1000: {
					items: 4
				},
				1300: {
					items: 6
				}
			}
		})
	}
	if ($('.owl-carousel.our-doctors').length > 0) {
		$('.owl-carousel.our-doctors').owlCarousel({
			loop: true,
			margin: 15,
			dots: false,
			nav: true,
			navContainer: '.slide-nav-2',
			navText: ['<i class="fas fa-chevron-left custom-arrow"></i>', '<i class="fas fa-chevron-right custom-arrow"></i>'],
			responsive: {
				0: {
					items: 1
				},
				500: {
					items: 1
				},
				768: {
					items: 2
				},
				1000: {
					items: 3
				},
				1200: {
					items: 4
				}
			}
		})
	}
	if ($('.owl-carousel.clinic-feature').length > 0) {
		$('.owl-carousel.clinic-feature').owlCarousel({
			loop: true,
			margin: 15,
			dots: false,
			nav: true,
			navContainer: '.slide-nav-3',
			navText: ['<i class="fas fa-chevron-left custom-arrow"></i>', '<i class="fas fa-chevron-right custom-arrow"></i>'],
			responsive: {
				0: {
					items: 1
				},
				500: {
					items: 1
				},
				768: {
					items: 3
				},
				1000: {
					items: 4
				},
				1300: {
					items: 5
				}
			}
		})
	}
	if ($('.owl-carousel.blogs').length > 0) {
		$('.owl-carousel.blogs').owlCarousel({
			loop: true,
			margin: 15,
			dots: false,
			nav: true,
			navContainer: '.slide-nav-4',
			navText: ['<i class="fas fa-chevron-left custom-arrow"></i>', '<i class="fas fa-chevron-right custom-arrow"></i>'],
			responsive: {
				0: {
					items: 1
				},
				500: {
					items: 1
				},
				768: {
					items: 2
				},
				1000: {
					items: 3
				},
				1300: {
					items: 4
				}
			}
		})
	}

	//header-fixed

	if ($('.header-trans').length > 0) {
		$(document).ready(function () {
			$(window).scroll(function () {
				if (scroll > 95) {
					$(".header-trans").css("background", "#2b6ccb");
				}
				else {
					$(".header-trans").css("background", "transparent");
				}
			})
		})
	}
	if ($('.header-trans.custom').length > 0) {
		$(document).ready(function () {
			$(window).scroll(function () {
				var scroll = $(window).scrollTop();
				if (scroll > 95) {
					$(".header-trans").css("background", "#2b6ccb");
				}

				else {
					$(".header-trans").css("background", "transparent");
				}
			})
		})
	}

	// Header Fixed

	if ($('.header-one').length > 0) {
		$(document).ready(function () {
			$(window).scroll(function () {
				var scroll = $(window).scrollTop();
				if (scroll > 35) {
					$(".header-one").addClass('header-space');
				}

				else {
					$(".header-one").removeClass('header-space');
				}
			})
		})
	}
	if ($('.header-ten').length > 0) {
		$(document).ready(function () {
			$(window).scroll(function () {
				var scroll = $(window).scrollTop();
				if (scroll > 35) {
					$(".header-ten").addClass('header-space');
				}

				else {
					$(".header-ten").removeClass('header-space');
				}
			})
		})
	}
	// Header Fixed

	if ($('.header-fourteen').length > 0) {
		$(document).ready(function () {
			$(window).scroll(function () {
				var scroll = $(window).scrollTop();
				if (scroll > 95) {
					$(".header-fourteen").css("background", "#2b6ccb");
				}

				else {
					$(".header-fourteen").css("background", "transparent");
				}
			})
		})
	}
	if ($('.header-fourteen.header-twelve').length > 0) {
		$(document).ready(function () {
			$(window).scroll(function () {
				var scroll = $(window).scrollTop();
				if (scroll > 95) {
					$(".header-fourteen").css("background", "#fff");
				}

				else {
					$(".header-fourteen").css("background", "transparent");
				}
			})
		})
	}
	// Header Fixed

	if ($('.header-fifteen').length > 0) {
		$(document).ready(function () {
			$(window).scroll(function () {
				var scroll = $(window).scrollTop();
				if (scroll > 95) {
					$(".header-trans").css("background", "#FFFFFF");
				}

				else {
					$(".header-trans").css("background", "transparent");
				}
			})
		})
	}
	if ($('.header-trans.custom').length > 0) {
		$(document).ready(function () {
			$(window).scroll(function () {
				var scroll = $(window).scrollTop();
				if (scroll > 95) {
					$(".header-trans").css("background", "#2b6ccb");
				}

				else {
					$(".header-trans").css("background", "transparent");
				}
			})
		})
	}

	if($('.header-trans.header-eleven').length > 0) {
		$(document).ready(function(){
		  $(window).scroll(function(){
			var scroll = $(window).scrollTop();
			  if (scroll > 95) {
				$(".header-trans").css("background" , "#1e5d92");
			  }
	
			  else{
				  $(".header-trans").css("background" , "transparent");  	
			  }
		  })
		})
	}

	// Header Fixed

	if ($('.header-one').length > 0) {
		$(document).ready(function () {
			$(window).scroll(function () {
				var scroll = $(window).scrollTop();
				if (scroll > 35) {
					$(".header-one").addClass('header-space');
				}

				else {
					$(".header-one").removeClass('header-space');
				}
			})
		})
	}
	// Header Fixed

	if ($('.header-fourteen').length > 0) {
		$(document).ready(function () {
			$(window).scroll(function () {
				var scroll = $(window).scrollTop();
				if (scroll > 95) {
					$(".header-fourteen").css("background", "#2b6ccb");
				}

				else {
					$(".header-fourteen").css("background", "transparent");
				}
			})
		})
	}
	// Header Fixed

	if ($('.header-fifteen').length > 0) {
		$(document).ready(function () {
			$(window).scroll(function () {
				var scroll = $(window).scrollTop();
				if (scroll > 95) {
					$(".header-fifteen").css("background", "#ffffff");
				}

				else {
					$(".header-fifteen").css("background", "transparent");
				}
			})
		})
	}

	if ($('.header-sixteen').length > 0) {
		$(document).ready(function () {
			$(window).scroll(function () {
				var scroll = $(window).scrollTop();
				if (scroll > 95) {
					$(".header-sixteen").css("background", "#ffffff");
				}

				else {
					$(".header-sixteen").css("background", "transparent");
				}
			})
		})
	}
	if($('.header-fourteen.header-twelve').length > 0) {
		$(document).ready(function(){
		  $(window).scroll(function(){
			var scroll = $(window).scrollTop();
			if (scroll > 95) {
				$(".header-fourteen").css("background" , "#fff");
			  }

			  else{
				  $(".header-fourteen").css("background" , "transparent");  	
			  }
		  })
		})
	}
	if($('.header-fourteen.header-thirteen').length > 0) {
		$(document).ready(function(){
		  $(window).scroll(function(){
			var scroll = $(window).scrollTop();
			if (scroll > 95) {
				$(".header-fourteen").css("background" , "#fff");
			  }

			  else{
				  $(".header-fourteen").css("background" , "#fff");  	
			  }
		  })
		})
	}
	//for slider
	$(window).on('load resize', function () {
		var window_width = $(window).outerWidth();
		var container_width = $('.container').outerWidth();
		var full_width = window_width - container_width
		var right_position_value = full_width / 2
		$('.slider-service').css('padding-left', right_position_value);

	});


	//BMI Status
	if ($('#bmi-status').length > 0) {
		var options = {
			series: [{
				name: "BMI",
				data: [10, 41, 35, 51, 49, 62, 69, 91, 148]
			}],
			chart: {
				height: 350,
				type: 'line',
				zoom: {
					enabled: false
				}
			},
			dataLabels: {
				enabled: false
			},
			stroke: {
				curve: 'straight'
			},
			title: {
				align: 'left'
			},
			grid: {
				row: {
					colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
					opacity: 0.5
				},
			},
			xaxis: {
				categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
			}
		};

		var chart = new ApexCharts(document.querySelector("#bmi-status"), options);
		chart.render();
	}

	//Heart Rate Status
	if ($('#heartrate-status').length > 0) {
		var options = {
			series: [{
				name: 'HeartRate',
				data: [4, 3, 10, 9, 29, 19, 22, 9, 12, 7, 19, 5, 13, 9, 17, 2, 7, 5]
			}],
			chart: {
				height: 350,
				type: 'line',
			},
			stroke: {
				width: 7,
				curve: 'smooth'
			},
			xaxis: {
				type: 'datetime',
				categories: ['1/11/2000', '2/11/2000', '3/11/2000', '4/11/2000', '5/11/2000', '6/11/2000', '7/11/2000', '8/11/2000', '9/11/2000', '10/11/2000', '11/11/2000', '12/11/2000', '1/11/2001', '2/11/2001', '3/11/2001', '4/11/2001', '5/11/2001', '6/11/2001'],
				tickAmount: 10,
			},
			title: {
				align: 'left',
			},
			fill: {
				type: 'gradient',
				gradient: {
					shade: 'dark',
					gradientToColors: ['#0de0fe'],
					shadeIntensity: 1,
					type: 'horizontal',
					opacityFrom: 1,
					opacityTo: 1,
					stops: [0, 100, 100, 100]
				},
			},
			markers: {
				size: 4,
				colors: ["#15558d"],
				strokeColors: "#fff",
				strokeWidth: 2,
				hover: {
					size: 7,
				}
			},
			yaxis: {
				min: -10,
				max: 40,
				title: {
				},
			}
		};

		var chart = new ApexCharts(document.querySelector("#heartrate-status"), options);
		chart.render();
	}

	//FBC Status
	if ($('#fbc-status').length > 0) {
		var options = {
			series: [{
				name: 'FBC',
				data: [2.3, 3.1, 4.0, 10.1, 4.0, 3.6, 3.2, 2.3, 1.4, 0.8, 0.5, 0.2]
			}],
			chart: {
				height: 350,
				type: 'bar',
			},
			plotOptions: {
				bar: {
					borderRadius: 10,
					dataLabels: {
						position: 'top', // top, center, bottom
					},
				}
			},
			dataLabels: {
				enabled: true,
				formatter: function (val) {
					return val + "%";
				},
				offsetY: -20,
				style: {
					fontSize: '12px',
					colors: ["#304758"]
				}
			},

			xaxis: {
				categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
				position: 'top',
				axisBorder: {
					show: false
				},
				axisTicks: {
					show: false
				},
				crosshairs: {
					fill: {
						type: 'gradient',
						gradient: {
							colorFrom: '#0de0fe',
							colorTo: '#0de0fe',
							stops: [0, 100],
							opacityFrom: 0.4,
							opacityTo: 0.5,
						}
					}
				},
				tooltip: {
					enabled: true,
				}
			},
			yaxis: {
				axisBorder: {
					show: false
				},
				axisTicks: {
					show: false,
				},
				labels: {
					show: false,
					formatter: function (val) {
						return val + "%";
					}
				}

			},
			title: {
				floating: true,
				offsetY: 330,
				align: 'center',
				style: {
					color: '#444'
				}
			}
		};

		var chart = new ApexCharts(document.querySelector("#fbc-status"), options);
		chart.render();
	}

	//Weight Status
	if ($('#weight-status').length > 0) {
		var options = {
			series: [{
				name: 'Weight',
				data: [34, 44, 54, 21, 12, 43, 33, 23, 66, 66, 58]
			}],
			chart: {
				type: 'line',
				height: 350
			},
			stroke: {
				curve: 'stepline',
			},
			dataLabels: {
				enabled: false
			},
			title: {
				align: 'left'
			},
			markers: {
				hover: {
					sizeOffset: 4
				}
			}
		};

		var chart = new ApexCharts(document.querySelector("#weight-status"), options);
		chart.render();
	}

	// Signup Toggle
	$(function () {
		$("#is_registered").click(function () {
			if ($(this).is(":checked")) {
				$("#preg_div").show();
			} else {
				$("#preg_div").hide();
			}
		});
	});

	//Increment Decrement value
	$('.inc.button').click(function () {
		var $this = $(this),
			$input = $this.prev('input'),
			$parent = $input.closest('div'),
			newValue = parseInt($input.val()) + 1;
		$parent.find('.inc').addClass('a' + newValue);
		$input.val(newValue);
		newValue += newValue;
	});
	$('.dec.button').click(function () {
		var $this = $(this),
			$input = $this.next('input'),
			$parent = $input.closest('div'),
			newValue = parseInt($input.val()) - 1;
		console.log($parent);
		$parent.find('.inc').addClass('a' + newValue);
		$input.val(newValue);
		newValue += newValue;
	});

	// Signup Profile
	function readURL(input) {
		if (input.files && input.files[0]) {
			var reader = new FileReader();

			reader.onload = function (e) {
				$('#prof-avatar').attr('src', e.target.result);
			};

			reader.readAsDataURL(input.files[0]);
		}
	}
	$("#profile_image").change(function () {
		readURL(this);
	});

	// Datepicker
	var maxDate = $('#maxDate').val();
	if ($('#dob').length > 0) {
		$('#dob').datepicker({
			startView: 2,
			format: 'dd/mm/yyyy',
			autoclose: true,
			todayHighlight: true,
			endDate: maxDate
		});
	}
	if ($('#editdob').length > 0) {
		$('#editdob').datepicker({
			startView: 2,
			format: 'dd/mm/yyyy',
			autoclose: true,
			todayHighlight: true,
			endDate: maxDate
		});
	}

	// Search Bar

	$(document).ready(function () {
		$(".searchbar a").click(function () {
			$(".togglesearch").slideToggle();
			$(".top-search").focus();
		});
	});

	if ($('#more-view2').length > 0) {
		const button = document.getElementById('more-view2');
		const container = document.getElementById('fill-more2');

		let isLess = true;

		function showMoreLess() {
			if (isLess) {
				isLess = false;
				container.style.height = 'auto';
				button.innerHTML = "Show less <i class='feather-chevrons-right ms-1'>";
			} else {
				isLess = true;
				container.style.height = '100px';
				button.innerHTML = "Show more <i class='feather-chevrons-right ms-1'></i>";
			}
		}
		button.addEventListener('click', showMoreLess);
	}

	if ($('#more-view').length > 0) {
		const button = document.getElementById('more-view');
		const container = document.getElementById('fill-more');

		let isLess = true;

		function showMoreLess() {
			if (isLess) {
				isLess = false;
				container.style.height = 'auto';
				button.innerHTML = "Show less <i class='feather-chevrons-right ms-1'>";
			} else {
				isLess = true;
				container.style.height = '100px';
				button.innerHTML = "Show more <i class='feather-chevrons-right ms-1'></i>";
			}
		}
		button.addEventListener('click', showMoreLess);
	}

	if ($('#more-view1').length > 0) {
		const button = document.getElementById('more-view1');
		const container = document.getElementById('fill-more1');

		let isLess = true;

		function showMoreLess() {
			if (isLess) {
				isLess = false;
				container.style.height = 'auto';
				button.innerHTML = "Show less <i class='feather-chevrons-right ms-1'>";
			} else {
				isLess = true;
				container.style.height = '100px';
				button.innerHTML = "Show more <i class='feather-chevrons-right ms-1'></i>";
			}
		}
		button.addEventListener('click', showMoreLess);
	}

	$('.favourite-btn .favourite-icon').on('click', function () {
		$(this).toggleClass('favourite');
	});

	$('.favourite-btn-two .favourite-icon-two').on('click', function () {
		$(this).toggleClass('favourite-two');
	});

	// Price Slider

	if ($('#price-range').length > 0) {
		$('#pricerangemin').text(10);
		$('#pricerangemax').text(10000);
		$("#price-range").slider({
			range: true,
			min: 10,
			max: 10000,
			values: [10, 5000],

			slide: function (event, ui) {
				$("#pricerangemin").text(ui.values[0]);
				$("#pricerangemax").text(ui.values[1]);
			}
		});
	}

	// Map

	$("#map-list").on('click', function () {
		$(this).closest(".container").addClass('container-fluid');
		$(this).closest(".container-fluid").removeClass('container');
		$(".map-view").removeClass('col-xl-12').addClass('col-xl-9');
		$(".map-right").css('display', 'block');
		$('.time-slot-slider')[0].slick.refresh();
	});

	// Cursor

	function mim_tm_cursor() {
		var myCursor = jQuery('.mouse-cursor');
		if (myCursor.length) {
			if ($("body")) {
				const e = document.querySelector(".cursor-inner"),
					t = document.querySelector(".cursor-outer");
				let n, i = 0,
					o = !1;
				window.onmousemove = function (s) {
					o || (t.style.transform = "translate(" + s.clientX + "px, " + s.clientY + "px)"), e.style.transform = "translate(" + s.clientX + "px, " + s.clientY + "px)", n = s.clientY, i = s.clientX
				}, $("body").on("mouseenter", "a, .cursor-pointer", function () {
					e.classList.add("cursor-hover"), t.classList.add("cursor-hover")
				}), $("body").on("mouseleave", "a, .cursor-pointer", function () {
					$(this).is("a") && $(this).closest(".cursor-pointer").length || (e.classList.remove("cursor-hover"), t.classList.remove("cursor-hover"))
				}), e.style.visibility = "visible", t.style.visibility = "visible"
			}
		}
	};
	mim_tm_cursor()

	// Slick Slider
	if ($('.onboard-slider').length > 0) {
		$('#onboard-slider').owlCarousel({
			items: 1,
			margin: 30,
			dots: true,
			nav: true,
			navText: false,
			loop: true,
			smartSpeed: 450,
			autoplay: true,
			autoplayTimeout: 5000,
			autoplayHoverPause: true,
			responsiveClass: true,
			responsive: {
				0: {
					items: 1
				},
				768: {
					items: 1
				},
				1170: {
					items: 1
				}
			}
		});
	}

	// Toggle Password

	if ($('.toggle-password').length > 0) {
		$(document).on('click', '.toggle-password', function () {
			$(this).toggleClass("feather-eye-off");
			var input = $(".pass-input");
			if (input.attr("type") == "password") {
				input.attr("type", "text");
			} else {
				input.attr("type", "password");
			}
		});
	}

	if ($('.toggle-password-sub').length > 0) {
		$(document).on('click', '.toggle-password-sub', function () {
			$(this).toggleClass("feather-eye-off");
			var input = $(".pass-input-sub");
			if (input.attr("type") == "password") {
				input.attr("type", "text");
			} else {
				input.attr("type", "password");
			}
		});
	}

	// Custom Country Code Selector

	if ($('#phone').length > 0) {
		var input = document.querySelector("#phone");
		window.intlTelInput(input, {
			utilsScript: "assets/plugins/intltelinput/js/utils.js",
		});
	}

	// Custom Country Code Selector

	if ($('#phone-number').length > 0) {
		var input = document.querySelector("#phone-number");
		window.intlTelInput(input, {
			utilsScript: "assets/plugins/intltelinput/js/utils.js",
		});
	}

	// Otp Verfication

	$('.digit-group').find('input').each(function () {
		$(this).attr('maxlength', 1);
		$(this).on('keyup', function (e) {
			var parent = $($(this).parent());

			if (e.keyCode === 8 || e.keyCode === 37) {
				var prev = parent.find('input#' + $(this).data('previous'));

				if (prev.length) {
					$(prev).select();
				}
			} else if ((e.keyCode >= 48 && e.keyCode <= 57) || (e.keyCode >= 65 && e.keyCode <= 90) || (e.keyCode >= 96 && e.keyCode <= 105) || e.keyCode === 39) {
				var next = parent.find('input#' + $(this).data('next'));

				if (next.length) {
					$(next).select();
				} else {
					if (parent.data('autosubmit')) {
						parent.submit();
					}
				}
			}
		});
	});

	$('.digit-group input').on('keyup', function () {
		var self = $(this);
		if (self.val() != '') {
			self.addClass('active');
		} else {
			self.removeClass('active');
		}
	});

	// Doctor Signup Wizard

	let progressVal = 0;
	let businessType = 0;

	$(".next_btn").click(function () {
		$(this).parent().parent().next().fadeIn('slow');
		$(this).parent().parent().css({
			'display': 'none'
		});
		progressVal = progressVal + 1;
		$('.progress-active').removeClass('progress-active').addClass('progress-activated').next().addClass('progress-active');
	});

	$(".prev_btn").click(function () {
		$(this).parent().parent().prev().fadeIn('slow');
		$(this).parent().parent().css({
			'display': 'none'
		});
		progressVal = progressVal - 1;
		$('.progress-active').removeClass('progress-active').prev().removeClass('progress-activated').addClass('progress-active');
	});
	// Select Favourite

	$('.fav-item').on('click', function () {
		$(this).toggleClass('selected');
		//$(this).children().toggleClass("feather-heart fa-solid fa-heart");
	});

})(jQuery);