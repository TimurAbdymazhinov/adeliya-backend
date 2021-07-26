import json

from django.core.serializers.json import DjangoJSONEncoder

from huey.contrib.djhuey import task, periodic_task, db_task
from huey import crontab
from loguru import logger

from apps.notifications.models import Notification
from apps.notifications.service import SendPushNotification
from core.constants import DUE_DATE_CHECK_MESSAGE


@task()
def save_notification_and_send_fcm_for_article(body, obj):
    from apps.account.models import User
    users_qs = User.objects.filter(is_registration_finish=True, is_active=True)
    for user in users_qs:
        notice_obj = Notification(
            user=user,
            notice_type=body['information_type'],
            linked_article=obj,
            body=json.dumps(body, cls=DjangoJSONEncoder),
        )
        badge_count = Notification.objects.filter(
            user=user, is_viewed=False
        ).count()
        SendPushNotification.send_fcm(user, notice_obj, body, badge_count)


@db_task(retries=5)
def create_notification_for_db(notice_obj):
    try:
        notice_obj.save()
    except Exception as e:
        logger.error('Didn\'t created notification')
        logger.exception(e)
    else:
        logger.success('Success create notification')


@task()
def save_notification_and_send_fcm_for_check(body, user, obj):
    notice_obj = Notification(
        user=user,
        notice_type=body['status'],
        linked_check=obj,
        body=json.dumps(body, cls=DjangoJSONEncoder)
    )
    if obj.is_on_credit:
        body['description'] = DUE_DATE_CHECK_MESSAGE
        notice_obj.is_on_credit = True

    else:
        body['description'] = f'{user.first_name}, {notice_obj.get_message}'

    notice_obj.body = json.dumps(body, cls=DjangoJSONEncoder)
    badge_count = Notification.objects.filter(
        user=user, is_viewed=False
    ).count()
    SendPushNotification.send_fcm(user, notice_obj, body, badge_count)


@periodic_task(crontab(hour='*/24'))
def send_notification_for_debtors():
    """Everyday sending push notification for debtor"""
    SendPushNotification.checking_debtors()


@task()
def send_notice_for_deleted_fcm_device(device, is_corporate_account):
    SendPushNotification.send_notice_for_delete(
        device, is_corporate_account
    )
