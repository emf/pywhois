# parser.py - Module for parsing whois response data
# Copyright (c) 2008 Andrey Petrov
#
# This module is part of pywhois and is released under
# the MIT license: http://www.opensource.org/licenses/mit-license.php

import re
import time
   

class PywhoisError(Exception):
    pass


def cast_date(date_str):
    """Convert any date string found in WHOIS to a time object.
    """
    known_formats = [
        '%d-%b-%Y', 				# 02-jan-2000
        '%Y-%m-%d', 				# 2000-01-02
        '%Y.%m.%d %H:%M:%S',        # 2006.06.12 15:53:14 (.pl)
        '%Y.%m.%d',                 # 2002.12.25 (.ru)
	'%Y-%b-%d',                 # 2008-Feb-5 (.nu)
        '%d.%m.%Y %H:%M:%S',        # 18.05.2004 18:15:00 (.cz)
        '%d.%m.%Y',                 # 21.5.1998 (.fi)
        '%d-%b-%Y %H:%M:%S %Z',     # 24-Jul-2009 13:20:03 UTC
        '%Y-%m-%d %H:%M',           # 2000-03-07 00:00 (.cn)
        '%a %b %d %H:%M:%S %Z %Y',  # Tue Jun 21 23:59:59 GMT 2011
	'%d %b %Y %H:%M %Z',        # 31 Dec 1999 05:00 PST (.fm)
        '%Y-%m-%dT%H:%M:%S',        # 2007-01-26T19:10:31
        '%Y%m%d%H%M%S',             # 20110209194637 (.ua)
        '%Y%m%d',                   # 20020702 (isoc.org.il)
        '%m/%d/%Y',                 # 05/14/2002
        '%d/%m/%Y',                 # 13/09/2004 (.fr)
        '%Y/%m/%d',                 # 2004/10/14 (.jp)
        '%Y. %m. %d.'               # 2007. 04. 23. (.kr)
    ]

    for format in known_formats:
        try:
            return time.strptime(date_str.strip(), format)
        except ValueError, e:
            pass # Wrong format, keep trying
    return None


class WhoisEntry(object):
    """Base class for parsing a Whois entries.
    """
    # regular expressions to extract domain data from whois profile
    # child classes will override this
    _regex = {
        'domain_name':      'Domain Name:\s?(.+)',
        'registrar':        'Registrar:\s?(.+)',
        'whois_server':     'Whois Server:\s?(.+)',
        'referral_url':     'Referral URL:\s?(.+)', # http url of whois_server
        'updated_date':     'Updated Date:\s?(.+)',
        'creation_date':    'Creation Date:\s?(.+)',
        'expiration_date':  'Expiration Date:\s?(.+)',
        'name_servers':     'Name Server:\s?(.+)', # list of name servers
        'status':           'Status:\s?(.+)', # list of statuses
        'emails':           '[\w.-]+@[\w.-]+\.[\w]{2,4}', # list of email addresses
    }

    def __init__(self, domain, text, regex=None):
        self.domain = domain
        self.text = text
        if regex is not None:
            self._regex = regex


    def __getattr__(self, attr):
        """The first time an attribute is called it will be calculated here.
        The attribute is then set to be accessed directly by subsequent calls.
        """
        whois_regex = self._regex.get(attr)
        if whois_regex:
            setattr(self, attr, re.findall(whois_regex, self.text))
            return getattr(self, attr)
        else:
            raise KeyError('Unknown attribute: %s' % attr)

    def __str__(self):
        """Print all whois properties of domain
        """
        return '\n'.join('%s: %s' % (attr, str(getattr(self, attr))) for attr in self.attrs())


    def attrs(self):
        """Return list of attributes that can be extracted for this domain
        """
        return sorted(self._regex.keys())


    @staticmethod
    def load(domain, text):
        """Given whois output in ``text``, return an instance of ``WhoisEntry`` that represents its parsed contents.
        """
        if text.strip() == 'No whois server is known for this kind of object.':
            raise PywhoisError(text)

        if    '.com' == domain[-4:]:
            return WhoisCom(domain, text)
        elif  '.net' == domain[-4:]:
            return WhoisNet(domain, text)
        elif  '.org' == domain[-4:]:
            return WhoisOrg(domain, text)
        elif   '.au' == domain[-3:]:
            return WhoisAu(domain, text)
        elif  '.biz' == domain[-4:]:
            return WhoisBiz(domain, text)
        elif   '.ca' == domain[-3:]:
            return WhoisCa(domain, text)
        elif   '.cn' == domain[-3:]:
            return WhoisCn(domain, text)
        elif   '.co' == domain[-3:]:
            return WhoisCo(domain, text)
        elif   '.cz' == domain[-3:]:
            return WhoisCz(domain, text)
        elif   '.de' == domain[-3:]:
            return WhoisDe(domain, text)
        elif   '.dk' == domain[-3:]:
            return WhoisDk(domain, text)
        elif   '.fi' == domain[-3:]:
            return WhoisFi(domain, text)
        elif   '.fm' == domain[-3:]:
            return WhoisFm(domain, text)
        elif   '.fr' == domain[-3:]:
            return WhoisFr(domain, text)
        elif   '.il' == domain[-3:]:
            return WhoisIl(domain, text)
        elif '.info' == domain[-5:]:
            return WhoisInfo(domain, text)
        elif   '.jp' == domain[-3:]:
            return WhoisJp(domain, text)
        elif   '.kr' == domain[-3:]:
            return WhoisKr(domain, text)
        elif   '.me' == domain[-3:]:
        	return WhoisMe(domain, text)
        elif '.name' == domain[-5:]:
            return WhoisName(domain, text)
        elif   '.no' == domain[-3:]:
            return WhoisNo(domain, text)
        elif   '.nu' == domain[-3:]:
            return WhoisNu(domain, text)
        elif   '.pl' == domain[-3:]:
            return WhoisPl(domain, text)
        elif   '.tk' == domain[-3:]:
            return WhoisTk(domain, text)
        elif   '.tw' == domain[-3:]:
            return WhoisTw(domain, text)
        elif   '.ru' == domain[-3:]:
            return WhoisRu(domain, text)
        elif   '.sk' == domain[-3:]:
            return WhoisSk(domain, text)
        elif   '.su' == domain[-3:]:
            return WhoisSu(domain, text)
        elif   '.ua' == domain[-3:]:
            return WhoisUa(domain, text)
        elif   '.uk' == domain[-3:]:
        	return WhoisUk(domain, text)
        elif   '.us' == domain[-3:]:
            return WhoisUs(domain, text)
        else:
            return WhoisEntry(domain, text)



