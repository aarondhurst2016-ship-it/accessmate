
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Example: Gmail, Outlook, Yahoo
PROVIDER_CONFIG = {
	'gmail': {
		'smtp': 'smtp.gmail.com',
		'imap': 'imap.gmail.com',
		'smtp_port': 587,
		'imap_port': 993
	},
	'outlook': {
		'smtp': 'smtp.office365.com',
		'imap': 'outlook.office365.com',
		'smtp_port': 587,
		'imap_port': 993
	},
	'yahoo': {
		'smtp': 'smtp.mail.yahoo.com',
		'imap': 'imap.mail.yahoo.com',
		'smtp_port': 587,
		'imap_port': 993
	}
}

def send_email(provider, username, password, to_addr, subject, body, attachments=None):
	import os
	cfg = PROVIDER_CONFIG[provider]
	msg = MIMEMultipart()
	msg['From'] = username
	msg['To'] = to_addr
	msg['Subject'] = subject
	msg.attach(MIMEText(body, 'plain'))
	# Attach files/images
	if attachments:
		from email.mime.base import MIMEBase
		from email import encoders
		for file_path in attachments:
			try:
				part = MIMEBase('application', 'octet-stream')
				with open(file_path, 'rb') as f:
					part.set_payload(f.read())
				encoders.encode_base64(part)
				part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
				msg.attach(part)
			except Exception as e:
				print(f"Attachment error: {e}")
	try:
		server = smtplib.SMTP(cfg['smtp'], cfg['smtp_port'])
		server.starttls()
		server.login(username, password)
		server.sendmail(username, to_addr, msg.as_string())
		server.quit()
		return True
	except Exception as e:
		print(f"Send email error: {e}")
		return False

def read_emails(provider, username, password, mailbox='INBOX', num=5, unread_only=False, important_only=False, search_sender=None, search_subject=None, search_date=None):
	import datetime
	cfg = PROVIDER_CONFIG[provider]
	try:
		mail = imaplib.IMAP4_SSL(cfg['imap'], cfg['imap_port'])
		mail.login(username, password)
		mail.select(mailbox)
		search_criteria = 'ALL'
		if unread_only:
			search_criteria = 'UNSEEN'
		typ, data = mail.search(None, search_criteria)
		mail_ids = data[0].split()[-num:]
		emails = []
		for i in mail_ids:
			typ, msg_data = mail.fetch(i, '(RFC822)')
			for response_part in msg_data:
				if isinstance(response_part, tuple):
					msg = email.message_from_bytes(response_part[1])
					subject = msg['subject']
					from_ = msg['from']
					date_ = msg['date'] if 'date' in msg else None
					body = ""
					if msg.is_multipart():
						for part in msg.walk():
							if part.get_content_type() == 'text/plain':
								body = part.get_payload(decode=True).decode()
								break
					else:
						body = msg.get_payload(decode=True).decode()
					# Filtering
					match = True
					if important_only:
						if not (subject and ("important" in subject.lower() or "urgent" in subject.lower())):
							match = False
					if search_sender and (not from_ or search_sender.lower() not in from_.lower()):
						match = False
					if search_subject and (not subject or search_subject.lower() not in subject.lower()):
						match = False
					if search_date and date_:
						try:
							# Try to parse date string
							email_date = None
							for fmt in ("%a, %d %b %Y", "%d %b %Y", "%Y-%m-%d", "%m/%d/%Y"):
								try:
									email_date = datetime.datetime.strptime(date_[:16], fmt).date()
									break
								except:
									continue
							if email_date:
								if '-' in search_date:
									target_date = datetime.datetime.strptime(search_date, '%Y-%m-%d').date()
								else:
									target_date = datetime.datetime.strptime(search_date, '%m/%d/%Y').date()
								if email_date != target_date:
									match = False
						except:
							pass
					if match:
						emails.append({'from': from_, 'subject': subject, 'body': body, 'date': date_})
		mail.logout()
		return emails
	except Exception as e:
		print(f"Read email error: {e}")
		return []
