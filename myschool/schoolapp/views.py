from django.shortcuts import render ,redirect
from django.contrib.auth.models import User
from django.contrib import messages
#To replace username to email in login pages...
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
#For Login..
from django.contrib.auth import authenticate,login,logout
from schoolapp.models import Categories , Course ,Level ,Video , UserCourse ,Payment
#forfiltersection..
from django.template.loader import render_to_string
from django.http import JsonResponse
#to calculate video duration
from django.db.models import Sum

#Rezorpay section..
import razorpay
client = razorpay.Client(auth=("rzp_test_Zw4Xic7OozFS5B","AVDTlJwTZRpYNEpzER6Zoh4L"))
from time import time
from django.views.decorators.csrf import csrf_exempt


# #Create your views here.
def base(req):
    return render(req,"base.html")

def home(req):
    category = Categories.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status = 'PUBLISH').order_by('-id')
    context={
        "category":category,
        "course":course
    }
    return render(req,"Main/home.html",context)

def single(req):
    category = Categories.get_all_category(Categories)
    level=Level.objects.all()
    course = Course.objects.all()
    FreeCourse_count = Course.objects.filter(price = 0).count()
    PaidCourse_count =Course.objects.filter(price__gte=1).count()
    context={
        "category":category,
        "level":level,
        "course":course,  
        "FreeCourse_count":FreeCourse_count,
        'PaidCourse_count':PaidCourse_count,      
    }
    return render(req,"Main/single.html",context)

# filter section.....
def filter_data(request):
    category = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')
    
    if price == ['Pricefree']:
       course = Course.objects.filter(price=0)
    elif price == ['PricePaid']:
       course = Course.objects.filter(price__gte=1)
    elif price == ['PriceAll']:
       course = Course.objects.all()
    elif category:
        course =Course.objects.filter(category__id__in = category).order_by("-id")  
    elif level:
       course = Course.objects.filter(level__id__in = level).order_by('-id')      
    else:
       course = Course.objects.all().order_by('-id')

    contaxt ={
        "course":course
    }  

    t = render_to_string('ajax/course.html',contaxt)
    return JsonResponse({'data': t})



def contact(req):
    category = Categories.get_all_category(Categories)
    context ={
        'category':category
    }
    return render(req,"Main/contact.html",context)

def aboutus(req):
    category = Categories.get_all_category(Categories)
    context ={
        'category':category
    }
    return render(req,"Main/aboutus.html",context)


#Loginpages....
def register(request):
    category = Categories.get_all_category(Categories)
    context ={
        'category':category
    }
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(username,email,password)
        # check email
        if User.objects.filter(email=email).exists():
           messages.warning(request,'Email are Already Exists !')
           return redirect('register')
        # check username
        if User.objects.filter(username=username).exists():
           messages.warning(request,'Username are Already exists !')
           return redirect('register')
        user = User(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        return redirect('login')
    return render(request,'registration/register.html',context)




# #To replace username to email in login pages...
class EmailBackEnd(ModelBackend):

    def authenticate(self,  username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None




def doLogin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
		
        user = EmailBackEnd.authenticate(request, username=email, password=password)
        
        if user!=None:
           login(request,user)
           return redirect('home')
        else:
           messages.error(request,'Email and Password Are Invalid !')
           return redirect('login')


#Profile Update Sections..... Error
def profile(request):
    return render(request,'registration/profile.html')


def profile_update(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id

        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request,'Profile Are Successfully Updated. ')
        return redirect('profile')
      
  
#search section.....
def search(req):
    query =req.GET["query"]
    course =Course.objects.filter(title__icontains = query)
    
    context ={
        'course':course
    }
    return render(req, 'Main/search.html',context )


def courseDetails(req,slug):
    category = Categories.get_all_category(Categories)
    time_duration = Video.objects.filter(course__slug = slug).aggregate(sum=Sum('time_duration'))

    course_id =Course.objects.get(slug = slug)
    try:
        check_enroll = UserCourse.objects.get(user = req.user ,course = course_id)

    except UserCourse.DoesNotExist:
        check_enroll = None
         

    course =Course.objects.filter(slug = slug)
    if course.exists():
        course = course.first()
    else:
        return redirect("error")
    context ={
        "course":course,
        "category":category,
        'time_duration':time_duration,
        'check_enroll': check_enroll
    }    
    return render(req,'Main/courseDetail.html',context)


def errorpage(req):
    category = Categories.get_all_category(Categories)
    context ={
        'category':category
    }
    return render(req,'Main/error.html')




def checkout(req ,slug):
    course = Course.objects.get(slug = slug)

    action =req.GET.get('action')
    order = None
    #payment section..
    if course.price == 0:
        course = UserCourse (
            user = req.user,
            course= course,
        )
        course.save()
        messages.success(req,"Your course are successfully Enrool...!!!")
        return redirect('mycourse')
    elif action== 'create_payment':
        if req.method == "POST":
            first_name =req.POST.get('first_name')
            last_name =req.POST.get('last_name')
            country =req.POST.get('country')
            address_1 =req.POST.get('address_1')
            address_2 =req.POST.get('address_2')
            city =req.POST.get('city')
            state =req.POST.get('state')
            postcode =req.POST.get('postcode')
            phone =req.POST.get('phone')
            email =req.POST.get('email')
            order_comments =req.POST.get("order_comments")

            amount = (course.price * 100)
            currency = "INR"
            notes = {
                'name': f'{first_name}{last_name}',
                'country': country,
                'address':f'{address_1} {address_2}',
                'city':city,
                "state":state,
                'postcode':postcode,
                "phone":phone,
                'email':email,
                "order_comments":order_comments,
            }
            #for recipts...
            receipt =f"Skola.{int(time())}"
            order = client.order.create(
                {
                    'receipt': receipt,
                    'notes':notes,
                    'amount':amount,
                    'currency':currency
                }
            )
            payment = Payment(
                course=course,
                user=req.user,
                order_id=order.get('id')
            )
            payment.save()

    context ={
        'course':course,
        'order':order,
    }
    return render(req,'Main/checkout.html',context)


#course section.....
def mycourse(req):
    course = UserCourse.objects.filter(user =req.user)
    context ={
        'course':course,        
    }
    return render(req,'Main/my_course.html',context)


     

@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        data = request.POST
        print(data)
        
    try:
        client.utility.verify_payment_signature(data)
        razorpay_order_id =data['razorpay_order_id']
        razorpay_payment_id =data['razorpay_order_id']

        payment=Payment.objects.get(order_id = razorpay_order_id)
        payment.payment_id = razorpay_payment_id
        payment.status =True

        usercourse = UserCourse(
            user =payment.user,
            course = payment.course,
            )
        usercourse.save()
        payment.user_course = usercourse
        payment.save()

        context ={
                'data':data,
                'payment':payment,
            }
        return render(request,'verify_payment/success.html',context)
    except:
        return render(request,'verify_payment/failed.html') 
               


