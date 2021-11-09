# Email Configurations
# set the backend to the sendgrid to send the Mail
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
# Toggle sandbox mode (when running in DEBUG mode)
SENDGRID_SANDBOX_MODE_IN_DEBUG=False
# echo to stdout or any other file-like object that is passed to the backend via the stream kwarg.
SENDGRID_ECHO_TO_STDOUT=False
