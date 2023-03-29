jQuery(function() {

    jQuery(".progresss").each(function() {

        var value = jQuery(this).attr('data-value');
        var left = jQuery(this).find('.progresss-left .progresss-bar');
        var right = jQuery(this).find('.progresss-right .progresss-bar');

        if (value > 0) {
            if (value <= 50) {
                right.css('transform', 'rotate(' + percentageToDegrees(value) + 'deg)')
            } else {
                right.css('transform', 'rotate(180deg)')
                left.css('transform', 'rotate(' + percentageToDegrees(value - 50) + 'deg)')
            }
        }

    })

    function percentageToDegrees(percentage) {

        return percentage / 100 * 360

    }

});


jQuery(document).ready(function() {
    jQuery('textarea#summernote,textarea#summernote2').summernote({
        height: 550, //set editable area's height
        dialogsInBody: true
    });
});


jQuery('.custom-radio-box input').on('click', function() {
    if (jQuery(this).val() == 'Country Specific') {
        jQuery('.form-group.filters-wrap').css('display', 'flex')
    } else {
        jQuery('.form-group.filters-wrap').css('display', 'none')
    }
})


jQuery('#date-range,#date-range-2,#date-range-3,#date-range-4').datepicker({
    todayHighlight: true
});
jQuery('a.filterDrop').on('click', function() {
    jQuery(this).siblings('ul.filter-list-Box').toggle();
})
jQuery(document).mouseup(function(e) {
    var container = jQuery("ul.filter-list-Box");
    if (!container.is(e.target) && container.has(e.target).length === 0) {
        container.hide();
    }
});


// jQuery('.dishtab-show').css('display', 'none');
// jQuery('ul.nav.rrm-tabs-link li a').on('click', function() {
//     if (jQuery(this).hasClass('dish-tab')) {
//         jQuery('.dishtab-show').css('display', 'none');
//         jQuery('.rating-filter').css('display', 'none');
//     } else {
//         jQuery('.dishtab-show').css('display', 'block');
//         jQuery('.rating-filter').css('display', 'flex');
//     }
// })

jQuery(document).ready(function() {
    jQuery('.js-example-basic-single').select2({
        minimumResultsForSearch: -1
    });
});
jQuery('a.notification-bell').on('click', function() {
    jQuery('.notification-bell-dm').toggle()
})

jQuery(".hide-show-pass").click(function() {
    jQuery(this).children().toggleClass("fa-eye fa-eye-slash");
    input = jQuery(this).parent().find("input");
    if (input.attr("type") == "password") {
        input.attr("type", "text");
    } else {
        input.attr("type", "password");
    }
});

jQuery(function() {
    let pageName = location.pathname.split('/').slice(-1)[0];
    let currentLink = jQuery('.navbar-nav > .nav-item > .nav-link[href="' + pageName + '"]');
    if (pageName) {
        if (currentLink) {
            jQuery('.navbar-nav > .nav-item > .nav-link').removeClass('active');
            currentLink.addClass('active');
        }
    }
});


jQuery(function() {
var x, i, j, l, ll, selElmnt, a, b, c;
/*look for any elements with the class "custom-select":*/
x = document.getElementsByClassName("custom-select");
l = x.length;
for (i = 0; i < l; i++) {
    selElmnt = x[i].getElementsByTagName("select")[0];
    ll = selElmnt.length;
    /*for each element, create a new DIV that will act as the selected item:*/
    a = document.createElement("DIV");
    a.setAttribute("class", "select-selected");
    a.innerHTML = selElmnt.options[selElmnt.selectedIndex].innerHTML;
    x[i].appendChild(a);
    /*for each element, create a new DIV that will contain the option list:*/
    b = document.createElement("DIV");
    b.setAttribute("class", "select-items select-hide");
    for (j = 1; j < ll; j++) {
        /*for each option in the original select element,
        create a new DIV that will act as an option item:*/
        c = document.createElement("DIV");
        c.innerHTML = selElmnt.options[j].innerHTML;
        c.addEventListener("click", function(e) {
            /*when an item is clicked, update the original select box,
            and the selected item:*/
            var y, i, k, s, h, sl, yl;
            s = this.parentNode.parentNode.getElementsByTagName("select")[0];
            sl = s.length;
            h = this.parentNode.previousSibling;
            for (i = 0; i < sl; i++) {
                if (s.options[i].innerHTML == this.innerHTML) {
                    s.selectedIndex = i;
                    h.innerHTML = this.innerHTML;
                    y = this.parentNode.getElementsByClassName("same-as-selected");
                    yl = y.length;
                    for (k = 0; k < yl; k++) {
                        y[k].removeAttribute("class");
                    }
                    this.setAttribute("class", "same-as-selected");
                    break;
                }
            }
            h.click();
        });
        b.appendChild(c);
    }
    x[i].appendChild(b);
    a.addEventListener("click", function(e) {
        /*when the select box is clicked, close any other select boxes,
        and open/close the current select box:*/
        e.stopPropagation();
        closeAllSelect(this);
        this.nextSibling.classList.toggle("select-hide");
        this.classList.toggle("select-arrow-active");
    });
}

function closeAllSelect(elmnt) {
    /*a function that will close all select boxes in the document,
    except the current select box:*/
    var x, y, i, xl, yl, arrNo = [];
    x = document.getElementsByClassName("select-items");
    y = document.getElementsByClassName("select-selected");
    xl = x.length;
    yl = y.length;
    for (i = 0; i < yl; i++) {
        if (elmnt == y[i]) {
            arrNo.push(i)
        } else {
            y[i].classList.remove("select-arrow-active");
        }
    }
    for (i = 0; i < xl; i++) {
        if (arrNo.indexOf(i)) {
            x[i].classList.add("select-hide");
        }
    }
}
/*if the user clicks anywhere outside the select box,
then close all select boxes:*/
document.addEventListener("click", closeAllSelect);
});

