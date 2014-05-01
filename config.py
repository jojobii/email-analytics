import argparse
parser = argparse.ArgumentParser(description="Performs data analytics on emails")

def str_lower(x):
	return x.lower()

# Words to exclude from "most common words" plot
EXCLUDE_WORDS = ['re:', 'fwd:', 'fw:', '-', ' ', '', 'the', 'be', 'to', 'of',
				'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not',
				'on', 'with', 'as', 'you', 'do', 'at', 'this', 'by', 'from',
				 'they', 'or', 'an', 'your', 'is', 'my', '&']
				 
#host name mapping to appropriate server, sent mail folder, and received mail folder
#format is hostname: [server, sent, inbox]
host_map =	{'gmail': ['imap.gmail.com', '[Gmail]/Sent Mail', 'INBOX'],
			'outlook': ['imap-mail.outlook.com', 'Sent Items', 'INBOX']}
			
host_choices = host_map.keys()
type_choices = ['sent','received']

parser.add_argument("username", help="User name")
parser.add_argument("password", help="Password")
parser.add_argument("-eh", "--emailhostname", help="Email host name (default=gmail)", default='gmail', type=str_lower, choices=host_choices)
parser.add_argument("-ef", "--emailfolder", help="Email folder (default=sent)", default='sent', type=str_lower, choices=type_choices)
parser.add_argument("-cu", "--customq", help="Use this to specify a custom host server AND mail folder if your host is not in the email host names above (separate by space)", type=str, nargs=2, metavar=('imap.gmail.com', 'INBOX'))
parser.add_argument("-nd", "--numdaysback", help="Number of days to go back (Leave out to use all emails)", type=int, metavar=30)
parser.add_argument("-ex", "--excludewords", help='Space separated list of additional words to exclude from the "common words" plots. The current list of excluded words is: ['+', '.join(EXCLUDE_WORDS)+']', type=str_lower, metavar=('foo', 'bar'), nargs='*')
args = parser.parse_args()
#if want to use dest= option for parser.add_argument to put directly into globals then call: globals().update(vars(args))

IMAP_USER = args.username
IMAP_PASS = args.password
EMAIL_HOST = args.emailhostname
MAIL_TO_ANALYSE = args.emailfolder
user_exclusions = args.excludewords
custom_host_folder = args.customq
NUM_DAYS = args.numdaysback # Number of days to go back. To view all emails, set to None. (will default to None unless argument is specified by user)
# Note that sometimes there are errors when the program tries to fetch too many emails
# Hence the need for a date restriction

#if user specified host and folder:
if custom_host_folder == None:
	#kludgey to get the right mail query string sent vs inbox
	IMAP_HOST, MAIL_STRING = [host_map[EMAIL_HOST][x] for x in [0]+[1 if MAIL_TO_ANALYSE == 'sent' else 2]]
else:
	IMAP_HOST, MAIL_STRING = custom_host_folder
	
if user_exclusions != None:
	EXCLUDE_WORDS = list(set(EXCLUDE_WORDS + user_exclusions))