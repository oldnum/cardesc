var months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
var currentYear = 0;
var currentMonth = 0;

function formatCC(el, typeel) {
  var ccNumString = el.val();
  ccNumString = ccNumString.replace(/[^0-9]/g, "");
  var typeCheck = ccNumString.substring(0, 2);
  var cType = "";
  var block1 = "";
  var block2 = "";
  var block3 = "";
  var block4 = "";
  var formatted = "";

  if (typeCheck.length == 2) {
    typeCheck = parseInt(typeCheck);
    if (typeCheck >= 40 && typeCheck <= 49) {
      cType = "Visa";
    } else if ((typeCheck >= 51 && typeCheck <= 55) || (typeCheck >= 22 && typeCheck <= 27)) {
      cType = "Master Card";
    } else if (
      (typeCheck >= 60 && typeCheck <= 62) ||
      typeCheck == 64 ||
      typeCheck == 65
    ) {
      cType = "Discover";
    } else if (typeCheck == 34 || typeCheck == 37) {
      cType = "American Express";
    } else if (typeCheck >= 35 && typeCheck <= 39) {
      cType = "JCB";
    } else if (typeCheck == 62) {
      cType = "UnionPay";
    } else if ((typeCheck >= 50 && typeCheck <= 59) || typeCheck == 67) {
      cType = "Maestro";
    } else {
      cType = "Invalid";
    }
  }

  block1 = ccNumString.substring(0, 4);
  if (block1.length == 4) {
    block1 = block1 + " ";
  }

  if (cType == "Visa" || cType == "Master Card" || cType == "Discover" || cType == "JCB" || cType == "UnionPay" || cType == "Maestro") {
    block2 = ccNumString.substring(4, 8);
    if (block2.length == 4) {
      block2 = block2 + " ";
    }
    block3 = ccNumString.substring(8, 12);
    if (block3.length == 4) {
      block3 = block3 + " ";
    }
    block4 = ccNumString.substring(12, 16);
  } else if (cType == "American Express") {
    block2 = ccNumString.substring(4, 10);
    if (block2.length == 6) {
      block2 = block2 + " ";
    }
    block3 = ccNumString.substring(10, 15);
    block4 = "";
  } else if (cType == "Invalid") {
    block1 = typeCheck;
    block2 = "";
    block3 = "";
    block4 = "";
  }

  formatted = block1 + block2 + block3 + block4;
  el.val(formatted);
  typeel.text(cType);
}

function loadactions() {
  $("body")
    .off("keyup", 'input[name="creditcard_number"]')
    .on("keyup", 'input[name="creditcard_number"]', function () {
      var typeel = $(this).closest("form").find(".card-type");
      var el = $(this);
      formatCC(el, typeel);
    })
    .off("keyup", 'input[name="cvc"]')
    .on("keyup", 'input[name="cvc"]', function () {
      var myvalue = $(this).val();
      myvalue = myvalue.replace(/\D/g, "");
      $(this).val(myvalue);
    })
    .off("change", "form input,form select")
    .on("change", "form input,form select", function () {
      var validated = true;
      $("form input, form select").each(function () {
        if ($(this).val() == "") {
          validated = false;
        }
      });
      if (validated == false) {
        $("button").attr("disabled", "disabled");
      } else {
        $("button").removeAttr("disabled");
      }
    });
}
$(function () {
  currentYear = new Date().getFullYear();
  currentMonth = new Date().getMonth() + 1;
  var yearArr = [];
  for (var i = 0; 9 > i; i++) {
    var newyearvalue = currentYear + i;
    yearArr.push(newyearvalue);
  }
  var yearOptionsHTML = "";
  for (var i = 0; yearArr.length > i; i++) {
    yearOptionsHTML += "<option>" + yearArr[i] + "</option>";
  }
  $('select[name="year"]').html(yearOptionsHTML);

  var monthOptionsHTML = "";
  for (var i = 0; months.length > i; i++) {
    monthOptionsHTML += "<option";
    if (months[i] == currentMonth) {
      monthOptionsHTML += ' selected="selected"';
    }
    var mymonth = months[i];
    mymonth = mymonth.toString();
    if (mymonth.length == 1) {
      mymonth = "0" + mymonth;
    }
    monthOptionsHTML += ">" + mymonth + "</option>";
  }
  $('select[name="month"]').html(monthOptionsHTML);
  loadactions();
});