class WhoisCom(WhoisEntry):
    """Whois parser for .com domains
    """
    def __init__(self, domain, text):
        if 'No match for "' in text:
            raise PywhoisError(text)
        else:
            WhoisEntry.__init__(self, domain, text) 

class WhoisNet(WhoisEntry):
    """Whois parser for .net domains
    """
    def __init__(self, domain, text):
        if 'No match for "' in text:
            raise PywhoisError(text)
        else:
            WhoisEntry.__init__(self, domain, text) 

class WhoisOrg(WhoisEntry):
    """Whois parser for .org domains
    """
    regex = {
        'domain_name':                    'Domain Name:\s*(.+)',
        'creation_date':                  'Created On:\s*(.+)',
        'expiration_date':                'Expiration Date:\s*(.+)',
        'updated_date':                   'Last Updated On:\s*(.+)',
        'domain_id':                      'Domain ID:\s*(.+)',
        'registrar':                      'Sponsoring Registrar:\s*(.+)',
        'status':                         'Status:\s*(.+)',  # list of statuses
        'registrant_id':                  'Registrant ID:\s*(.+)',
        'registrant_organization':        'Registrant Organization:\s*(.+)',
        'registrant_name':                'Registrant Name:\s*(.+)',
        'registrant_address1':            'Registrant Street1:\s*(.+)',
        'registrant_address2':            'Registrant Street2:\s*(.+)',
        'registrant_city':                'Registrant City:\s*(.+)',
        'registrant_state_province':      'Registrant State/Province:\s*(.+)',
        'registrant_postal_code':         'Registrant Postal Code:\s*(.+)',
        'registrant_country':             'Registrant Country:\s*(.+)',
        'registrant_phone_number':        'Registrant Phone:\s*(.+)',
        'registrant_email':               'Registrant Email:\s*(.+)',
        'admin_id':                       'Admin ID:\s*(.+)',
        'admin_name':                     'Admin Name:\s*(.+)',
        'admin_organization':             'Admin Organization:\s*(.+)',
        'admin_address1':                 'Admin Street1:\s*(.+)',
        'admin_address2':                 'Admin Street2:\s*(.+)',
        'admin_city':                     'Admin City:\s*(.+)',
        'admin_state_province':           'Admin State/Province:\s*(.+)',
        'admin_postal_code':              'Admin Postal Code:\s*(.+)',
        'admin_country':                  'Admin Country:\s*(.+)',
        'admin_phone_number':             'Admin Phone:\s*(.+)',
        'admin_email':                    'Admin Email:\s*(.+)',
        'tech_id':                        'Tech ID:\s*(.+)',
        'tech_name':                      'Tech Name:\s*(.+)',
        'tech_organization':              'Tech Organization:\s*(.+)',
        'tech_address1':                  'Tech Street1:\s*(.+)',
        'tech_address2':                  'Tech Street2:\s*(.+)',
        'tech_city':                      'Tech City:\s*(.+)',
        'tech_state_province':            'Tech State/Province:\s*(.+)',
        'tech_postal_code':               'Tech Postal Code:\s*(.+)',
        'tech_country':                   'Tech Country:\s*(.+)',
        'tech_country_code':              'Tech Country Code:\s*(.+)',
        'tech_phone_number':              'Tech Phone Number:\s*(.+)',
        'tech_email':                     'Tech Email:\s*(.+)',
        'name_servers':                   'Name Server:\s*(.+)',  # list of name servers
	}
    def __init__(self, domain, text):
        if text.strip() == 'NOT FOUND':
            raise PywhoisError(text)
        else:
            WhoisEntry.__init__(self, domain, text, self.regex)

