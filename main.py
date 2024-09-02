import typer
import os
from registration import RegistrationService


def main(
    username: str = typer.Option(
        default=os.getenv("USERNAME", ""),
        prompt="Enter your username",
        hide_input=False,
    ),
    password: str = typer.Option(
        default=os.getenv("PASSWORD", ""), prompt="Enter your password", hide_input=True
    ),
    email_sender_address: str = typer.Option(
        default=os.getenv("SENDER_EMAIL", "jvtrueblood88@gmail.com"),
        prompt="Enter sender email address",
        hide_input=True,
    ),
    email_sender_password: str = typer.Option(
        default=os.getenv("SENDER_PASSWORD", ""),
        prompt="Enter sender email password",
        hide_input=True,
    ),
    email_notification_target_address: str = typer.Option(
        default=os.getenv("RECEIVER_EMAIL", "khush.jhug@gmail.com"),
        prompt="Where to send email notification?",
        hide_input=False,
    ),
):

    registration_service = RegistrationService(
        username, password, email_sender_address, email_sender_password
    )

    result = registration_service.headless_register(email_notification_target_address)


if __name__ == "__main__":
    if not (os.getenv("USERNAME") and os.getenv("PASSWORD")) and not os.getenv("DEBUG"):
        typer.echo(
            "Please set the USERNAME and PASSWORD environment variables or provide them as arguments."
        )
        raise typer.Abort()

    # Run the Typer application
    typer.run(main)
