from django.shortcuts import render ,redirect
from . models import *
from random import *
from django.http import HttpResponse
# Create your views here.
def index(request):
    cdata=tbl_category.objects.all().order_by("-id")[0:6]
    pdata=tbl_product.objects.all().order_by("-total_discount")[0:6]
    md={"categories":cdata,"products":pdata}
    return render(request,"user/index.html",md)
def contact(request):
    mydict={}
    if request.method=="POST":
        a=request.POST.get("name")
        b=request.POST.get("mobile")
        c=request.POST.get("email")
        d=request.POST.get("message")
        tbl_contact(name=a,mobile=b,email=c,message=d).save()
        mydict={"msg":"Thankyou you for contact with us"}
    return render(request,"user/contact.html",mydict)
def about(request):
    return render(request,"user/about.html")
def gallery(request):
    data=tbl_gallery.objects.all()
    mydict={'gdata':data}
    return render(request,"user/gallery.html",mydict)
def team(request):
    data=tbl_team.objects.all()
    mydict={'tdata':data}
    return render(request,"user/team.html",mydict)
def profile(request):
    return render(request,"user/profile.html")
def uprofile(request):
    return render(request,"uprofile.html")
def registration(request):
    if request.method=="POST":
        Name=request.POST.get("name")
        Email=request.POST.get("email")
        Mobile=request.POST.get("mobile")
        Password=request.POST.get("password")
        Address=request.POST.get("address")
        ppic=request.FILES["fu"]
        x=tbl_register.objects.all().filter(email=Email).count()
        if x==0:
             tbl_register(name=Name,mobile=Mobile,email=Email,password=Password,address=Address,profile_picture=ppic).save()
             return HttpResponse("<script>alert('you are registered successfully..'); location.href='/user/registration/'</script>")
        else:
             return HttpResponse("<script>alert('you are already registered'); location.href='/user/registration/'</script>")
    return render(request,"user/register.html")
def login(request):
    if request.method=="POST":
       Email=request.POST.get("email")
       Password=request.POST.get("password")
       x=tbl_register.objects.all().filter(email=Email,password=Password).first()
       if x:
           request.session["email"]=str(x.email)
           request.session["uname"]=str(x.name)
           request.session["upic"]=str(x.profile_picture) 
           ccount=tbl_cart.objects.all().filter(userid=Email).count()
           request.session["cartitems"]=ccount
           return HttpResponse("<script>alert('you are login successfully');location.href='/user/products/'</script>")
       else:
           return render(request,"user/login",{"msg":"your Email id or password is incorrect"})
    return render(request,"user/login.html")
def dashboard(request):
    return render(request,"dashboard.html")
def products(request):
    x=request.GET.get("cid")#3
    cdata=tbl_category.objects.all().order_by ("-id")
    pdata=""
    if x is not None:
        pdata=tbl_product.objects.all().filter(category=x)
    else:
        pdata=tbl_product.objects.all().order_by("-id")
        if request.method=="POST":
            pid=request.POST.get("pid")
            pname=request.POST.get("pname")
            ppic=request.POST.get("ppic")
            pprice= float (request.POST.get("pprice"))
            pdiscount=request.POST.get("pdiscount")
            pweight=request.POST.get("pweight")
            pquantity=int(request.POST.get("pquantity"))
            totalprice=pprice*pquantity
            user=request.session.get("email")
            if user:
                if pquantity>0:
                     tbl_cart(userid=user,pid=pid,product_name=pname,product_picture=ppic,price=pprice,discount_price=pdiscount,product_quantity=pquantity,product_weight=pweight,total_price=totalprice).save()
                     ccount=tbl_cart.objects.all().filter(userid=user).count()
                     request.session["cartitems"]=ccount
                     return HttpResponse("<script>alert('Your Item is added in cart...');location.href='/user/products/'</script>")
                else:
                     return HttpResponse("<script>alert('please increase your products quantity...');location.href='/user/products/'</script>")
                
            else:
                return HttpResponse("<script>alert('you have login first...');location.href='/user/login'</script>")


    md={"categories":cdata,"products":pdata}
    
    return render(request,"user/products.html",md)
def cart(request):
    cartid=request.GET.get("cid")
    email=request.session.get("email")
    cartItems=tbl_cart.objects.all().filter(userid=email)
    total=0
    for cart in cartItems:
        total+=cart.total_price
    orderid="TECHPILE:"+str(randint(10000,20000))
    if cartid is not None:
        tbl_cart.objects.all().filter(id=cartid).delete()
        ccount=tbl_cart.objects.all().filter(userid=email).count()
        request.session["cartitems"]=ccount
        return HttpResponse("<script>alert('your cart item deleted successfully...');location.href='/user/cart/'</script>")
    if email:
        if request.method=="POST":
            name=request.POST.get("name")
            mobile=request.POST.get("mobile")
            address=request.POST.get("address")
            tbl_order_info.objects.create(
                userid=email,
                orderid=orderid,
                name=name,
                mobile=mobile,
                 address=address,
                total_amount=total
            )
            for x in cartItems:
                tbl_order_items.objects.create(
                    orderid=order,
                    product_name=x.product_name,
                    product_picture=x.product_picture,
                    price=x.price,
                    discount_picture=x.discount_price,
                    product_quantity=x.product_quantity,
                    product_weight=x.product_weight,
                    total_price=x.total_price
                )
                cartItems.delete()
                ccount=tbl_cart.objects.all().filter(userid=email).count()
                request.session["cartitems"]=ccount
                return render(request,"user/cart.html",{"msg":"your order has been place successfully"})
    return render(request,"user/cart.html",{"data":cartItems,"payable_amount":total,"ord":orderid})