class WhoisAu(WhoisEntry):
    """Whois parser for .au domains (throw another domain on the barbie, mate)"""
    regex = {
        'domain_name':             'Domain Name:\s*(.+)',
        'registrar':               'Registrar Name:\s*(.+)',
        'registrar_id':            'Registrar ID:\s*(.+)',
        'registrant_name':         'Registrant Name:\s*(.+)',
        'registrant_id':           'Registrant ID:\s*(.+)',
        'updated_date':            'Last Modified:\s*(.+)',
        'name_servers':            'Name Server:\s*(.+)',  # list of name servers
        'status':                  'Status:\s*(.+)',  # list of statuses
    }
    def __init__(self, domain, text):
        if text.strip() == 'No Data Found':
            raise PywhoisError(text)
        else:
            WhoisEntry.__init__(self, domain, text, self.regex)

class WhoisBiz(WhoisEntry):
    """Whois parser for .biz domains.  really. .biz?  i hate the internet."""
    regex = {
        'domain_name':                    'Domain Name:\s*(.+)',
        'creation_date':                  'Domain Registration Date:\s*(.+)',
        'expiration_date':                'Domain Expiration Date:\s*(.+)',
        'updated_date':                   'Domain Last Updated Date:\s*(.+)',
        'domain_id':                      'Domain ID:\s*(.+)',
        'registrar':                      'Sponsoring Registrar:\s*(.+)',
        'status':                         'Domain Status:\s*(.+)',  # list of statuses
        'registrant_id':                  'Registrant ID:\s*(.+)',
        'registrant_name':                'Registrant Name:\s*(.+)',
        'registrant_address1':            'Registrant Address1:\s*(.+)',
        'registrant_city':                'Registrant City:\s*(.+)',
        'registrant_state_province':      'Registrant State/Province:\s*(.+)',
        'registrant_postal_code':         'Registrant Postal Code:\s*(.+)',
        'registrant_country':             'Registrant Country:\s*(.+)',
        'registrant_country_code':        'Registrant Country Code:\s*(.+)',
        'registrant_phone_number':        'Registrant Phone:\s*(.+)',
        'registrant_email':               'Registrant Email:\s*(.+)',
        'admin_id':                       'Administrative Contact ID:\s*(.+)',
        'admin_name':                     'Administrative Contact Name:\s*(.+)',
        'admin_address1':                 'Administrative Contact Address1:\s*(.+)',
        'admin_city':                     'Administrative Contact City:\s*(.+)',
        'admin_state_province':           'Administrative Contact State/Province:\s*(.+)',
        'admin_postal_code':              'Administrative Contact Postal Code:\s*(.+)',
        'admin_country':                  'Administrative Contact Country:\s*(.+)',
        'admin_country_code':             'Administrative Contact Country Code:\s*(.+)',
        'admin_phone_number':             'Administrative Contact Phone:\s*(.+)',
        'admin_email':                    'Administrative Contact Email:\s*(.+)',
        'billing_id':                     'Billing Contact ID:\s*(.+)',
        'billing_name':                   'Billing Contact Name:\s*(.+)',
        'billing_address1':               'Billing Contact Address1:\s*(.+)',
        'billing_city':                   'Billing Contact City:\s*(.+)',
        'billing_state_province':         'Billing Contact State/Province:\s*(.+)',
        'billing_postal_code':            'Billing Contact Postal Code:\s*(.+)',
        'billing_country':                'Billing Contact Country:\s*(.+)',
        'billing_country_code':           'Billing Contact Country Code:\s*(.+)',
        'billing_phone_number':           'Billing Contact Phone:\s*(.+)',
        'billing_email':                  'Billing Contact Email:\s*(.+)',
        'tech_id':                        'Technical Contact ID:\s*(.+)',
        'tech_name':                      'Technical Contact Name:\s*(.+)',
        'tech_address1':                  'Technical Contact Address1:\s*(.+)',
        'tech_city':                      'Technical Contact City:\s*(.+)',
        'tech_state_province':            'Technical Contact State/Province:\s*(.+)',
        'tech_postal_code':               'Technical Contact Postal Code:\s*(.+)',
        'tech_country':                   'Technical Contact Country:\s*(.+)',
        'tech_country_code':              'Technical Contact Country Code:\s*(.+)',
        'tech_phone_number':              'Technical Contact Phone:\s*(.+)',
        'tech_email':                     'Technical Contact Email:\s*(.+)',
        'name_servers':                   'Name Server:\s*(.+)',  # list of name servers
	}
    def __init__(self, domain, text):
        if 'Not found:' in text:
            raise PywhoisError(text)
        else:
            WhoisEntry.__init__(self, domain, text, self.regex)

class WhoisCa(WhoisEntry):
    """Whois parser for .ca domains (canada)"""
    regex = {
        'domain_name':             'Domain name:\s*(.+)',
        'creation_date':           'Creation date:\s*(.+)',
        'updated_date':            'Updated date:\s*(.+)',
        'expiration_date':         'Expiry Date:\s*(.+)',
        'name_servers':            'Name servers:\r?\n\s*(.+)',  # list of name servers
        'status':                  'Domain status:\s*(.+)',  # list of statuses
        'emails': '[\w.-]+@[\w.-]+\.[\w]{2,4}',  # list of email addresses
    }
    def __init__(self, domain, text):
            WhoisEntry.__init__(self, domain, text, self.regex)

