import typer
import os
from registration import RegistrationService
import logging
from logger import setup_logging
import logging.config

setup_logging()

logger = logging.getLogger(__name__)

app = typer.Typer()


@app.command()
def main(
    username: str = typer.Option(
        help="Enter your username",
        hide_input=False,
    ),
    password: str = typer.Option(help="Enter your password", hide_input=True),
    cvv: str = typer.Option(help="Enter your CVV code", hide_input=True),
    email_sender_address: str = typer.Option(
        default="jvtrueblood88@gmail.com",
        help="Enter sender email address",
        hide_input=True,
    ),
    email_sender_password: str = typer.Option(
        help="Enter sender email password",
        hide_input=True,
    ),
    email_notification_target_address: str = typer.Option(
        default="khush.jhug@gmail.com",
        help="Where to send email notification?",
        hide_input=False,
    ),
    dry_run: str = typer.Option(
        "false",
        help="If 'true', the script will not perform any payment processing.",
    ),
    just_email: str = typer.Option(
        "false",
        help="If 'true', the script will only send an email.",
    ),
):
    dry_run = dry_run.lower() == "true"
    just_email = just_email.lower() == "true"

    registration_service = RegistrationService(
        username,
        password,
        email_sender_address,
        email_sender_password,
        is_dry_run=dry_run,
    )

    result = registration_service.headless_register(
        email_notification_target_address,
        just_email=just_email,
    )


if __name__ == "__main__":
    if not (os.getenv("USERNAME") and os.getenv("PASSWORD")) and not os.getenv("DEBUG"):
        typer.echo(
            "Please set the USERNAME and PASSWORD environment variables or provide them as arguments."
        )
        raise typer.Abort()
    logger.info("Starting registration process...")

    app()
