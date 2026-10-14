from django.shortcuts import render, redirect
from user.models import tbl_register, tbl_order_info,tbl_order_items
from django.http import HttpResponse
# Create your views here.

def index(request):
    return render(request, "customer/index.html")


def profile(request):
    user = request.session.get("email")
    data = ""

    if user:
        data = tbl_register.objects.all().filter(email=user)

        if request.method == "POST":
            name = request.POST.get("name")
            mobile = request.POST.get("mobile")
            password = request.POST.get("password")
            address = request.POST.get("address")
            picture = request.FILES["fu"]

            tbl_register(
                name=name,
                mobile=mobile,
                password=password,
                address=address,
                profile_picture=picture,
                email=user
            ).save()

            return HttpResponse(
                "<script>alert('your profile is updated successfully..');location.href='/customer/profile/';</script>"
            )

    return render(request, "customer/profile.html", {"userinfo": data})


def logout(request):
    user = request.session.get("email")

    if user:
        del request.session["email"]
        del request.session["uname"]
        del request.session["upic"]
        del request.session["cartitems"]

        return redirect("/user/index/")

    return render(request, "customer/logout.html")


def products(request):
    return render(request, "customer/products.html")


def myorder(request):
    user = request.session.get("email")
    data = ""

    if user:
        data = tbl_order_info.objects.all().filter(userid=user)

    return render(request, "customer/myorder.html", {"data": data})

def orderdetail(request, orderid):
    data = tbl_order_info.objects.get(orderid=orderid)
    items = tbl_order_items.objects.filter(orderid=data)

    return render(request, "customer/orderdetail.html", {
        "data": data,
        "items": items
    })    