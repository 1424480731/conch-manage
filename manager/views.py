from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from manager.models import PluginManage
from manager.mongo import MongoChengJiApi
import requests
# Create your views here.
mc = MongoChengJiApi()

def plugin(req):

    plugin_msg_list = []
    plugin_set = PluginManage.objects.all()
    for plugin in plugin_set:
        plugin_msg = {
            'plugin_num': plugin.plugin_num,
            'plugin_belong_net': plugin.plugin_belong_net,
            'plugin_name': plugin.plugin_name,
            'plugin_status': plugin.plugin_status,
            'plugin_produce':plugin.produce
        }
        plugin_msg_list.append(plugin_msg)


    return render(req,'plugin.html',{'plugin_msg_list':plugin_msg_list})


def data(req):

    base_all = mc.base_all()

    return render(req,'data.html',{'data':base_all})



def run(req):

    plugin_name = req.GET.get('plugin_name')
    try:
        plugin = PluginManage.objects.get(plugin_name=plugin_name)
        res = requests.get(url='http://127.0.0.1:5000/run/'+plugin_name).json()

        if res.get('msg') == 'ok':

            plugin.plugin_status='插件已运行'
            plugin.save()
            return JsonResponse({'data':1})
        else:
            plugin.plugin_status='插件运行失败'
            plugin.save()
            return JsonResponse({'data':0})
    except:
        return JsonResponse({'data':-1})


def stop(req):

    plugin_name = req.GET.get('plugin_name')
    try:
        plugin = PluginManage.objects.get(plugin_name=plugin_name)
        res = requests.get(url='http://127.0.0.1:5000/stop/' + plugin_name).json()
        if res.get('msg') == 'ok':
            plugin.plugin_status='插件已停止'
            plugin.save()
            return JsonResponse({'data':1})
        else:
            plugin.plugin_status='插件停止失败'
            plugin.save()
            return JsonResponse({'data':0})
    except:
        return JsonResponse({'data':-1})

def area_district(req):

    area_district = mc.get_area_district()
    return JsonResponse({'data':area_district})

def search(req):

    cond = req.GET
    cond_fy = mc.get_fymsg_by_area_district(cond)
    return JsonResponse({'data':cond_fy})