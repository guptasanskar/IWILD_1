from django.http import *
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, request
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from docxtpl import DocxTemplate
import jinja2


def dashboard(request):
    return render(request, 'srd.html')


def learning(request):
    return render(request, 'learning.html')


def workflow(request):
    return render(request, 'workflow.html')


#To fetch and Render NIP realted data
def nip(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name', '')
        ap_count = request.POST.get('ap_count', '')
        hostname = request.POST.get('hostname', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        vlan_id = request.POST.get('vlan_id', '')
        ip = request.POST.get('ip', '')
        subnet = request.POST.get('subnet', '')
        gateway_mgmt = request.POST.get('gateway_mgmt', '')
        country = request.POST.get('country', '')
        wlc_model = request.POST.get('wlc_model', '')
        oob_management = request.POST.get('oob_management', '')
        oob_gateway = request.POST.get('oob_gateway', '')
        value_dict = {
            'customer_name': customer_name,
            'ap_count': ap_count,
            'hostname': hostname,
            'username': username,
            'password': password,
            'vlan_id': vlan_id,
            'ip': ip,
            'subnet': subnet,
            'gateway_mgmt': gateway_mgmt,
            'country': country,
            'wlc_model': wlc_model,
            'oob_management': oob_management,
            'oob_gateway': oob_gateway,
        }
        wordGenerateFunc(value_dict, "NIP")
        return render(
            request, 'result_nip.html', {
                'customer_name': customer_name,
                'ap_count': ap_count,
                'hostname': hostname,
                'username': username,
                'password': password,
                'vlan_id': vlan_id,
                'ip': ip,
                'subnet': subnet,
                'gateway_mgmt': gateway_mgmt,
                'country': country,
                'wlc_model': wlc_model,
                'oob_management': oob_management,
                'oob_gateway': oob_gateway,
            })
    else:
        return render(request, 'nip.html')


def sdd(request):
    return render(request, 'sdd.html')


#To fetch and Render SRD realted data
def srd(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name', '')
        user_count = request.POST.get('user_count', '')
        deployment_type = request.POST.get('deployment_type', '')
        controller_model = request.POST.get('controller_model', '')
        in_scope_area = request.POST.get('in_scope_area', '')
        out_of_scope_area = request.POST.get('out_of_scope_area', '')
        rf_environment_type = request.POST.get('rf_environment_type', '')
        user_type = request.POST.getlist('user_type')
        devices_type = request.POST.getlist('devices_type')
        value_dict = {
            'customer_name': customer_name,
            'user_count': user_count,
            'deployment_type': deployment_type,
            'controller_model': controller_model,
            'in_scope_area': in_scope_area,
            'out_of_scope_area': out_of_scope_area,
            'rf_environment_type': rf_environment_type,
            'user_type': user_type,
            'devices_type': devices_type
        }
        wordGenerateFunc(value_dict, "SRD")
        return render(
            request, 'result_srd.html', {
                'customer_name': customer_name,
                'user_count': user_count,
                'deployment_type': deployment_type,
                'controller_model': controller_model,
                'in_scope_area': in_scope_area,
                'out_of_scope_area': out_of_scope_area,
                'rf_environment_type': rf_environment_type,
                'user_type': user_type,
                'devices_type': devices_type
            })

    else:
        return render(request, 'srd.html')


#To Provide data to Word and generate a word file from existing template
def wordGenerateFunc(value_dict, type):
    new_dict = value_dict
    jinja_env = jinja2.Environment(autoescape=True)
    jinja_env.trim_blocks = True
    jinja_env.lstrip_blocks = True
    context = {'value': new_dict}
    try:
        tpl = DocxTemplate(
            "C:/Users/akandalk/OneDrive - Cisco/Desktop/IWILD/deliverables/upload/"
            + type + ".docx")
        print("Doc opened")
        print("tpl", tpl)
        tpl.render(context, jinja_env)
        tpl.save(
            'C:/Users/akandalk/OneDrive - Cisco/Desktop/IWILD/deliverables/downloads/generated'
            + type + '.docx')
    except Exception as e:
        print(e)
        print("Error", e)


#For Calculating RF Assessment
def calculate_hours(stick_deployment_checked, predictive_checked,
                           post_deployment_checked):
    hours = 0
    if stick_deployment_checked:
        hours += 0.3
    if predictive_checked:
        hours += 0.1
    if post_deployment_checked:
        hours += 0.15
    return hours


def rf_assessment(request):
    total_points = 0
    total_hours = 0
    # initialize form values from request.POST or use default values
    
    if request.method == 'POST':
        stick_deployment_checked = request.POST.get('stick_deployment') == 'on' if request.POST else False
        predictive_checked = request.POST.get('Predictive') == 'on' if request.POST else False
        post_deployment_checked = request.POST.get('post_deployment') == 'on' if request.POST else False
        user_input = request.POST.get('user_input') if request.POST else ""
        hours = calculate_hours(stick_deployment_checked,
                                                predictive_checked,
                                                post_deployment_checked)
        total_hours = hours * int(user_input)
        return render(request, 'result_rf_assessment.html', {
            'total_hours': total_hours,
            'stick_deployment_checked': stick_deployment_checked,
            'predictive_checked': predictive_checked,
            'post_deployment_checked': post_deployment_checked,
            'user_input': user_input,
        })
    else: 
        return render(request, 'rf_assessment.html')