class WhoisCn(WhoisEntry):
    """Whois parser for .cn domains (china)"""
    regex = {
        'domain_name':             'Domain Name:\s*(.+)',
        'registrar':               'Sponsoring Registrar:\s*(.+)',
        'registrant_organization': 'Registrant Organization:\s*(.+)',
        'registrant_name':         'Registrant Name:\s*(.+)',
        'creation_date':           'Registration Date:\s*(.+)',
        'expiration_date':         'Expiration Date:\s*(.+)',
        'name_servers':            'Name Server:\s*(.+)',  # list of name servers
        'status':                  'Domain Status:\s*(.+)',  # list of statuses
        'emails': '[\w.-]+@[\w.-]+\.[\w]{2,4}',  # list of email addresses
    }
    def __init__(self, domain, text):
        if 'no matching record' in text:
            raise PywhoisError(text)
        else:
            WhoisEntry.__init__(self, domain, text, self.regex)

class WhoisCo(WhoisBiz):
    """whois parser for .co, identical to .biz"""
    pass

class WhoisCz(WhoisEntry):
    """Whois parser for .cz domains """
    regex = {
        'domain_name':     'domain:\s*(.+)',
        'creation_date':   'registered:\s*(.+)',
        'updated_date':    'changed:\s*(.+)',
        'expiration_date': 'expire:\s*(.+)',
        'name_servers':    'nserver:\s*(.+)',  # list of name servers
    }
    def __init__(self, domain, text):
        if 'No entries found' in text:
            raise PywhoisError(text)
        else:
            WhoisEntry.__init__(self, domain, text, self.regex)

class WhoisDe(WhoisEntry):
    """Whois parser for .de domains (germany)"""
    regex = {
        'domain_name':     'Domain:\s*(.+)',
        #'creation_date':   'created:\s*(.+)',
        'updated_date':    'Changed:\s*(.+)',
        'name_servers':    'Nserver:\s*(.+)',  # list of name servers
        'status':          'Status:\s*(.+)',  # list of statuses
        'emails': '[\w.-]+@[\w.-]+\.[\w]{2,4}',  # list of email addresses
    }
    def __init__(self, domain, text):
        if 'Status: free' in text or 'Error' in text:
            raise PywhoisError(text)
        else:
            WhoisEntry.__init__(self, domain, text, self.regex)

class WhoisDk(WhoisEntry):
    """Whois parser for .dk domains (denmark)"""
    regex = {
        'domain_name':     'Domain:\s*(.+)',
        'creation_date':   'Registered:\s*(.+)',
        'expiration_date': 'Expires:\s*(.+)',
        'name_servers':    'Hostname:\s*(.+)',  # list of name servers
        'status':          'Status:\s*(.+)',  # list of statuses
    }
    def __init__(self, domain, text):
        if 'No entries found' in text:
            raise PywhoisError(text)
        else:
            WhoisEntry.__init__(self, domain, text, self.regex)

class WhoisFi(WhoisEntry):
    """Whois parser for .fi domains (finland)"""
    regex = {
        'domain_name':     'domain:\s*(.+)',
        'creation_date':   'created:\s*(.+)',
        'expiration_date': 'expires:\s*(.+)',
        'name_servers':    'nserver:\s*(.+) ',  # list of name servers
        'status':          'status:\s*(.+)',  # list of statuses
    }
    def __init__(self, domain, text):
        if 'Domain not found' in text:
            raise PywhoisError(text)
        else:
            WhoisEntry.__init__(self, domain, text, self.regex)

class WhoisFm(WhoisEntry):
    """Whois parser for .fm domains"""
    regex = {
        'domain_name':     'Query:\s*(.+)',
        'registrar':       'Registrar Name:\s*(.+)',
        'creation_date':   'Created:\s*(.+)',
        'updated_date':    'Modified::\s*(.+)',
        'expiration_date': 'Expires:\s*(.+)',
        'name_servers':    'Name Servers:\r?\n\s*(.+) ',
        'status':          'Status:\s*(.+)',  # list of statuses
        'emails': '[\w.-]+@[\w.-]+\.[\w]{2,4}',  # list of email addresses
    }
    def __init__(self, domain, text):
            WhoisEntry.__init__(self, domain, text, self.regex)

class WhoisFr(WhoisEntry):
    """Whois parser for .fr domains (france)"""
    regex = {
        'domain_name':     'domain:\s*(.+)',
        'registrar_id':    'source:\s*(.+)',
        'registrar':       'registrar:\s*(.+)',
        'admin_id':        'admin-c:\s*(.+)',
        'technical_id':    'tech-c:\s*(.+)',
        'creation_date':   'created:\s*(.+)',
        'updated_date':    'last-update:\s*(.+)',
        'name_servers':    'nserver:\s*(.+)',  # list of name servers
        'status':          'status:\s*(.+)',  # list of statuses
        'emails': '[\w.-]+@[\w.-]+\.[\w]{2,4}',  # list of email addresses
    }
    def __init__(self, domain, text):
        if 'No entries found' in text:
            raise PywhoisError(text)
        else:
            WhoisEntry.__init__(self, domain, text, self.regex)

