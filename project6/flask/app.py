from flask import Flask, render_template, request, redirect, url_for, flash, session
import pickle
import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta, date

app = Flask(__name__)


def get_weekday(date):
    day = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    return day[date.weekday()]


def is_weekend_or_holiday(date):
    holiday_list = [
        "2023-08-15",
        "2023-09-28",
        "2023-09-29",
        "2023-09-30",
        "2023-10-03",
        "2023-10-09",
        "2023-12-25",
    ]
    if date.weekday() >= 5:
        return "주말"
    elif date.strftime("%Y-%m-%d") in holiday_list:
        return "공휴일"
    else:
        return "평일"


def is_weekend(date):
    if date.weekday() >= 5:
        return "주말"
    else:
        return "평일"


def is_peak_season(date_str):
    peak_seasons = [
        (date(2023, 8, 1), date(2023, 8, 19)),  # 8월 성수기
        (date(2023, 9, 27), date(2023, 9, 30)),  # 9월 성수기
        (date(2023, 10, 1), date(2023, 10, 4)),  # 10월 성수기
        (date(2023, 10, 9), date(2023, 10, 10)),  # 10월 성수기
        (date(2023, 12, 22), date(2023, 12, 25)),  # 12월 성수기
        (date(2023, 12, 29), date(2023, 12, 31)),  # 12월 성수기
    ]
    for peak_start, peak_end in peak_seasons:
        if peak_start <= date_str <= peak_end:
            return "성수기"
    return "비수기"


