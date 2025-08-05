import smtplib
import email.message
from datetime import date
import locale

fireAlerts = 20
defAlerts = 50

locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
eventDate = date.today().strftime("%d de %B de %Y")

## Send alert emails

def sendEmail(fireAlerts, defAlerts, eventDate):  
    
    # Format e-mail 
    email_body = f"""
        <div>
            <p style="margin-top: 0; margin-bottom: 8px; font-family: Arial, Helvetica, sans-serif; font-size: 14px; line-height:1.8; color: #000000; text-align:left;">Informo que houve a ocorrência de <strong>{fireAlerts}</strong> focos de calor e <strong>{defAlerts}</strong> hectares de alertas de desmatamento, em <strong>{eventDate}</strong>, na região norte da <i>Terrra Indígena Campinas/Katukina</i>.</p>
            <p style="margin-top: 0; margin-bottom: 8px; font-family: Arial, Helvetica, sans-serif; font-size: 14px; line-height:1.8; color: #000000; text-align:left;">Para mais informações acesse o portal <a href="https://www.nokekoi.ufac.br/" target="_blank">https://www.nokekoi.ufac.br/</a>. </p>
        </div>

        <br>
        <br>

        <div>
            <table style="width: 100%; border-collapse:collapse; border-spacing:0px;" border="0" cellpadding="0" cellspacing="0">
                <tbody>
                    <tr>
                        <td>
                            <p style="margin-top: 0; margin-bottom: 8px; font-family: Arial, Helvetica, sans-serif; font-size: 20px; line-height:1; color: #42017C; text-align:left;"><b>Dr. Willian Flores</b></p>
                            <p style="margin-top: 0; margin-bottom: 16px; font-family: Arial, Helvetica, sans-serif; font-size: 14px; line-height:1; color: #000000; text-align:left;">Professor / Pesquisador UFAC Campus Floresta</p>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    """
    msg = email.message.Message()
    msg['Subject'] = "Alerta de queimadas e/ou desmatamento..."
    msg['From'] = "willian.flores@ufac.br"
    msg['To'] = "willianflores@gmail.com"
    password =  "U$4ep6My " #"doytkvjwtlenxpfe"  
    msg.add_header("Content-Type", "text/html")
    msg.set_payload(email_body )

    # Send e-mail
    try:
        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        
        # Login Credentials for sending the mail
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    
        print('Email enviado')


sendEmail(fireAlerts,defAlerts,eventDate)

