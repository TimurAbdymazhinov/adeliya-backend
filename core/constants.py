MALE = 'male'
FEMALE = 'female'

GENDER_TYPE = (
    (MALE, 'Мужской'),
    (FEMALE, 'Женский')
)

NEWS = 'news'
PROMOTION = 'promotion'

INFORMATION_TYPE = (
    (NEWS, 'Новость'),
    (PROMOTION, 'Акция'),
)

ACCRUED = 'accrued'
WITHDRAW = 'withdrawn'
ACCRUED_AND_WITHDRAW = 'accrued_and_withdrawn'

NOTIFICATION_TYPE = (
    (ACCRUED, 'Начислено бонусов'),
    (WITHDRAW, 'Снято бонусов'),
    (ACCRUED_AND_WITHDRAW, 'Начислено и снято'),
    (PROMOTION, 'Акции'),
    (NEWS, 'Новости')
)

CHECK_TYPE = (
    (ACCRUED, 'Начислено'),
    (WITHDRAW, 'Снято'),
    (ACCRUED_AND_WITHDRAW, 'Начислено и снято'),
)

DUE_DATE_CHECK_MESSAGE = 'У вас есть неоплаченный долг'

MONTH_NAMES = {
    '01': 'Январь',
    '02': 'Февраль',
    '03': 'Март',
    '04': 'Апрель',
    '05': 'Май',
    '06': 'Июнь',
    '07': 'Июль',
    '08': 'Август',
    '09': 'Сентябрь',
    '10': 'Октябрь',
    '11': 'Ноябрь',
    '12': 'Декабрь',
}

MONDAY = 1
TUESDAY = 2
WEDNESDAY = 3
THURSDAY = 4
FRIDAY = 5
SATURDAY = 6
SUNDAY = 7

WORK_DAYS = (
    (MONDAY, 'ПН'),
    (TUESDAY, 'ВТ'),
    (WEDNESDAY, 'СР'),
    (THURSDAY, 'ЧТ'),
    (FRIDAY, 'ПТ'),
    (SATURDAY, 'СБ'),
    (SUNDAY, 'ВС'),
)

WEEKDAY = {
    MONDAY: 'ПН',
    TUESDAY: 'ВТ',
    WEDNESDAY: 'СР',
    THURSDAY: 'ЧТ',
    FRIDAY: 'ПТ',
    SATURDAY: 'СБ',
    SUNDAY: 'ВС',
}
