# from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import io
from docxtpl import DocxTemplate, InlineImage
from .constant_variables import website_url
from docx.shared import Mm


class Invoice:

    def __init__(self, booking) -> None:
        self.booking = booking
        self.customer_full_name = f"{self.booking.customer.user_first_name} {self.booking.customer.user_surname}".capitalize()

    
    @property
    def get_body(self):
        body = f"""
Dear {self.customer_full_name}


please kindly find attached invoice.docx.

Summary:

Description      Quantity
------------------------------------------
Vehicle type: {self.booking.vehicle_type}
Helpers: {self.booking.helpers}
Floors: {self.booking.floors}
Payment Option: {self.booking.payment_option}
------------------------------------------

Description     Prices(ZAR)
------------------------------------------
Base price: R {self.booking.base_amount}
Middle month discount: R -{self.booking.mid_month_discount}
Loyal customer discount: R -{self.booking.loyal_customer_discount}
------------------------------------------
Balance Due: {self.booking.amount_due_customer}
------------------------------------------ 
 

Kind regards
Reload Logistics Services 
Team
                """
        return body
    



    @property
    def cancelation_body(self):
        return f"""
Dear {self.customer_full_name}

We are sorry to hear that you've cancelled your
booking with us. If you ever need to use our services 
please do not hesitate to book with us again, we 
are alway here at your services.

Kind regards 
Reload Logistics Services
Team

"""
    @property
    def header(self):
        return "Reload Logistics Services Invoice-{0}".format(self.booking.id)
    @property
    def cancelation_header(self):
        return "Booking Cancelation Invoice-{0}".format(self.booking.id)
    
    def get_dict(self, doc):
        return {
            "id": self.booking.id,
            "user_email": self.booking.customer.email, 
            "logo": InlineImage(doc, "templates/src/invoice-logo.jpg", width=Mm(27.686), height=Mm(22.86)),
            "customer_full_name": self.customer_full_name,
            "user_contact_number": self.booking.customer.user_contact_number,
            "created_at": self.booking.created_at,
            "pickup_dropoff_routes": self.booking.pickup_dropoff_routes,
            "booking_date": self.booking.booking_date,
            "booking_time": self.booking.booking_time,
            "vehicle_type": self.booking.vehicle_type,
            "helpers": self.booking.helpers,
            "floors": self.booking.floors,
            "distance": self.booking.distance,  
            "base_amount": self.booking.base_amount,
            "mid_month_discount": self.booking.mid_month_discount,
            "loyal_customer_discount": self.booking.loyal_customer_discount,
            "amount_due_customer": self.booking.amount_due_customer}
    
    @property
    def recipient_list(self):
        return [self.booking.customer.email, "eleric44@gmail.com", settings.EMAIL_HOST_USER]
    

    def send_invoice_email(self):

        doc = DocxTemplate('templates/invoice.docx')
        doc.render(self.get_dict(doc))

        if(settings.DEBUG):
            doc.save("templates/output.docx")
            return

        docx_io = io.BytesIO()
        doc.save(docx_io)
        docx_io.seek(0)

        try:
            email = EmailMultiAlternatives(
                    self.header,
                    self.get_body,
                    settings.EMAIL_HOST_USER,
                    self.recipient_list,
                    [settings.EMAIL_HOST_USER]
                    )
            email.attach('invoice.docx',  docx_io.read(), 'application/docx')
            email.fail_silently = True
            email.send()
        except Exception as e:             
            print(str(e))

    
    def send_feedback_email(self):
        pass

    def invoice_cancelation_email(self):

        if settings.DEBUG:
            return False
        
        if(self.booking.booking_cancelation_email_sent == False and 
            self.booking.booking_canceled):
            try:
                email = EmailMultiAlternatives(
                self.cancelation_header,
                self.cancelation_body,
                settings.EMAIL_HOST_USER,
                self.recipient_list,
                [settings.EMAIL_HOST_USER]
                )

                # email.attach('invoice.docx',  docx_io.read(), 'application/docx')
                email.fail_silently = True
                email.send()
                return True
            except Exception as e: 
                print(str(e))
                return True
            
        return False 
        