class WhoisInfo(WhoisOrg):
    """identical to WhoisOrg"""
    pass

class WhoisJp(WhoisEntry):
    """Whois parser for .jp domains
    """
    regex = {
        'domain_name': '\[Domain Name\]\s+(.+)',
        'registrar':   '\[Registrant\]\s+(.+)',
        'creation_date': '\[(?:Created on|Registered Date)\]\s+(.+)',
        'updated_date': '\[Last Updated?\]\s+(.+)',
        'expiration_date': '\[Expires on\]\s+(.+)',
        'name_servers': '\[Name Server\]\s+(.+)',
        'status': '\[(?:Status|State)\]\s+(.+)',
        'emails': '[\w.-]+@[\w.-]+\.[\w]{2,4}',  # list of email addresses
    }

    def __init__(self, domain, text):
        if text.strip() == 'No match':
            raise PywhoisError(text)
        else:
            WhoisEntry.__init__(self, domain, text, self.regex)

class WhoisKr(WhoisEntry):
    """Whois parser for .kr domains """
    regex = {
        'domain_name': 'Domain Name\s*:\s*(.+)',
        'creation_date': 'Registered Date\s*:\s*(.+)',
        'updated_date': 'Last updated Date\s*:\s*(.+)',
        'expiration_date': 'Expiration Date\s*:\s*(.+)',
        'registrant': 'Authorized Agency\s*:\s*(.+)',
        'name_servers': 'Name Server\r?\n\s*Host Name\s*:\s*(.+)',
        'status': 'Publishes\s*:\s*(.+)',
        'admin_name': 'Administrative Contact\(AC\):(.+)',
        'emails': '[\w.-]+@[\w.-]+\.[\w]{2,4}',  # list of email addresses
    }

    def __init__(self, domain, text):
        if text.strip() == 'No match':
            raise PywhoisError(text)
        else:
            WhoisEntry.__init__(self, domain, text, self.regex)

class WhoisNo(WhoisEntry):
    """Whois parser for .no domains
    """
    regex = {
        'domain_name': 'Domain Name\.+:\s*(.+)',
        'creation_date': 'Created:\s*(.+)',
        'updated_date': 'Last updated:\s*(.+)',
        'emails': '[\w.-]+@[\w.-]+\.[\w]{2,4}',  # list of email addresses
    }

    def __init__(self, domain, text):
        if text.strip() == 'No match':
            raise PywhoisError(text)
        else:
            WhoisEntry.__init__(self, domain, text, self.regex)

class WhoisNu(WhoisEntry):
    """Whois parser for .nu domains """
    regex = {
        'domain_name':     'Domain Name.*:\s*(.+)',
        'creation_date':   'Record created on (.+)\.',
        'updated_date':    'Record last updated on (.+)\.',
        'expiration_date': 'Record expires on (.+)\.',
        'status':          'Record status:\s*(.+)',
        'name_servers':    'Domain servers in listed order:\r?\n\s*(.+)',
        'emails':          '[\w.-]+@[\w.-]+\.[\w]{2,4}',  # list of email addresses
    }

    def __init__(self, domain, text):
        if 'NO MATCH' in text:
            raise PywhoisError(text)
        else:
            WhoisEntry.__init__(self, domain, text, self.regex)

class WhoisPl(WhoisEntry):
    """Whois parser for .pl domains
    """
    regex = {
        'domain_name': 'DOMAIN NAME:\s*(.+)',
        'creation_date': 'created:\s*(.+)',
        'updated_date': 'last modified:\s*(.+)',
        'name_servers': 'nameservers:\s*(.+)',  # list of name servers
        'emails': '[\w.-]+@[\w.-]+\.[\w]{2,4}',  # list of email addresses
    }

    def __init__(self, domain, text):
        if text.strip() == 'No information available':
            raise PywhoisError(text)
        else:
            WhoisEntry.__init__(self, domain, text, self.regex)

class WhoisRu(WhoisEntry):
    """Whois parser for .ru domains
    """
    regex = {
        'domain_name': 'domain:\s*(.+)',
        'registrar': 'registrar:\s*(.+)',
        'creation_date': 'created:\s*(.+)',
        'expiration_date': 'paid-till:\s*(.+)',
        'name_servers': 'nserver:\s*(.+)',  # list of name servers
        'status': 'state:\s*(.+)',  # list of statuses
        'emails': '[\w.-]+@[\w.-]+\.[\w]{2,4}',  # list of email addresses
    }

    def __init__(self, domain, text):
        if text.strip() == 'No entries found':
            raise PywhoisError(text)
        else:
            WhoisEntry.__init__(self, domain, text, self.regex)

