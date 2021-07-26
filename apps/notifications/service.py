import json
import datetime

from fcm_django.models import FCMDevice
from loguru import logger

from core.constants import DUE_DATE_CHECK_MESSAGE, MONTH_NAMES


class SendPushNotification:

    @classmethod
    def send_fcm(cls, user, notice_obj, body, badge_count):
        responses, full_notification, data = cls.message_generate(
            user, notice_obj, body, badge_count
        )
        try:
            for response in responses:
                if response.type and response.type == 'android':
                    response.send_message(data=data)
                else:
                    full_notification['click_action'] = notice_obj.notice_type
                    response.send_message(**full_notification)

            from apps.notifications.tasks import create_notification_for_db
            create_notification_for_db(notice_obj)

        except Exception as e:
            logger.error('Error on sending push notification to fcm service')
            logger.exception(e)
        else:
            logger.success('Success sending push notification')

    @classmethod
    def send_fcm_for_debtors(cls, user, notice_obj, body, badge_count):
        responses, full_notification, data = cls.message_generate(
            user, notice_obj, body, badge_count
        )
        data['body'] = body['description']
        full_notification['data'] = data
        try:
            for response in responses:
                if response.type and response.type == 'android':
                    response.send_message(data=data)
                else:
                    full_notification['click_action'] = notice_obj.notice_type
                    response.send_message(**full_notification)

        except Exception as e:
            logger.error('Error on sending push notification to fcm service')
            logger.exception(e)
        else:
            logger.success('Success sending push notification')

    @staticmethod
    def set_notification_viewed_for_check(request, obj):
        user = request.user
        if user.is_authenticated:
            from apps.notifications.models import Notification
            notices = (
                Notification.objects.filter(
                    user=user, linked_check_id=obj.id, is_viewed=False
                )
            )
            notices.update(is_viewed=True)

    @staticmethod
    def set_notification_viewed_for_article(request, obj):
        user = request.user
        if user.is_authenticated:
            from apps.notifications.models import Notification
            notice = (
                Notification.objects.filter(
                    user=user, linked_article_id=obj.id
                ).first()
            )
            if notice and not notice.is_viewed:
                notice.is_viewed = True
                notice.save(update_fields=['is_viewed'])

    @classmethod
    def checking_debtors(cls):
        from apps.check.models import Check
        from apps.notifications.models import Notification

        checks = (
            Check.objects.filter(
                is_on_credit=True,
                due_date__date=datetime.datetime.now() + datetime.timedelta(
                    days=3)
            ).select_related('user')
        )
        for check in checks:
            body = {
                'object_id': check.id,
                'title': str(check.filial),
                'status': check.status,
                'accrued_point': check.accrued_point,
                'withdrawn_point': check.withdrawn_point,
                'description': DUE_DATE_CHECK_MESSAGE,
            }
            notice_obj = cls.save_notification_for_debtor(check, body)
            badge_count = Notification.objects.filter(
                user=check.user, is_viewed=False
            ).count()
            cls.send_fcm_for_debtors(check.user, notice_obj, body, badge_count)

    @staticmethod
    def save_notification_for_debtor(check, body):
        from apps.notifications.models import Notification
        from django.core.serializers.json import DjangoJSONEncoder

        notice_obj = Notification.objects.create(
            user=check.user,
            notice_type=check.status,
            linked_check=check,
            body=json.dumps(body, cls=DjangoJSONEncoder),
            is_on_credit=True,
        )
        return notice_obj

    @staticmethod
    def message_generate(user, notice_obj, body, badge_count):
        responses = FCMDevice.objects.filter(user=user, active=True)
        data_msg = dict(
            title=notice_obj.NOTIFICATION_TITLE,
            body=notice_obj.get_message,
            click_action=notice_obj.notice_type,
            id=body['object_id'],
            type=notice_obj.notice_type,
            badge_count=badge_count,
        )
        full_notification = {
            'data': data_msg, 'title': notice_obj.NOTIFICATION_TITLE,
            'body': notice_obj.get_message,
            'sound': "default",
        }
        return responses, full_notification, data_msg

    @classmethod
    def send_notice_for_delete(cls, devices, is_corporate_account) -> None:
        data = dict(
            title='TruckParts',
            body='Вы зашли с другого устройства!',
            click_action='TruckPartsKick',
            id=6699,  # not necessarily
            is_kicked=True,
        )
        full_notification = {
            'data': data, 'title': 'TruckParts',
            'body': 'Вы зашли с другого устройства!',
            'sound': "default",
        }
        if is_corporate_account:
            device = devices.last()
            cls.send_kick_notice(device, data)
        else:
            for device in devices:
                cls.send_kick_notice(device, data, full_notification)

    @staticmethod
    def send_kick_notice(device, data, full_notification=None):
        try:
            if device.type and device.type == 'android':
                device.send_message(data=data)
            else:
                device.send_message(**full_notification)
        except Exception as e:
            logger.error('Error on sending push notification to fcm service')
            logger.exception(e)
            device.delete()
        else:
            logger.success('Success sending push notification')
            device.delete()


class NotificationResponseService:
    @classmethod
    def reformat(cls, notifications):
        notification_list = []
        month_list = []

        last_month = None
        last_year = None

        if len(notifications) == 0:
            return notification_list

        for notification in notifications:
            notification_date = notification['created_at'].split('T')[0]
            year, month, _ = notification_date.split('-')

            if last_month == month and last_year == year:
                month_list['notifications'].append(notification)
            else:
                if month_list:
                    notification_list.append(month_list)
                month_list = {
                    'month': cls.get_month_name(month), 'year': year,
                    'notifications': [notification]
                }
            last_month, last_year = month, year

        notification_list.append(month_list)

        return notification_list

    @staticmethod
    def get_month_name(month_number):
        return MONTH_NAMES.get(month_number)