def format_number_with_won(number):
    return "￦{:,.0f}".format(number)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        print(request.form)
        # flight_xgb = pickle.load(open("./data/xgb_model_flight.pkl", "rb"))
        # test_data = np.array([[0, 0, 0, 1, 60, 0, 1, 0, 1]])
        # test_predict = flight_xgb.predict(test_data)

        # 일단 인풋 데이터부터 정제
        input_start_date = request.form["startDate"].split(" ")[0]
        input_start_time = request.form["startDate"].split(" ")[1]
        input_start_datetime = request.form["startDate"]

        input_end_date = request.form["endDate"].split(" ")[0]
        input_end_time = request.form["endDate"].split(" ")[1]
        input_end_datetime = request.form["endDate"]

        input_headcount = int(request.form["headcount"])

        input_airport = request.form["airport"]
        input_city = request.form["city"]
        input_district = request.form["district"]
        input_location = input_city + " " + input_district

        # 실제 데이터를 이용한 추천 시스템 (랜덤으로 추천)
        # 항공권
        flight_csv = pd.read_csv("./data/flight.csv", encoding="utf-8")
        flight_csv["departure_datetime"] = pd.to_datetime(
            flight_csv["date"] + " " + flight_csv["departure_time"]
        )
        time_start_input = pd.to_datetime(input_start_datetime)
        time_end_input = pd.to_datetime(input_end_datetime)
        flight_start_result = pd.DataFrame()
        flight_end_result = pd.DataFrame()

        # 출발 기준
        # 미래의 시간으로부터 추출 (오류 방지용)
        future_flight_csv = flight_csv[flight_csv["departure_place"] == input_airport]
        future_flight_csv = future_flight_csv["departure_datetime"][
            flight_csv["departure_datetime"] > time_start_input
        ]

        # 미래의 시간 중에서 가장 가까운 시간 추출
        if not future_flight_csv.empty:

            closest_time_idx = (future_flight_csv - time_start_input).idxmin()
            flight_start_result = flight_csv.iloc[closest_time_idx]

        print(flight_start_result)

        # 도착 기준
        # 미래의 시간으로부터 추출 (오류 방지용)
        future_flight_csv = flight_csv[flight_csv["departure_place"] == "CJU"]
        future_flight_csv = future_flight_csv[
            flight_csv["arrival_place"] == input_airport
        ]
        future_flight_csv = future_flight_csv["departure_datetime"][
            flight_csv["departure_datetime"] > time_end_input
        ]

        # 미래의 시간 중에서 가장 가까운 시간 추출
        if not future_flight_csv.empty:
            closest_time_idx = (future_flight_csv - time_end_input).idxmin()
            flight_end_result = flight_csv.iloc[closest_time_idx]

        print(flight_end_result)

        # 호텔
        hotel_csv = pd.read_csv("./data/hotel.csv", encoding="utf-8")
        hotel_result = pd.DataFrame()

        # 날짜가 겹치는 호텔만 먼저 추출 후
        date_hotel_csv = hotel_csv[hotel_csv["date"] == input_start_date]

        # 시, 동이 일치하는 호텔만 추출
        matching_hotel_csv = pd.DataFrame()
        if not date_hotel_csv.empty:
            matching_hotel_csv = date_hotel_csv[
                date_hotel_csv["location"].str.contains(input_location)
            ]

        if not matching_hotel_csv.empty:
            hotel_result = matching_hotel_csv.sample().iloc[0]

        print(hotel_result)

        # 렌트카
        car_csv = pd.read_csv("./data/car.csv", encoding="utf-8")
        car_result = pd.DataFrame()

        # 날짜가 겹치는 렌트카만 먼저 추출 후
        date_car_csv = car_csv[car_csv["date"] == input_start_date]

        # 5인승만 골라서
        matching_car_csv = pd.DataFrame()
        if not date_car_csv.empty:
            matching_car_csv = date_car_csv[
                date_car_csv["category"].isin(
                    ["경차", "소형SUV", "소형차", "중형SUV", "중형차", "준중형"]
                )
            ]
            matching_car_csv = matching_car_csv[matching_car_csv["made"] == "국산차"]

        # 랜덤으로 하나 선택
        if not matching_car_csv.empty:
            car_result = matching_car_csv.sample().iloc[0]

        print(car_result)

        # 실제 총 가격 계산
        total_price = 0

        # 며칠 묵는지 계산
        start_datetime = datetime.strptime(input_start_datetime, "%Y-%m-%d %H:%M:%S")
        start_date = start_datetime.date()
        end_datetime = datetime.strptime(input_end_datetime, "%Y-%m-%d %H:%M:%S")
        end_date = end_datetime.date()

        travel_days = (end_datetime - start_datetime).days
        print(travel_days)

        template_data = 0

        if (
            not car_result.empty
            and not flight_start_result.empty
            and not flight_end_result.empty
            and not hotel_result.empty
        ):
            total_price += (
                flight_start_result["price"] + flight_end_result["price"]
            ) * input_headcount
            total_price += (hotel_result["price"] + car_result["price"]) * travel_days

            template_data = {
                "hotel": hotel_result.to_dict(),
                "flight_start": flight_start_result.to_dict(),
                "flight_end": flight_end_result.to_dict(),
                "car": car_result.to_dict(),
                "total_price": {
                    "price": total_price,
                    "price_per_head": total_price / input_headcount,
                },
            }

            # 숫자를 원화로 변환
            keys_to_format = [
                "hotel",
                "flight_start",
                "flight_end",
                "car",
                "total_price",
            ]

            for key in keys_to_format:
                if key in template_data and "price" in template_data[key]:
                    template_data[key]["price"] = format_number_with_won(
                        template_data[key]["price"]
                    )

            template_data["total_price"]["price_per_head"] = format_number_with_won(
                template_data["total_price"]["price_per_head"]
            )

        print(template_data)

        # 모델 예측
        # 일단 모델 전부 불러오기
        flight_pkl = pickle.load(open("./data/xgb_model_flight.pkl", "rb"))
        hotel_pkl = pickle.load(open("./data/xgb_model_hotel.pkl", "rb"))
        rent_pkl = pickle.load(open("./data/xgb_model_rent.pkl", "rb"))

        # 항공권
        flight_xgb_model = flight_pkl

        feature_list = [
            "departure_time",
            "departure_place",
            "arrival_place",
            "day",
            "holiday",
            "peak_season",
        ]
        departure_place_mapping = {"CJJ": 0, "CJU": 1, "GMP": 2, "PUS": 3}
        arrival_place_mapping = {"CJJ": 0, "CJU": 1, "GMP": 2, "PUS": 3}
        day_mapping = {
            "금요일": 0,
            "목요일": 1,
            "수요일": 2,
            "월요일": 3,
            "일요일": 4,
            "토요일": 5,
            "화요일": 6,
        }
        holiday_mapping = {"공휴일": 0, "주말": 1, "평일": 2}
        peak_season_mapping = {"비수기": 0, "성수기": 1}

        # 모델에 맞게 데이터 정제
        # ['departure_time', 'departure_place', 'arrival_place', 'day', 'holiday', 'peak_season']
        # 출발 기준
        flight_start_departure_time = int(input_start_time.split(":")[0]) * 60 + int(
            input_start_time.split(":")[1]
        )
        flight_start_departure_place = departure_place_mapping[input_airport]
        flight_start_arrival_place = arrival_place_mapping["CJU"]
        flight_start_day = day_mapping[get_weekday(start_datetime)]
        flight_start_holiday = holiday_mapping[is_weekend_or_holiday(start_datetime)]
        flight_start_peak_season = peak_season_mapping[is_peak_season(start_date)]

        flight_start_features = [
            flight_start_departure_time,
            flight_start_departure_place,
            flight_start_arrival_place,
            flight_start_day,
            flight_start_holiday,
            flight_start_peak_season,
        ]

        print(flight_start_features)
        flight_start_predict = flight_xgb_model.predict(
            np.array([flight_start_features])
        )

        # 도착 기준
        flight_end_departure_time = int(input_end_time.split(":")[0]) * 60 + int(
            input_end_time.split(":")[1]
        )
        flight_end_departure_place = departure_place_mapping["CJU"]
        flight_end_arrival_place = arrival_place_mapping[input_airport]
        flight_end_day = day_mapping[get_weekday(end_datetime)]
        flight_end_holiday = holiday_mapping[is_weekend_or_holiday(end_datetime)]
        flight_end_peak_season = peak_season_mapping[is_peak_season(end_date)]
        flight_end_features = [
            flight_end_departure_time,
            flight_end_departure_place,
            flight_end_arrival_place,
            flight_end_day,
            flight_end_holiday,
            flight_end_peak_season,
        ]

        print(flight_end_features)
        flight_end_predict = flight_xgb_model.predict(np.array([flight_end_features]))

        print(flight_start_predict, flight_end_predict)

        # 호텔
        hotel_xgb_model = hotel_pkl

        person_mapping = {"2인": 0, "4인": 1}  # (4인 : 2인도 포함 / 2인 : 2인만)
        level_mapping = {
            "1성급": 0,
            "2성급": 1,
            "비지니스": 2,
            "3성급": 3,
            "콘도": 4,
            "관광": 5,
            "부티크": 6,
            "레지던스": 7,
            "4성급": 8,
            "가족호텔": 9,
            "5성급": 10,
        }
        city_mapping = {"제주시": 0, "서귀포시": 1}
        city_details_mapping = {
            "강정동": 0,
            "건입동": 1,
            "구좌읍": 2,
            "남원읍": 3,
            "내도동": 4,
            "노형동": 5,
            "대정읍": 6,
            "법환동": 7,
            "보목동": 8,
            "삼도이동": 9,
            "삼도일동": 10,
            "삼양이동": 11,
            "상예동": 12,
            "색달동": 13,
            "서귀동": 14,
            "서호동": 15,
            "서홍동": 16,
            "성산읍": 17,
            "안덕면": 18,
            "애월읍": 19,
            "연동": 20,
            "오등동": 21,
            "오라이동": 22,
            "외도일동": 23,
            "용담삼동": 24,
            "용담이동": 25,
            "용담일동": 26,
            "우도면": 27,
            "이도이동": 28,
            "이호일동": 29,
            "조천읍": 30,
            "중문동": 31,
            "토평동": 32,
            "표선면": 33,
            "하예동": 34,
            "한림읍": 35,
            "호근동": 36,
        }
        month_mapping = {"August": 8, "September": 9, "October": 10}
        peak_mapping = {"비수기": 0, "성수기": 1}
        weekends_mapping = {"평일": 0, "주말": 1}
        review_group_mapping = {"500 미만": 0, "500 이상": 1}

        # 모델에 맞게 데이터 정제
        # ['person', 'level', 'score', 'city', 'city_details', 'peak', 'weekends']
        hotel_person = person_mapping[str(2 if input_headcount > 2 else 4) + "인"]
        hotel_level = random.randint(0, 10)
        hotel_score = 4.5
        hotel_city = city_mapping[input_city]
        hotel_city_details = city_details_mapping[input_district]
        hotel_peak = peak_mapping[is_peak_season(start_date)]
        hotel_weekends = weekends_mapping[is_weekend(start_date)]

        hotel_features = [
            hotel_person,
            hotel_level,
            hotel_score,
            hotel_city,
            hotel_city_details,
            hotel_peak,
            hotel_weekends,
        ]
        # hotel_predict = hotel_xgb_model.predict(np.array([hotel_features]))
        hotel_predict = [100000]
        print("hotel : ", hotel_predict)

        # 렌트카
        rent_xgb_model = rent_pkl

        rent_seater_mapping = {
            2: 0,
            4: 1,
            5: 2,
            6: 3,
            7: 4,
            8: 5,
            9: 6,
            11: 7,
            12: 8,
            15: 9,
        }
        rent_made_mapping = {"국산차": 0, "외제차": 1}
        rent_category_mapping = {
            "경차": 0,
            "대형SUV": 1,
            "대형차": 2,
            "소형SUV": 3,
            "소형차": 4,
            "스포츠카": 5,
            "승합차": 6,
            "준대형": 7,
            "준중형": 8,
            "중형SUV": 9,
            "중형차": 10,
        }
        rent_holiday_mapping = {"공휴일": 0, "주말": 1, "평일": 2}
        rent_day_mapping = {
            "금요일": 0,
            "목요일": 1,
            "수요일": 2,
            "월요일": 3,
            "일요일": 4,
            "토요일": 5,
            "화요일": 6,
        }
        rent_peak_season_mapping = {"비수기": 0, "성수기": 1}

        # 모델에 맞게 데이터 정제
        # ['seater', 'made', 'category', 'day', 'holiday', 'peak_season']

        rent_seater = rent_seater_mapping[5]
        rent_made = rent_made_mapping["국산차"]
        rent_category_before = random.choice(
            ["경차", "소형SUV", "소형차", "중형SUV", "중형차", "준중형"]
        )
        rent_category = rent_category_mapping[rent_category_before]
        rent_day = day_mapping[get_weekday(start_datetime)]
        rent_holiday = holiday_mapping[is_weekend_or_holiday(start_datetime)]
        rent_peak_season = peak_season_mapping[is_peak_season(start_date)]

        rent_features = [
            rent_seater,
            rent_made,
            rent_category,
            rent_day,
            rent_holiday,
            rent_peak_season,
        ]
        rent_predict = rent_xgb_model.predict(np.array([rent_features]))

        print(rent_predict)

        total_predict_price = (
            flight_start_predict + flight_end_predict
        ) * input_headcount
        total_predict_price += (hotel_predict + rent_predict) * travel_days

        if template_data == 0:
            print(input_start_time)
            flight_start_arrival_time = datetime.strptime(
                input_start_time, "%H:%M:%S"
            ) + timedelta(hours=1)
            flight_start_arrival_time = flight_start_arrival_time.strftime("%H:%M")

            flight_end_arrival_time = datetime.strptime(
                input_end_time, "%H:%M:%S"
            ) + timedelta(hours=1)
            flight_end_arrival_time = flight_end_arrival_time.strftime("%H:%M")

            template_data = {
                "hotel": {
                    "name": "모델이 예측한 호텔",
                    "price": format_number_with_won(hotel_predict[0]),
                    "score": 4.5,
                    "room_type": "모델이 예측한 방" + ", " + str((hotel_person + 1) * 2) + "인",
                    "location": input_location,
                },
                "flight_start": {
                    "airline": "AI항공",
                    "price": format_number_with_won(flight_start_predict[0]),
                    "departure_time": datetime.strptime(
                        input_start_time, "%H:%M:%S"
                    ).strftime("%H:%M"),
                    "arrival_time": flight_start_arrival_time,
                    "departure_place": input_airport,
                    "arrival_place": "CJU",
                    "date": input_start_date,
                },
                "flight_end": {
                    "airline": "AI항공",
                    "price": format_number_with_won(flight_end_predict[0]),
                    "departure_time": datetime.strptime(
                        input_end_time, "%H:%M:%S"
                    ).strftime("%H:%M"),
                    "arrival_time": flight_end_arrival_time,
                    "departure_place": "CJU",
                    "arrival_place": input_airport,
                    "date": input_end_date,
                },
                "car": {
                    "name": "모델이 예측한 렌트카",
                    "price": format_number_with_won(rent_predict[0]),
                    "category": rent_category_before + ", 5",
                    "label": random.choice(["자차미포함", "완전자차포함"]),
                },
                "total_price": {
                    "price": format_number_with_won(total_predict_price[0]),
                    "price_per_head": format_number_with_won(
                        total_predict_price[0] / input_headcount
                    ),
                },
            }

            return render_template("search2.html", data=template_data)
        template_data["total_price"]["predict"] = format_number_with_won(
            total_predict_price[0]
        )
        return render_template("search.html", data=template_data)
    else:  # GET
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0")
    # app.run(debug=True)