class WhoisSk(WhoisEntry):
    """Whois parser for .sk domain"""
    regex = {
        'domain_name': 'Domain-name\s*(.+)',
        'expiration_date': 'Valid-date\s*(.+)',
        'updated_date': 'Last-update\s*(.+)',
        'name_servers': 'dns_name\s*(.+)',  # list of name servers
        'status': 'Domain-status\s*(.+)',
        'emails': '[\w.-]+@[\w.-]+\.[\w]{2,4}',  # list of email addresses
    }

    def __init__(self, domain, text):
        if 'Not found' in text:
            raise PywhoisError(text)
        else:
            WhoisEntry.__init__(self, domain, text, self.regex)

class WhoisSu(WhoisRu):
    """whois parser for .su, identical to .ru"""
    pass

class WhoisTk(WhoisEntry):
    """Whois parser for .tk domain"""
    regex = {
        'domain_name': 'Domain name:\r?\n\s*(.+)',
        'registrant_name': 'Organisation:\r?\n\s*(.+)',
        'registrar':    'Record maintained by:\s*(.+)',
        'creation_date': 'Domain registered:\s*(.+)',
        'expiration_date': 'Record will expire on (.+)',
        'name_servers': 'Domain Nameservers:\r?\n\s*(.+)',  # list of name servers
        'status': '(Your selected domain name [\r\n\w\s\d]+)',
        'emails': '[\w.-]+@[\w.-]+\.[\w]{2,4}',  # list of email addresses
    }

    def __init__(self, domain, text):
        if text.strip() == 'Invalid query or domain name not known in Dot TK Domain Registry':
            raise PywhoisError(text)
        else:
            WhoisEntry.__init__(self, domain, text, self.regex)

class WhoisTw(WhoisEntry):
    """Whois parser for .tw domains
    """
    regex = {
        'domain_name': 'Domain Name:\s*(.+)',
        'registrar': 'Registration Service Provider:\s*(.+)',
        'creation_date': '\s*Record created on (.+) \(',
        'expiration_date': '\s*Record expires on (.+) \(',
        'name_servers': '\s+([\w\d.-_]+)\s+[\d.]+',  # list of name servers
        'emails': '[\w.-]+@[\w.-]+\.[\w]{2,4}',  # list of email addresses
    }

    def __init__(self, domain, text):
        if text.strip() == 'No found':
            raise PywhoisError(text)
        else:
            WhoisEntry.__init__(self, domain, text, self.regex)

class WhoisName(WhoisEntry):
    """Whois parser for .name domains
    """
    regex = {
    	'domain_name_id':  'Domain Name ID:\s*(.+)',
        'domain_name':     'Domain Name:\s*(.+)',
        'registrar_id':    'Sponsoring Registrar ID:\s*(.+)',
        'registrar':       'Sponsoring Registrar:\s*(.+)',
        'registrant_id':   'Registrant ID:\s*(.+)',
        'admin_id':        'Admin ID:\s*(.+)',
        'technical_id':    'Tech ID:\s*(.+)',
        'billing_id':      'Billing ID:\s*(.+)',
        'creation_date':   'Created On:\s*(.+)',
        'expiration_date': 'Expires On:\s*(.+)',
        'updated_date':    'Updated On:\s*(.+)',
        'name_server_ids': 'Name Server ID:\s*(.+)',  # list of name server ids
        'name_servers':    'Name Server:\s*(.+)',  # list of name servers
        'status':          'Domain Status:\s*(.+)',  # list of statuses
	}
    def __init__(self, domain, text):
        if 'No match.' in text:
            raise PywhoisError(text)
        else:
            WhoisEntry.__init__(self, domain, text, self.regex) 

class WhoisUa(WhoisEntry):
    """Whois parser for .ua domains (ukraine)"""
    regex = {
        'domain_name':     'domain:\s*(.+)',
        'registrar_id':    'source:\s*(.+)',
        'admin_id':        'admin-c:\s*(.+)',
        'technical_id':    'tech-c:\s*(.+)',
        'creation_date':   'created:\s*.+ (.+)',
        'expiration_date': 'status:\s*OK-UNTIL\ (.+)',
        'updated_date':    'changed:\s*.+ (.+)',
        'name_servers':    'nserver:\s*(.+)',  # list of name servers
        'status':          'status:\s*(.+)',  # list of statuses
        'emails': '[\w.-]+@[\w.-]+\.[\w]{2,4}',  # list of email addresses
    }
    def __init__(self, domain, text):
        if 'No entries found for' in text:
            raise PywhoisError(text)
        else:
            WhoisEntry.__init__(self, domain, text, self.regex)
            