jQuery(function() {
var xValues = ["Bad", "Okay", "Good", "Very Good"];
var yValues = [10, 20, 20, 50];
var barColors = [
    "#B40000",
    "#E1B31F",
    "#7C9204",
    "#249204"
];
var settings = {
    type: "pie",
    data: {
        labels: xValues,
        datasets: [{
            backgroundColor: barColors,
            data: yValues
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'bottom',
                display: false,
            },
            title: {
                display: false,
                text: 'Chart.js Pie Chart'
            }
        }
    },
}
new Chart("myPieChart", settings);
new Chart("myPieChart2", settings);
new Chart("myPieChart3", settings);
});
jQuery(function() {
var xValues = ["â˜…1", "â˜…2", "â˜…3", "â˜…4", "â˜…5"];
var yValues = [55, 49, 44, 24, 15];
var barColors = ["#000000", "#000000","#000000","#000000","#000000"];

new Chart("myChart", {
  type: "bar",
  data: {
    labels: xValues,
    datasets: [{
      backgroundColor: barColors,
      data: yValues
    }]
  },
  options: {
    legend: {display: false},
    title: {
      display: false
    }
  }
});
});


jQuery('.information-style').on('click',function(){
    jQuery('.SelectdropDown').toggle();
})


jQuery(document).ready(function() {
    jQuery('.select-country,.select-state,.select-city,.select-town,.select-order').select2({
        minimumResultsForSearch: -1,
        // dropdownParent: jQuery('#addCountry')
    });
});
jQuery('.common-select').select2({
        minimumResultsForSearch: -1,
        // dropdownParent: jQuery('#addCountry')
    });

jQuery(document).ready(function() {
    jQuery('.cook-drop-list').css('display','inline-block');
    jQuery('.cook-tabs a.nav-link').on('click',function(){
        if(jQuery(this).hasClass('cook-drop-list')){
            jQuery('.cf-drop-list').css('display','none');
            jQuery('.cook-drop-list').css('display','inline-block');
        }else if(jQuery(this).hasClass('fsc-drop-list')){
            jQuery('.cf-drop-list').css('display','none');
            jQuery('.fsc-drop-list').css('display','inline-block');        
        }else{
            jQuery('.cf-drop-list').css('display','none');        
        }
    });
});

jQuery(document).ready(function() {
    jQuery('.courier-drop-list').css('display', 'inline-block')
    jQuery('.cook-tabs a.nav-link').on('click', function() {
        if (jQuery(this).hasClass('show-upload')) {
            jQuery('.upload-doc').css('display', 'block')
        } else if(jQuery(this).hasClass('courier-drop')){
            jQuery('.courier-drop-list').css('display', 'inline-block')
        }else{
            jQuery('.courier-drop-list').css('display', 'none')        
            jQuery('.upload-doc').css('display', 'none')
        }
    });
});

$(document).ready(function(){

   $('.timepicker-12-hr').wickedpicker();

});

$('.timepicker-12-hr').wickedpicker({
        now: "12:35", //hh:mm 24 hour format only, defaults to current time
        twentyFour: false,  //Display 24 hour format, defaults to false
        upArrow: 'wickedpicker__controls__control-up',  //The up arrow class selector to use, for custom CSS
        downArrow: 'wickedpicker__controls__control-down', //The down arrow class selector to use, for custom CSS
        close: 'wickedpicker__close', //The close class selector to use, for custom CSS
        hoverState: 'hover-state', //The hover state class to use, for custom CSS
        title: 'Timepicker', //The Wickedpicker's title,
        showSeconds: false, //Whether or not to show seconds,
        timeSeparator: ' : ', // The string to put in between hours and minutes (and seconds)
        secondsInterval: 1, //Change interval for seconds, defaults to 1,
        minutesInterval: 1, //Change interval for minutes, defaults to 1
        beforeShow: null, //A function to be called before the Wickedpicker is shown
        afterShow: null, //A function to be called after the Wickedpicker is closed/hidden
        show: null, //A function to be called when the Wickedpicker is shown
        clearable: false, //Make the picker's input clearable (has clickable "x")
});

