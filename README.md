# WIP - Use with caution. You can delete your mails!

# check_email

#### Table of Contents

1. [About](#about)
2. [License](#license)
3. [Usage](#usage)
4. [Configuration](#configuration)
5. [Thanks](#thanks)
6. [Contributing](#contributing)

## About

*check_email* is a plugin to monitor email transmissions. It sends an email via SMTP to a
given email-address and evaluates the email receipt via IMAP. Furthermore *check_email* can
handle echo replies. An echo reply or in other name *echo-mail* will be sent from a mail
server, which received an email and responds to it. The last feature which *check_email* offers,
is a cleanup option. This allows to delete mails, which were sent by *check_email* or the *echo reply*.

## License

This plugin is licensed under the terms of the GNU General Public License Version 2, you will
find a copy of this license in the LICENSE file included in the source package.

## Usage

### Send an email and check for its delivery

In order to send an email to a given IMAP server and check for its delivery, you have to set the
required arguments *(see the example below)*. The plugin sends an email with an unique (hash) subject
and *X-Custom-Tag* via SMTP to the specified email-address. Afterwards the plugin connects via IMAP
to the given mail account and searches in the given mailbox for the email sent before. Dependent on
the thresholds, the plugin searches through the mailbox until the critical threshold is exceeded.<br>

**Required arguments:**<br>
      `--imap-host=[IMAP_HOST]`<br>
      `--imap-port=[IMAP_PORT]`<br>
      `--imap-user=[IMAP_USERNAME]`<br>
      `--imap-password=[IMAP_PASSWORD]`<br>
      `--smtp-host=[SMTP_HOST]`<br>
      `--smtp-port=[SMTP_PORT]`<br>
      `--sender=[SENDER_ADDRESS]`<br>
      `--receiver=[RECEIVER_ADDRESS]`<br>

**Optional arguments:**<br>
      `--smtp-user=[SMTP_USERNAME]`<br>
      `--smtp-password=[SMTP_PASSWORD]`<br>

**If not otherwise specified, the default values will be applied:**<br>
      `--imap-port=993`<br>
      `--imap-mailbox='INBOX'`<br>
      `--smtp-port=465`<br>
      `--critical=500`<br>
      `--warning=300`

### Check for echo replies

If the argument *--echo-reply* is set, the plugin assumes that an *echo-mail* will be send automatically
from a mail server, to inform the sender of the previous sent email that the email has been
delivered. Therefore, the plugin searches for this specified *echo-mail* in the mailbox of the
sender account via IMAP. Usually the *echo-mail* subject contains the same subject as the previous
sent email e.g.: “RE: Subject”
>NOTE: This *echo function* has to be configured on the mail server.

**Required arguments:**<br>
      `--echo-reply`<br>

**If not otherwise specified, the default values will be applied:**<br>
      `--imap-sender-host=[--smtp-host]`<br>
      `--imap-sender-port=993`<br>
      `--imap-sender-mailbox='INBOX'`<br>
      `--imap-sender-user=[--smtp-user]`<br>
      `--imap-sender-password=[--smtp-password]`<br>
      `--critical-reply=500`<br>
      `--warning-reply=300`

### Cleanup

In order to avoid a full mailbox of *echo-mails* and *check-mails*, there is an argument *--cleanup*
to delete *echo-mails* and *check-mails*.
>Use this option with caution, it could delete involuntary emails if the wrong *--imap-mailbox*,
>*--imap-sender-mailbox* or *--reply-name* is specified!

**Required arguments:**<br>
      `--cleanup`<br>
      `--reply-name=[REPLY_NAME]`<br>

**If not otherwise specified, the default values will be applied:**<br>
      `--cleanup-time=3600`

### Optional: environment variables

Check_email can gather these following environment variables from the system:

	export IMAP_USERNAME='username'
	export IMAP_PASSWORD='password'
	export SMTP_USERNAME='username'
	export SMTP_PASSWORD='password'
	export IMAP_SENDER_USERNAME='username'
	export IMAP_SENDER_PASSWORD='password'

>NOTE: It's currently not implemented to define more than one of each *SMTP*, *IMAP* and *IMAP_SENDER*

## Example - Send an email and check for its delivery (without cleanup)

	./check_mail.py \
			--smtp-host='mail.example.com' \
			--smtp-port=587 \
			--smtp-user='DOMAIN\User' \
			--smtp-password='***' \
			--sender='sender@example.com' \
			--imap-host='imap.example.com' \
			--imap-port=993 \
			--imap-user='receiver@example.de' \
			--imap-password='***' \
			--receiver='receiver@example.de' \
			--imap-mailbox='Monitoring' \
			--warning=300 \
			--critical=500

>1. The plugin connects to *mail<span>.example.com*, creates an unique hash subject and sends an email
>to *receiver<span>@example.com*
>2. The plugin connects to *imap<span>.example.com*, searches trough the mailbox *Monitoring*
>3. If the email cannot be found within 300 seconds, the return state will be WARNING
>4. After 500 seconds, the plugin will exit and return a CRITICAL

### Output - Send an email and check for its delivery (without cleanup)

	OK - check_email: imap.example.com - Email received in 3s | 'receive'=3

 >The email was found, and the plugin returns OK. Additionally, the duration how long this action took
 >will be served as *perfdata*.

## Example - Check for echo replies (with cleanup)

	./check_mail.py \
			--smtp-host='mail.example.com' \
			--smtp-port=587 \
			--smtp-user='DOMAIN\User' \
			--smtp-password='***' \
			--sender='sender@example.com' \
			--imap-host='imap.example.com' \
			--imap-port=993 \
			--imap-user='DOMAIN\User' \
			--imap-password='***'\
			--receiver='receiver@example.com' \
			--imap-mailbox='Monitoring' \
			--warning=300 \
			--critical=500 \
			--echo-reply \
			--imap-sender-host='imap.sender.example.com' \
			--imap-sender-port=993 \
			--imap-sender-user='DOMAIN\User' \
			--imap-sender-password='***' \
			--imap-sender-mailbox='Monitoring' \
			--reply-name='Echo Notify' \
			--warning-reply=300 \
			--critical-reply=500 \
			--cleanup \
			--cleanup-time=300

>1. The plugin connects to *mail<span>.example.com*, creates an unique hash subject and sends an email
>to *receiver<span>@example.com*.
>2. The plugin connects to *imap<span>.example.com*, searches trough the mailbox *Monitoring*. Additionally,
>emails with the *X-Custom-Tag* and if they are older then 300 seconds, will be deleted.
>3. If the email cannot be found within 300 seconds, the state will be WARNING
>4. After 500 seconds the plugin will exit and return a CRITICAL
>5. If the email was found, the plugin connects to *imap<span>.sender.example.com*
>6. The plugin selects the mailbox *Monitoring* and searches for the assumend *echo-mail*, which should
>contain **Echo Notify** in the subject. Additionally, old *echo-mails*  will be deleted (see 2.)
>7. If the *echo-mail* cannot be found within 300 seconds, the return state will be WARNING
>8. After 500 seconds, the plugin will exit and return a CRITICAL

### Output - Email loop example with cleanup

	OK - check_email: Email loop took 7s | 'receive'=3 'reply'=4 'loop'=7

>The *sent-mail* and *echo-mail* was found and the plugin returns OK. Additionally, the duration
>how long each action took will be served as *perfdata*.<br>

>NOTE: The output will be always the *highest* state, e.g.: *receive* is WARNING and *reply* is,
>the plugin output will be WARNING.

## Configuration

### Icinga 

**IMPORTANT**
`check_timeout` must be greater than the `critical threshold` otherwise the *default timeout* of a
plugin could be exceeded and Icinga kills its process. As a result, the plugin can never reach the
*critical* state. Moreover `check_interval` has also to be lower than the `check_timeout`. Due to
the fact, that the plugin *waits* for an email or rather an event, the execution time could be, in
the worst case, higher than the `check_interval`. In such circumstances Icinga triggers *check_email*
again, even if the plugin did not finish correctly.

>See *check_email.conf* for an example configuration

### Mail server
It is recommended to configure rules to manage emails from this plugin. By using a rule, any received
email message that match conditions specified in the rule can be automatically forwarded or redirected
to another mailbox (**of the same account!**). This is very useful, since the plugin searches through
a given mailbox. It could be a negative impact if the specified mailbox is filled up with other mails,
which are also be evaluated.

## Thanks

- Michael Friedrich
- Markus Frosch
- Markus Waldmüller

## Contributing

There are many ways to contribute to *check_email* -- whether it be sending patches, testing, reporting bugs,
or reviewing and updating the documentation. Every contribution is appreciated!