class WhoisUs(WhoisEntry):
    """Whois parser for .us domains
    """
    regex = {
        'domain_name':                    'Domain Name:\s*(.+)',
    	'domain__id':                     'Domain ID:\s*(.+)',
        'registrar':                      'Sponsoring Registrar:\s*(.+)',
        'registrar_id':                   'Sponsoring Registrar IANA ID:\s*(.+)',
        'registrar_url':                  'Registrar URL \(registration services\):\s*(.+)',        
        'status':                         'Domain Status:\s*(.+)',  # list of statuses
        'registrant_id':                  'Registrant ID:\s*(.+)',
        'registrant_name':                'Registrant Name:\s*(.+)',
        'registrant_address1':            'Registrant Address1:\s*(.+)',
        'registrant_address2':            'Registrant Address2:\s*(.+)',
        'registrant_city':                'Registrant City:\s*(.+)',
        'registrant_state_province':      'Registrant State/Province:\s*(.+)',
        'registrant_postal_code':         'Registrant Postal Code:\s*(.+)',
        'registrant_country':             'Registrant Country:\s*(.+)',
        'registrant_country_code':        'Registrant Country Code:\s*(.+)',
        'registrant_phone_number':        'Registrant Phone Number:\s*(.+)',
        'registrant_email':               'Registrant Email:\s*(.+)',
        'registrant_application_purpose': 'Registrant Application Purpose:\s*(.+)',
        'registrant_nexus_category':      'Registrant Nexus Category:\s*(.+)',
        'admin_id':                       'Administrative Contact ID:\s*(.+)',
        'admin_name':                     'Administrative Contact Name:\s*(.+)',
        'admin_address1':                 'Administrative Contact Address1:\s*(.+)',
        'admin_address2':                 'Administrative Contact Address2:\s*(.+)',
        'admin_city':                     'Administrative Contact City:\s*(.+)',
        'admin_state_province':           'Administrative Contact State/Province:\s*(.+)',
        'admin_postal_code':              'Administrative Contact Postal Code:\s*(.+)',
        'admin_country':                  'Administrative Contact Country:\s*(.+)',
        'admin_country_code':             'Administrative Contact Country Code:\s*(.+)',
        'admin_phone_number':             'Administrative Contact Phone Number:\s*(.+)',
        'admin_email':                    'Administrative Contact Email:\s*(.+)',
        'admin_application_purpose':      'Administrative Application Purpose:\s*(.+)',
        'admin_nexus_category':           'Administrative Nexus Category:\s*(.+)',
        'billing_id':                     'Billing Contact ID:\s*(.+)',
        'billing_name':                   'Billing Contact Name:\s*(.+)',
        'billing_address1':               'Billing Contact Address1:\s*(.+)',
        'billing_address2':               'Billing Contact Address2:\s*(.+)',
        'billing_city':                   'Billing Contact City:\s*(.+)',
        'billing_state_province':         'Billing Contact State/Province:\s*(.+)',
        'billing_postal_code':            'Billing Contact Postal Code:\s*(.+)',
        'billing_country':                'Billing Contact Country:\s*(.+)',
        'billing_country_code':           'Billing Contact Country Code:\s*(.+)',
        'billing_phone_number':           'Billing Contact Phone Number:\s*(.+)',
        'billing_email':                  'Billing Contact Email:\s*(.+)',
        'billing_application_purpose':    'Billing Application Purpose:\s*(.+)',
        'billing_nexus_category':         'Billing Nexus Category:\s*(.+)',
        'tech_id':                        'Technical Contact ID:\s*(.+)',
        'tech_name':                      'Technical Contact Name:\s*(.+)',
        'tech_address1':                  'Technical Contact Address1:\s*(.+)',
        'tech_address2':                  'Technical Contact Address2:\s*(.+)',
        'tech_city':                      'Technical Contact City:\s*(.+)',
        'tech_state_province':            'Technical Contact State/Province:\s*(.+)',
        'tech_postal_code':               'Technical Contact Postal Code:\s*(.+)',
        'tech_country':                   'Technical Contact Country:\s*(.+)',
        'tech_country_code':              'Technical Contact Country Code:\s*(.+)',
        'tech_phone_number':              'Technical Contact Phone Number:\s*(.+)',
        'tech_email':                     'Technical Contact Email:\s*(.+)',
        'tech_application_purpose':       'Technical Application Purpose:\s*(.+)',
        'tech_nexus_category':            'Technical Nexus Category:\s*(.+)',
        'name_servers':                   'Name Server:\s*(.+)',  # list of name servers
        'created_by_registrar':           'Created by Registrar:\s*(.+)',
        'last_updated_by_registrar':      'Last Updated by Registrar:\s*(.+)',
        'creation_date':                  'Domain Registration Date:\s*(.+)',
        'expiration_date':                'Domain Expiration Date:\s*(.+)',
        'updated_date':                   'Domain Last Updated Date:\s*(.+)',
	}
    def __init__(self, domain, text):
        if 'Not found:' in text:
            raise PywhoisError(text)
        else:
            WhoisEntry.__init__(self, domain, text, self.regex)
            
