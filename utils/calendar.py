from telegram_bot_calendar import DetailedTelegramCalendar

rus_months = ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"]
rus_days_of_week = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
cal_steps = {'y': 'год', 'm': 'месяц', 'd': 'день'}


class MyCalendar(DetailedTelegramCalendar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.days_of_week['my'] = rus_days_of_week
        self.months['my'] = rus_months
