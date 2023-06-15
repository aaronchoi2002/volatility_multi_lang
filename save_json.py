import json

# Your JSON data
data_en = {
    "title": "Volatility Dashboard",
    "enter_stock_code": "Enter the stock code:",
    "enter_period": "Enter the period for the rolling:",
    "enter_volatility_days": "Enter the number of days volatility:",
    "avg_volatility_higher_or_lower": "Average volatility Higher/Low than pervious (%):",
    "Multipage_Volatility_Dashboard": "Multipage Volatility Dashboard",
    "refresh": "Refresh",
    "no_data_error": "No data found for",
    "price": "Price",
    "last_update_time": "Last update time",
    "today_volatility": "Today Volatility",
    "x_day_volatility": "{}-Day Volatility",
    "weekly_volatility": "Weekly Volatility",
    "today_range": "Today Range",
    "day_high": "Day high",
    "day_low": "Day low",  
    "std_deviation_1": "1 Std Deviation",
    "previous_day_volatility": "Previous day volatility",
    "std_deviation_2": "2 Std Deviation",
    "average_volatility": f"Average volatility",
    "std_deviation_3": "3 Std Deviation",
    "std_deviation_of_volatility": "Std Deviation of volatility",
    "previous_day": "Previous day",
    "sell": "Sell",
    "previous_day_volatility": "Previous day volatility",
    "is_higher_than": "is higher than",
    "average_volatility": "average volatility",
    "buy": "Buy",
    "is_lower_than": "is lower than",
    "download_csv": "Download data as CSV",
    "x_day_volatility": "{}-Day Volatility",
    "avg_x_day_volatility": "Average {}-Day Volatility",
    "std_x_day_volatility": "Std Deviation of {}-Day Volatility",
    "x_day_volatility_pct": "{}-Day Volatility (%)",
    "avg_x_day_volatility_pct": "Average {}-Day Volatility (%)",
    "std_x_day_volatility_pct": "Std Deviation of {}-Day Volatility (%)",
    "download_csv_pct": "Download data as CSV (in %)",
    "previous_x_day_volatility": "Previous {}-Day Volatility",
    "previous_x_day": "Previous {}-Day",
    "x_day": "{}-Day range",
    "x_day_high": "{}-Day High",
    "x_day_low": "{}-Day Low",
    "week_high": "Week High",
    "week_low": "Week Low",
    "week_range": "Week Range",
    "previous_week": "Previous Week",
    "previous_week_volatility": "Previous Week Volatility",
}


data_zh_Hant = {
    "title": "波動性儀表板",
    "enter_stock_code": "輸入股票代碼：",
    "enter_period": "輸入滾動的期間：",
    "enter_volatility_days": "輸入波動性的天數：",
    "avg_volatility_higher_or_lower": "平均波動性高於/低於之前（％）：",
    "Multipage_Volatility_Dashboard": "多頁波動性儀表板",
    "refresh": "更新",
    "no_data_error": "找不到數據：",
    "price": "價格",
    "last_update_time": "最後更新時間",
    "today_volatility": "今日波動性",
    "x_day_volatility": "{}天波動性",
    "weekly_volatility": "週波動性",
    "today_range": "今日範圍",
    "day_high": "日高",
    "day_low": "日低",
    "std_deviation_1": "1標準差",
    "previous_day_volatility": "前一日的波動性",
    "std_deviation_2": "2標準差",
    "average_volatility": f"平均波動性",
    "std_deviation_3": "3標準差",
    "std_deviation_of_volatility": "波動性的標準差",
    "previous_day": "前一天",
    "sell": "賣出",
    "previous_day_volatility": "前一日的波動性",
    "is_higher_than": "高於",
    "average_volatility": "平均波動性",
    "buy": "購買",
    "is_lower_than": "低於",
    "download_csv": "下載數據為CSV",
    "x_day_volatility": "{}天波動性",
    "avg_x_day_volatility": "平均{}天波動性",
    "std_x_day_volatility": "{}天波動性的標準差",
    "x_day_volatility_pct": "{}天波動性（％）",
    "avg_x_day_volatility_pct": "平均{}天波動性（％）",
    "std_x_day_volatility_pct": "{}天波動性的標準差（％）",
    "download_csv_pct": "下載數據為CSV（％）",
    "previous_x_day_volatility": "前{}日的波動性",
    "previous_x_day": "前{}天",
    "x_day": "{}天範圍",
    "x_day_high": "{}天高",
    "x_day_low": "{}天低",
    "week_high": "週高",
    "week_low": "週低",
    "week_range": "週範圍",
    "previous_week": "上週",
    "previous_week_volatility": "上週波動性",



}