class WhoisMe(WhoisEntry):
    """Whois parser for .me domains
    """
    regex = {
    	'domain_id':                   'Domain ID:(.+)',
        'domain_name':                 'Domain Name:(.+)',
        'creation_date':               'Domain Create Date:(.+)',
        'updated_date':                'Domain Last Updated Date:(.+)',
        'expiration_date':             'Domain Expiration Date:(.+)',
        'transfer_date':               'Last Transferred Date:(.+)',
        'trademark_name':              'Trademark Name:(.+)',
        'trademark_country':           'Trademark Country:(.+)',
        'trademark_number':            'Trademark Number:(.+)',
        'trademark_application_date':  'Date Trademark Applied For:(.+)',
        'trademark_registration_date': 'Date Trademark Registered:(.+)',
        'registrar':                   'Sponsoring Registrar:(.+)',
        'created_by':                  'Created by:(.+)',
        'updated_by':                  'Last Updated by Registrar:(.+)',
        'status':                      'Domain Status:(.+)',  # list of statuses
        'registrant_id':               'Registrant ID:(.+)',
        'registrant_name':             'Registrant Name:(.+)',
        'registrant_org':              'Registrant Organization:(.+)',
        'registrant_address':          'Registrant Address:(.+)',
        'registrant_address2':         'Registrant Address2:(.+)',
        'registrant_address3':         'Registrant Address3:(.+)',
        'registrant_city':             'Registrant City:(.+)',
        'registrant_state_province':   'Registrant State/Province:(.+)',
        'registrant_country':          'Registrant Country/Economy:(.+)',
        'registrant_postal_code':      'Registrant Postal Code:(.+)',
        'registrant_phone':            'Registrant Phone:(.+)',
        'registrant_phone_ext':        'Registrant Phone Ext\.:(.+)',
        'registrant_fax':              'Registrant FAX:(.+)',
        'registrant_fax_ext':          'Registrant FAX Ext\.:(.+)',
        'registrant_email':            'Registrant E-mail:(.+)',
        'admin_id':                    'Admin ID:(.+)',
        'admin_name':                  'Admin Name:(.+)',
        'admin_org':                   'Admin Organization:(.+)',
        'admin_address':               'Admin Address:(.+)',
        'admin_address2':              'Admin Address2:(.+)',
        'admin_address3':              'Admin Address3:(.+)',
        'admin_city':                  'Admin City:(.+)',
        'admin_state_province':        'Admin State/Province:(.+)',
        'admin_country':               'Admin Country/Economy:(.+)',
        'admin_postal_code':           'Admin Postal Code:(.+)',
        'admin_phone':                 'Admin Phone:(.+)',
        'admin_phone_ext':             'Admin Phone Ext\.:(.+)',
        'admin_fax':                   'Admin FAX:(.+)',
        'admin_fax_ext':               'Admin FAX Ext\.:(.+)',
        'admin_email':                 'Admin E-mail:(.+)',
        'tech_id':                     'Tech ID:(.+)',
        'tech_name':                   'Tech Name:(.+)',
        'tech_org':                    'Tech Organization:(.+)',
        'tech_address':                'Tech Address:(.+)',
        'tech_address2':               'Tech Address2:(.+)',
        'tech_address3':               'Tech Address3:(.+)',
        'tech_city':                   'Tech City:(.+)',
        'tech_state_province':         'Tech State/Province:(.+)',
        'tech_country':                'Tech Country/Economy:(.+)',
        'tech_postal_code':            'Tech Postal Code:(.+)',
        'tech_phone':                  'Tech Phone:(.+)',
        'tech_phone_ext':              'Tech Phone Ext\.:(.+)',
        'tech_fax':                    'Tech FAX:(.+)',
        'tech_fax_ext':                'Tech FAX Ext\.:(.+)',
        'tech_email':                  'Tech E-mail:(.+)',
        'name_servers':                'Nameservers:(.+)',  # list of name servers
	}
    def __init__(self, domain, text):
        if 'NOT FOUND' in text:
            raise PywhoisError(text)
        else:
            WhoisEntry.__init__(self, domain, text, self.regex) 

class WhoisUk(WhoisEntry):
    """Whois parser for .uk domains
    """
    regex = {
        'domain_name':          'Domain name:\r?\n\s*(.+)',
        'registrar':            'Registrar:\r?\n\s*(.+)',
        'registrar_url':        'URL:\s*(.+)',
        'status':               'Registration status:\r?\n\s*(.+)',  # list of statuses
        'registrant_name':      'Registrant:\r?\n\s*(.+)',
        'creation_date':        'Registered on:\s*(.+)',
        'expiration_date':      'Renewal date:\s*(.+)',
        'updated_date':         'Last updated:\s*(.+)',
        'name_servers':         'Name servers:\r?\n\s*(.+)',     # at least get one of them.
	}
    def __init__(self, domain, text):
        if 'Not found:' in text:
            raise PywhoisError(text)
        else:
            WhoisEntry.__init__(self, domain, text, self.regex)

class WhoisIl(WhoisEntry):
    """Whois parser for .il domains
    """
    regex = {
        'creation_date':    'changed:.*\.il (.+) \(Assigned\)',
        'domain_name':      'domain:\s*(.+)',
        'registrar':        'registrar name:\s*(.+)',
        'expiration_date':  'validity:\s*(.+)',
        'name_servers':     'nserver:\s*(.+)',  # list of name servers
        'status':           'status:\s*(.+)',  # list of statuses
        'emails':           '[\w.-]+ AT [\w.-]+\.[\w]{2,4}',  # list of email addresses
    }

    def __init__(self, domain, text):
        if text.strip() == 'No entries found':
            raise PywhoisError(text)
        else:
            WhoisEntry.__init__(self, domain, text, self.regex)
