# weather

Weather report bot using GitHub Actions

## Usage

Fork this repository, fill secrets in your own repository's setting page.

There several secret key you need to configure:

1. location: The location you concerns.
2. receiver: The email receiver.
3. sender: The email sender.
4. password: The email sender's password. 

Note that if you enabled 2FA for your sender account, the password may not be your login password.

And then, adjust the schedule cron in [python-app.yml](.github/workflows/python-app.yml).

## LICENSE

[MIT](LICENSE)