data_sh_Hans = {
    "title": "波动性仪表板",
    "enter_stock_code": "输入股票代码：",
    "enter_period": "输入滚动的期间：",
    "enter_volatility_days": "输入波动性的天数：",
    "avg_volatility_higher_or_lower": "平均波动性高于/低于之前（％）：",
    "Multipage_Volatility_Dashboard": "多页波动性仪表板",
    "refresh": "刷新",
    "no_data_error": "找不到数据：",
    "price": "价格",
    "last_update_time": "最后更新时间",
    "today_volatility": "今日波动性",
    "x_day_volatility": "{}天波动性",
    "weekly_volatility": "周波动性",
    "today_range": "今日範圍",
    "day_high": "日高",
    "day_low": "日低",
    "today_range": "今日范围",
    "day_high": "日高",
    "day_low": "日低",
    "std_deviation_1": "1标准差",
    "previous_day_volatility": "前一日的波动性",
    "std_deviation_2": "2标准差",
    "average_volatility": f"平均波动性",
    "std_deviation_3": "3标准差",
    "std_deviation_of_volatility": "波动性的标准差",
    "previous_day": "前一天",
    "sell": "卖出",
    "previous_day_volatility": "前一日的波动性",
    "is_higher_than": "高于",
    "average_volatility": "平均波动性",
    "buy": "购买",
    "is_lower_than": "低于",
    "download_csv": "下载数据为CSV",
    "x_day_volatility": "{}天波动性",
    "avg_x_day_volatility": "平均{}天波动性",
    "std_x_day_volatility": "{}天波动性的标准差",
    "x_day_volatility_pct": "{}天波动性（％）",
    "avg_x_day_volatility_pct": "平均{}天波动性（％）",
    "std_x_day_volatility_pct": "{}天波动性的标准差（％）",
    "download_csv_pct": "下载数据为CSV（％）",
    "previous_x_day_volatility": "前{}日的波动性",
    "previous_x_day": "前{}天",
    "x_day": "{}天范围",
    "x_day_high": "{}天高",
    "x_day_low": "{}天低",
    "week_high": "周高",
    "week_low": "周低",
    "week_range": "周范围",
    "previous_week": "上周",
    "previous_week_volatility": "上周波动性",


}

# Write English data to a file
with open('en.json', 'w', encoding='utf8') as file:
    json.dump(data_en, file, ensure_ascii=False)

# Write Traditional Chinese data to a file
with open('zh_Hant.json', 'w', encoding='utf8') as file:
    json.dump(data_zh_Hant, file, ensure_ascii=False)

# Write Simplified Chinese data to a file
with open('sh_Hans.json', 'w', encoding='utf8') as file:
    json.dump(data_sh_Hans, file, ensure_ascii=False)

def update_json(filename, new_data):
    # Read existing data
    with open(filename, 'r', encoding='utf8') as file:
        data = json.load(file)
        
    # Update data
    data.update(new_data)

    # Write updated data back to file
    with open(filename, 'w', encoding='utf8') as file:
        json.dump(data, file, ensure_ascii=False)

# Update English data
update_json('en.json', data_en)

# Update Traditional Chinese data
update_json('zh_Hant.json', data_zh_Hant)

# Update Simplified Chinese data
update_json('sh_Hans.json', data_sh_Hans)