class UserCustomer:

    def __init__(self, user, reset_token) -> None:
        self.user = user 
        self.user_full_name = f"{str(self.user.user_first_name).capitalize()} {str(self.user.user_surname).capitalize()}"
        self.password_reset_url = f"{website_url}/password/reset/{reset_token}"
    
    @property
    def context(self):
        return {"user_full_name": self.user_full_name,
                 "website_url": website_url}
    
    @property
    def password_reset_context(self):
        return {"user_full_name":self.user_full_name, 
                "password_reset_url":self.password_reset_url,
                "website_url": website_url}
    
    @property
    def welcome_message_header(self):
        return "RELOAD LOGISTICS SERVICES (Pty) Ltd"
    
    @property
    def password_reset_header(self):
        return "RELOAD LOGISTICS SERVICES (Pty) Ltd PASSWORD RESET"
    
    @property
    def recepient_list(self):
        return [self.user.email, "eleric44@gmail.com", settings.EMAIL_HOST_USER]
    
    def send_welcome_message_email(self):
        
        if(settings.DEBUG): return 

        html = render_to_string("new_user.html", self.context)
        text_content = strip_tags(html)

        try:
            #.. send email 
            email = EmailMultiAlternatives(
                        self.welcome_message_header,
                        text_content, 
                        settings.EMAIL_HOST_USER,
                        self.recepient_list,
                        [settings.EMAIL_HOST_USER]
                    )
            
            email.attach_alternative(html, "text/html")  
            email.fail_silently = True
            email.send()
        except Exception as e:
            print(str(e))

    def send_password_reset_email(self):
        if(settings.DEBUG): return 

        html = render_to_string("password_reset.html", self.password_reset_context)
        text_content = strip_tags(html)

        try:
                           #.. send email 
            email = EmailMultiAlternatives(
                        self.password_reset_header,
                        text_content, 
                        settings.EMAIL_HOST_USER,
                        self.recepient_list,
                        [settings.EMAIL_HOST_USER]
                    )
            
            email.attach_alternative(html, "text/html")  
            email.fail_silently = True
            email.send()
        except Exception as e:
            print(str(e))

        


    



class UserContactUs:

    def __init__(self, instance) -> None:
        self.instance = instance 
        self.user_full_name = f"{instance.name} {instance.surname}"

    @property
    def header(self):
        return "Reload Logistics Services"
    @property
    def body(self):
        return f"""
Dear {self.user_full_name}

Thank you for contacting us. 
One of our team members will respond to you shortly.

Kind Regards
Reload Logistics Services 
Team

"""
    @property
    def recepient_list(self):
        return [self.instance.email, "eleric44@gmail.com", settings.EMAIL_HOST_USER]

    def send_thank_you_email(self):

        if(settings.DEBUG): return 

        try:
            #.. send email 
            email = EmailMultiAlternatives(
                        self.header,
                        self.body, 
                        settings.EMAIL_HOST_USER,
                        self.recepient_list,
                        [settings.EMAIL_HOST_USER]
                    )
            
            email.fail_silently = True
            email.send()
        except Exception as e:
            print(str(e))
    


    @property
    def response_header(self):
        return "Reload Logistics Services Question Response"

    @property
    def response_body(self):
        return f"""
Dear {self.user_full_name}

Thank you for enquering with Reload Logistics Services.

Your Question: {self.instance.message}
Answer: {self.instance.message_response}

Kind Regards
Reload Logistics Services 
Team

"""

    # response email 
    def send_response_email(self):

        if(settings.DEBUG): return False
        if(self.instance.respond and 
            len(list(str(self.instance.message_response))) > 0 and 
                self.instance.responded == False):
            
            try: 
                        #.. send email 
                email = EmailMultiAlternatives(
                            self.response_header,
                            self.response_body, 
                            settings.EMAIL_HOST_USER,
                            self.recepient_list,
                            [settings.EMAIL_HOST_USER]
                        )
                
                email.fail_silently = True
                email.send()
                return True
            except Exception as e:
                print(e)
                return True

        return False 
        
            

        