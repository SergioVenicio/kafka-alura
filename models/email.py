class Email:
    def __init__(self, email_from, email_to, subject, body):
        self.email_from = email_from
        self.email_to = email_to
        self.subject = subject
        self.body = body

    def __repr__(self):
        return f'FROM: {self.email_from}, TO: {self.email_to}, SUBJECT: {self.subject}, BODY: {self.body}'

    def to_dict(self):
        return {
            'from': self.email_from,
            'to': self.email_to,
            'subject': self.subject,
            'body': self.body
        }

    @staticmethod
    def from_dict(dict_value):
        return Email(
            dict_value.get('email_from'),
            dict_value.get('email_to'),
            dict_value.get('subject'),
            dict_value.get('body'),
        )