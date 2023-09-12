// 로고 크기 동적 변경
$("<img/>")
  .attr("src", "static/image/logo.png")
  .on("load", function () {
    $(this).remove();

    var fixedHeight = 96;
    var width = this.width;
    var height = this.height;

    var ratio = width / height;
    var fixedWidth = ratio * fixedHeight;

    $(".logo-container").css({
      width: fixedWidth + "px",
      height: fixedHeight + "px",
    });
  });

// 날짜를 범위로 지정하는 라이브러리
$("#calendar").daterangepicker(
  {
    minYear: 2023,
    maxYear: 2023,
    timePicker: true,
    timePicker24Hour: true,
    timePickerIncrement: 10,
    autoApply: true,
    maxSpan: { days: 7 },
    locale: {
      format: "YYYY-MM-DD",
      separator: " - ",
      applyLabel: "선택",
      cancelLabel: "취소",
      fromLabel: "부터",
      toLabel: "까지",
      customRangeLabel: "Custom",
      weekLabel: "W",
      daysOfWeek: ["일", "월", "화", "수", "목", "금", "토"],
      monthNames: [
        "1월",
        "2월",
        "3월",
        "4월",
        "5월",
        "6월",
        "7월",
        "8월",
        "9월",
        "10월",
        "11월",
        "12월",
      ],
      firstDay: 1,
    },
    linkedCalendars: false,
    showCustomRangeLabel: false,
    alwaysShowCalendars: true,
    parentEl: "datefilter",
    startDate: "2023-08-01",
    endDate: "2023-08-02",
    minDate: "2023-08-01",
    maxDate: "2023-12-31",
    opens: "center",
    drops: "up",
  },
  function (start, end, label) {
    $('input[name="startDate"]').val(start.format("YYYY-MM-DD HH:mm:ss"));
    $('input[name="endDate"]').val(end.format("YYYY-MM-DD HH:mm:ss"));
    console.log(
      "New date range selected: " +
        start.format("YYYY-MM-DD HH:mm:ss") +
        " to " +
        end.format("YYYY-MM-DD HH:mm:ss") +
        " (predefined range: " +
        label +
        ")"
    );
  }
);

$(document).ready(function () {
  $("#start").click(function () {
    $("#start").addClass("visually-hidden");
    $("#p-snipe").removeClass("visually-hidden");

    $("html, body").animate(
      {
        scrollTop: $("#p-snipe").offset().top,
      },
      700
    );
  });

  var districtData = {
    제주시: [
      "건입동",
      "구좌읍",
      "내도동",
      "노형동",
      "삼도이동",
      "삼도일동",
      "삼양이동",
      "애월읍",
      "연동",
      "오등동",
      "오라이동",
      "외도일동",
      "용담삼동",
      "용담이동",
      "용담일동",
      "우도면",
      "이도이동",
      "이호일동",
      "조천읍",
      "한림읍",
    ],
    서귀포시: [
      "강정동",
      "남원읍",
      "대정읍",
      "법환동",
      "보목동",
      "상예동",
      "색달동",
      "서귀동",
      "서호동",
      "서홍동",
      "성산읍",
      "안덕면",
      "중문동",
      "토평동",
      "표선면",
      "하예동",
      "호근동",
    ],
  };

  $("#city").on("click", function () {
    var city = $(this).val();

    $("#district").empty();
    if (city in districtData) {
      districtData[city].forEach(function (district) {
        $("#district").append(new Option(district, district));
      });
    }
    $("#submit").prop("disabled", false);
  });

  $("form").on("submit", function (e) {
    e.preventDefault();

    var form = $(this);
    var url = form.attr("action");

    $.ajax({
      type: "POST",
      url: url,
      data: form.serialize(),
      success: function (data) {
        $("#p-snipe").fadeOut("slow", function () {
          $("#result-card")
            .html(data)
            .hide()
            .fadeIn("slow", function () {
              $("html, body").animate(
                {
                  scrollTop: $("#output-title").offset().top - 175,
                },
                "slow"
              );
            });
        });
      },
    });
  });

  $(document).on("click", "#plan-again", function () {
    location.reload();
  });

  $(document).on("click", "#toggleIcon", function () {
    $(this).toggleClass("rotate-90");

    setTimeout(function () {
      $("html, body").animate(
        { scrollTop: $("#toggleIcon").offset().top - 210 },
        "slow"
      );
    }, 500);
  });
});
