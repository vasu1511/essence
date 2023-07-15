from django import template

register = template.Library()


@register.filter(name='orderstatus')
def orderstatus(request,num):
    if(num==0):
        return "order placed"
    elif(num==1):
        return "not packed"
    elif(num==2):
        return "packed"
    elif(num==3):
        return "ready to dispatch"
    elif(num==4):
        return "dispatched"
    elif(num==5):
        return "out for delivery"
    elif(num==6):
        return "delivered"
    else:
        return "cancelled"
    

@register.filter(name='paymentstatus')
def paymentstatus(request,num):
    if(num==0):
        return "PEnding"
    else:
        return "Done"
    
@register.filter(name='paymentmode')
def paymentmode(request,num):
    if(num==0):
        return "COD"
    else:
        return "Net Banking"