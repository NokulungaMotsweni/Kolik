from datetime import timedelta
from django.utils.timezone import now
from .models import IPAddressBan, AuditLog

class SecurityPolicy:
    """
    Security Policy for handling use and ip based login attempts.

    Constants:
    - MAX_LOGIN_ATTEMPTS_USER: Allowed failed attempts before cooldown/ban.
    - MAX_COOLDOWN_STRIKES: Number of cooldowns before permanent block.
    - USER_BAN_PERIOD: Duration of temporary user ban.
    - MAX_LOGIN_ATTEMPTS_IP: Failed IP login attempts before blocking IP.
    - IP_BAN_PERIOD: Duration of IP address block.
    - MAX_SIGNUP_ATTEMPTS_IP: Allowed IP login attempts before cooldown/ban.
    - SIGNUP_BAN_PERIOD: Duration of IP address block.
    """
    # User Based Login Attempts
    MAX_LOGIN_ATTEMPTS_USER = 5
    MAX_COOLDOWN_STRIKES = 3
    USER_BAN_PERIOD = timedelta(minutes=15)

    #IP Based Login Attempts
    MAX_LOGIN_ATTEMPTS_IP = 5
    IP_BAN_PERIOD = timedelta(minutes=30)

    # Sign Up Attempts
    MAX_SIGNUP_ATTEMPTS_IP = 5
    SIGNUP_BAN_PERIOD = timedelta(minutes=15)


    @staticmethod
    def handle_user_login_attempts(user, success):
        """
        Adds a login attempt for a user.

        Args:
            user: The user instance attempting to log in.
            success: Boolean indicating if login was successful.

        Returns:
            True if further login attempts are allowed, False if user is blocked.
        """
        now_time = now()

        # If the user is permanently blocked, deny further login attempts
        if user.is_blocked and (not user.cooldown_time_until or user.cooldown_until < now_time):
            return False


        if success:
            # Reset to default values on successful login; clear blocked status
            user.login_attempt_count = 0
            user.cooldown_strikes = 0
            user.is_blocked = False
            user.cooldown_until = None
        else:
            # On failed login, increment attempt login_attempt_count
            user.login_attempt_count += 1
            user.last_failed_login = now_time

            if user.login_attempt_count >= SecurityPolicy.MAX_LOGIN_ATTEMPTS_USER:
              # Reached max attempts; increase cooldown strikes
              user.login_attempt_count = 0
              user.cooldown_strikes += 1

              if user.cooldown_strikes >= SecurityPolicy.MAX_COOLDOWN_STRIKES:
                  # PERMANENT block of the user
                  user.is_blocked = True
                  user.cooldown_until = None
                  AuditLog.objects.create(
                      user=user,
                      action='user_permanently_blocked',
                      path='/login/',
                      ip_address=None,
                      status='FAILED',
                      device=''
                  )
              else:
                  # TEMPORARY block the user
                  user.is_blocked = True
                  user.cooldown_until = now_time + SecurityPolicy.USER_BAN_PERIOD
                  AuditLog.objects.create(
                      user=user,
                      action='user_temp_blocked',
                      path='/login/',
                      ip_address=None,
                      status='FAILED',
                      device=''
                  )

        user.save()
        return True

    @staticmethod
    def handle_ip(ip_address, success):
        """
        Adds a login attempt based on IP Address.

        Args:
            ip_address: The IP address attempting to log in.
            success: Boolean indicating if login was successful.

        Returns:
            True if further login attempts are allowed, False if IP Address is blocked.
        """
        now_time = now()
        ip_record, _ = IPAddressBan.objects.get_or_create(ip_address=ip_address)

        # If IP is currently blocked and still within block period
        if ip_record.is_blocked and ip_record.blocked_until and ip_record.blocked_until > now_time:
            return False

        if success:
            # On successful login, reset IP block information
            ip_record.login_attempt_count = 0
            ip_record.is_blocked = False
            ip_record.blocked_until = None
        else:
            # On failed login, increment IP attempt count
            ip_record.login_attempt_count += 1
            if ip_record.login_attempt_count >= SecurityPolicy.MAX_LOGIN_ATTEMPTS_IP:
                # Block the IP if too many failed attempts
                ip_record.is_blocked = True
                ip_record.blocked_until = now_time + SecurityPolicy.IP_BAN_PERIOD
                AuditLog.objects.create(
                    user=None,
                    action='ip_blocked',
                    path='/login/',
                    ip_address=ip_address,
                    status='FAILED',
                    device=''
                )
        ip_record.save()
        return True

    @staticmethod
    def handle_signup_ip(ip_address, success):

        """
        Handles and logs all user sign up attempts, updating IP-Based signup attempt records.

        Tracks the number of failed signup attempts from a given IP Address.
        Should the nuber of failed attempts exceed the allowed threshold, the IP is blocked for the specified duration.

        Args:
            ip_address: The IP Address attempting signup. Must have an `ip_address` attribute.
            success: True if the signup attempt succeeded, False otherwise.

        Returns:
            bool: False if the IP is currently blocked and the block period is still active.
                True otherwise (after updating attempt counters).
        """
        now_time = now()

        # Retrieve/Create an IPAddressBan record for the given IP address
        ip_record, _ = IPAddressBan.objects.get_or_create(ip_address=ip_address)

        # Deny signup if IP is currently blocked and still within the block duration
        if ip_record.is_blocked and ip_record.blocked_until and ip_record.blocked_until > now_time:
            return False

        if success:
            # Reset counters and unblock IP on successful signup
            ip_record.signup_attempt_count = 0
            ip_record.is_blocked = False
            ip_record.blocked_until = None
        else:
            # Increment failed signup attempt count and update the last attempt
            ip_record.signup_attempt_count += 1
            ip_record.last_attempt = now_time

            # Block IP if maximum failed attempts exceeded
            if ip_record.signup_attempt_count >= SecurityPolicy.MAX_SIGNUP_ATTEMPTS_IP:
                ip_record.is_blocked = True
                ip_record.blocked_until = now_time + SecurityPolicy.SIGNUP_BAN_PERIOD

                # Log the blocking event
                AuditLog.objects.create(
                    user=None,
                    action='ip_blocked_signup',
                    path='/register/',
                    ip_address=ip_address,
                    status='FAILED',
                    device=''
                )

            # Save the updated IP record
            ip_record.save()
            return True
