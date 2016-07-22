from django.shortcuts import render

from django.http import HttpResponse,StreamingHttpResponse
from Report.forms import HMCForm,HMCSelectForm
from Report.models import HardwareManagementConsole,ManagedSystem,LogicalPartition,VirtualIOServer
from django.shortcuts import render_to_response
from HmcRestApi.report_generator import generate_report,sync_database
# Create your views here.
def index(request):
    #print( request.method )
    if request.method == 'POST' :
        f = HMCForm(request.POST)
        f.save()

    form = HMCForm()
    selectForm = HMCSelectForm()


    return render(request,'Report/index.html',{'form':form,'select_form':selectForm, },)

class ManagedSystemFeatures(object):
    def __init__(self,name):
        self.name = name
        self.lpar_count = 0
        self.vios_count = 0
        self.lpar_list = []
        self.vios_list = []
    def process_data(self, lpar_list, vios_list):
        self.lpar_count = len(lpar_list)
        self.vios_count = len(vios_list)
        self.lpar_list = lpar_list
        self.vios_list = vios_list

def get_hmc_list( name ):
    ms_obj_list = ManagedSystem.objects.filter(associated_hmc=name)
    #print("N° Managed Systems: ", len(ms_obj_list))
    ms_list = []
    for i in ms_obj_list:
        tmp = ManagedSystemFeatures(i.name)
        lpar_tmp = LogicalPartition.objects.filter(associated_managed_system=i.id)
        #print("N° LPARs: ", len(lpar_tmp))
        vios_tmp = VirtualIOServer.objects.filter(associated_managed_system=i.id)
        #print("N° VIOS's: ", len(vios_tmp))
        tmp.process_data(lpar_tmp, vios_tmp)
        ms_list.append(tmp)
    return ms_list

def hmc_report(request):
    #print(request.method)

    if request.method == 'POST' and 'Select' in request.POST['submit']:
        info = request.POST
        hmc_list = HardwareManagementConsole.objects.all()
        hmc_obj = hmc_list[int(info['field'])]
        ms_list = get_hmc_list(hmc_obj.name)
        return render(request, 'Report/hmc_report.html', {'hmc_obj': hmc_obj, 'ms_list': ms_list,'net_status':0})
    elif request.method == 'POST' and 'Remove' in request.POST['submit']:
        info = request.POST
        hmc_list = HardwareManagementConsole.objects.all()
        hmc_obj = hmc_list[int(info['field'])]
        ms_list = ManagedSystem.objects.filter(associated_hmc=hmc_obj.name)
        for i in ms_list:
            LogicalPartition.objects.filter(associated_managed_system=i.id).delete()
            VirtualIOServer.objects.filter(associated_managed_system=i.id).delete()
        ManagedSystem.objects.filter(associated_hmc=hmc_obj.name).delete()
        HardwareManagementConsole.objects.filter(name=hmc_obj.name).delete()
        request.method = 'GET'
        return index(request)
    elif request.method == 'GET':
        #
        #
        #
        #AARREGGGLAARRRR
        #
        #
        print(request.GET['hmc_name'])

        if 'download_report' in request.GET:
            #generate_report()
            #print( generate_report(request.GET['hmc_name']))
            outContent = generate_report(request.GET['hmc_name'])
            excelname = request.GET['hmc_name']+"_report.xlsx"

            response = HttpResponse(outContent, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=%s' % excelname
            return response
        elif 'update_records' in request.GET:
            hmc_obj = HardwareManagementConsole.objects.filter(name=request.GET['hmc_name']).first()
            return_statement = sync_database( hmc_obj )
            if return_statement:
                return render(request, 'Report/hmc_report.html', {'hmc_obj': hmc_obj, 'ms_list': get_hmc_list(request.GET['hmc_name']),'net_status':1})
            else:
                return render(request, 'Report/hmc_report.html',
                              {'hmc_obj': hmc_obj, 'ms_list': get_hmc_list(request.GET['hmc_name']),'net_status':2})



    return render(request,'Report/404.html')


