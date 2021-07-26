import uuid
import datetime

from apps.notifications.tasks import save_notification_and_send_fcm_for_check


class QRCodeService:
    @staticmethod
    def generate_qr_code():
        unique_code = uuid.uuid4().int

        return unique_code

    @classmethod
    def update_user_data(cls, user):
        user.qr_code = cls.generate_qr_code()
        user.qr_code_updated_at = datetime.datetime.now()
        user.save(update_fields=['qr_code', 'qr_code_updated_at'])

        return user


class CheckNotificationService:
    @classmethod
    def send_notification(cls, check, user):
        body = {
            'object_id': check.id,
            'title': str(check.filial),
            'status': check.status,
            'accrued_point': check.accrued_point,
            'withdrawn_point': check.withdrawn_point,
        }
        save_notification_and_send_fcm_for_check(body, user, check)
